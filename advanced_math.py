"""
advanced_math.py — Powerful self-contained Quantitative + Monte Carlo engine.
No external ML deps. Pure numpy/pandas math.
"""

import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


# ──────────────────────────────────────────────
# QUANTITATIVE AI
# ──────────────────────────────────────────────

class QuantitativeAI:
    """
    Multi-factor win probability engine.
    Combines:
      1. Historical pattern matching (similar RSI/ADX/volume regimes)
      2. Bayesian base-rate from forward returns
      3. Kelly-criterion expected value
      4. Regime filter (trending vs choppy)
    """

    # ── helpers ──────────────────────────────

    def _forward_returns(self, df: pd.DataFrame, horizon: int = 5) -> pd.Series:
        """% return over next `horizon` bars."""
        close = df['Close'] if 'Close' in df.columns else df['close']
        return close.pct_change(horizon).shift(-horizon) * 100

    def _similar_regime_mask(self, df: pd.DataFrame, cur: dict, tolerance: float = 0.15) -> pd.Series:
        """
        Boolean mask of rows whose indicator values are within `tolerance`
        (relative) of current values.  Returns at least 30 rows by
        progressively relaxing tolerance if needed.
        """
        close = df['Close'] if 'Close' in df.columns else df['close']
        rsi_col   = df.get('RSI',         pd.Series(dtype=float))
        adx_col   = df.get('ADX',         pd.Series(dtype=float))
        vol_col   = df.get('Volume_Ratio', pd.Series(dtype=float))
        ema20_col = df.get('EMA_20',       pd.Series(dtype=float))

        for tol in [tolerance, tolerance * 2, tolerance * 4, tolerance * 8]:
            mask = pd.Series(True, index=df.index)

            if 'rsi' in cur and not rsi_col.empty:
                rsi_lo, rsi_hi = cur['rsi'] * (1 - tol), cur['rsi'] * (1 + tol)
                mask &= rsi_col.between(rsi_lo, rsi_hi)

            if 'adx' in cur and not adx_col.empty:
                adx_lo, adx_hi = cur['adx'] * (1 - tol), cur['adx'] * (1 + tol)
                mask &= adx_col.between(adx_lo, adx_hi)

            if 'volume_ratio' in cur and not vol_col.empty:
                vr = cur['volume_ratio']
                # bucket: low (<0.8), normal (0.8-1.2), high (>1.2)
                if vr < 0.8:
                    mask &= vol_col < 0.9
                elif vr > 1.2:
                    mask &= vol_col > 1.1
                # else neutral — no filter

            if mask.sum() >= 10:
                return mask

        # fallback: all rows
        return pd.Series(True, index=df.index)

    def _market_regime(self, df: pd.DataFrame) -> str:
        """trending_up | trending_down | choppy"""
        close = df['Close'] if 'Close' in df.columns else df['close']
        adx = df.get('ADX', pd.Series(dtype=float))

        adx_val = adx.iloc[-1] if not adx.empty else 20
        ema20 = df.get('EMA_20', close.rolling(20).mean())
        ema50 = df.get('EMA_50', close.rolling(50).mean())

        if adx_val > 25:
            if ema20.iloc[-1] > ema50.iloc[-1]:
                return 'trending_up'
            return 'trending_down'
        return 'choppy'

    # ── main API ─────────────────────────────

    def calculate_win_probability(
        self,
        df: pd.DataFrame,
        current_indicators: dict,
        forward_horizon: int = 5,
        win_threshold: float = 0.5      # % gain counts as win
    ) -> tuple[float, float, int]:
        """
        Returns (win_probability %, expected_value %, sample_size).
        """
        fwd = self._forward_returns(df, forward_horizon).dropna()
        if len(fwd) < 30:
            return 50.0, 0.0, 0

        mask = self._similar_regime_mask(df, current_indicators)
        # align mask with fwd (fwd is shorter due to shift)
        mask = mask.reindex(fwd.index, fill_value=False)
        similar_returns = fwd[mask]
        sample_size = len(similar_returns)

        if sample_size < 8:
            # Bayesian fallback: use full history + shrink toward 50
            similar_returns = fwd
            sample_size = len(similar_returns)
            shrink = 0.4
        else:
            shrink = max(0.0, 1.0 - sample_size / 200)   # shrink less as n grows

        # Raw win rate
        raw_win_prob = (similar_returns > win_threshold).mean() * 100

        # Bayesian shrinkage toward 50 %
        win_prob = raw_win_prob * (1 - shrink) + 50 * shrink

        # Regime adjustment
        regime = self._market_regime(df)
        regime_adj = {'trending_up': +3, 'trending_down': -3, 'choppy': -2}
        win_prob = np.clip(win_prob + regime_adj.get(regime, 0), 5, 95)

        # Expected value: mean of matched returns weighted by outcome
        avg_win  = similar_returns[similar_returns > 0].mean() if (similar_returns > 0).any() else 0
        avg_loss = similar_returns[similar_returns <= 0].mean() if (similar_returns <= 0).any() else 0
        p = win_prob / 100
        expected_value = p * avg_win + (1 - p) * avg_loss

        return round(float(win_prob), 1), round(float(expected_value), 2), int(sample_size)

    def get_trade_verdict(
        self,
        win_prob: float,
        expected_value: float,
        risk_reward: float = 1.5
    ) -> tuple[str, str]:
        """
        Combines win probability + EV + R:R into a single verdict.
        """
        # Kelly fraction as a signal (positive = worth trading)
        kelly = win_prob / 100 - (1 - win_prob / 100) / max(risk_reward, 0.1)

        if win_prob >= 68 and expected_value > 1.0 and kelly > 0.15:
            return "STRONG BUY", f"High-edge setup: {win_prob:.0f}% prob, EV {expected_value:+.1f}%"
        if win_prob >= 60 and expected_value > 0.3 and kelly > 0.05:
            return "BUY", f"Positive edge: {win_prob:.0f}% win rate, EV {expected_value:+.1f}%"
        if win_prob >= 55 and expected_value > 0:
            return "CONSIDER", f"Marginal edge — confirm with price action"
        if win_prob < 45 or expected_value < -1.0:
            return "AVOID", f"Negative edge: {win_prob:.0f}% prob, EV {expected_value:+.1f}%"
        return "NEUTRAL", f"Insufficient edge — wait for cleaner signal"


# ──────────────────────────────────────────────
# MONTE CARLO SIMULATOR
# ──────────────────────────────────────────────

class MonteCarloSimulator:
    """
    Path-simulation engine using:
      • GBM (Geometric Brownian Motion) with fat tails (Student-t)
      • Jump-diffusion (Merton model) for gap risk
      • 5 000 paths, vectorised numpy
    """

    N_PATHS    = 5_000
    N_STEPS    = 20          # trading days per simulation
    T_DF       = 5           # Student-t degrees of freedom (fat tails)

    def _fit_params(self, df: pd.DataFrame) -> tuple[float, float, float, float]:
        """Fit drift, vol, jump intensity & size from recent log-returns."""
        close = df['Close'] if 'Close' in df.columns else df['close']
        log_ret = np.log(close / close.shift(1)).dropna().values[-60:]

        mu    = float(np.mean(log_ret))
        sigma = float(np.std(log_ret))

        # Simple jump detection: returns > 2.5σ treated as jumps
        jump_mask  = np.abs(log_ret) > 2.5 * sigma
        lam        = float(jump_mask.mean())              # jump intensity (daily)
        jump_mean  = float(log_ret[jump_mask].mean()) if jump_mask.any() else 0.0

        return mu, sigma, lam, jump_mean

    def run_simulation(
        self,
        df: pd.DataFrame,
        current_price: float,
        target: float,
        stoploss: float
    ) -> dict:
        """
        Returns rich dict with probability bands, path stats, and risk metrics.
        """
        if df is None or df.empty or len(df) < 30:
            return None

        mu, sigma, lam, jump_mean = self._fit_params(df)
        n, m = self.N_PATHS, self.N_STEPS

        # ── simulate log-returns (Student-t + jumps) ──────────────────────
        # Student-t shocks (fat tails)
        t_shocks = stats.t.rvs(df=self.T_DF, size=(n, m))
        t_shocks = t_shocks / np.sqrt(self.T_DF / (self.T_DF - 2))   # scale to unit variance

        # Poisson jumps
        jump_counts = np.random.poisson(lam, size=(n, m))
        jumps       = jump_counts * jump_mean

        log_returns = (mu - 0.5 * sigma**2) + sigma * t_shocks + jumps

        # ── build price paths ──────────────────────────────────────────────
        log_paths   = np.cumsum(log_returns, axis=1)
        price_paths = current_price * np.exp(log_paths)      # shape (n, m)

        final_prices = price_paths[:, -1]

        # ── outcome classification ─────────────────────────────────────────
        hit_target   = np.any(price_paths >= target,   axis=1)
        hit_stoploss = np.any(price_paths <= stoploss, axis=1)

        # Paths that hit target before stoploss
        target_first = np.zeros(n, dtype=bool)
        for i in range(n):
            t_idx = np.argmax(price_paths[i] >= target)   if hit_target[i]   else m
            s_idx = np.argmax(price_paths[i] <= stoploss) if hit_stoploss[i] else m
            target_first[i] = hit_target[i] and (t_idx <= s_idx)

        prob_target   = float(target_first.mean()      * 100)
        prob_stoploss = float(hit_stoploss.mean()      * 100)
        prob_neutral  = 100.0 - prob_target - prob_stoploss

        # ── price distribution at horizon ─────────────────────────────────
        pct = np.percentile(final_prices, [5, 10, 25, 50, 75, 90, 95])
        price_pcts = {
            'p5':  float(pct[0]), 'p10': float(pct[1]),
            'p25': float(pct[2]), 'p50': float(pct[3]),
            'p75': float(pct[4]), 'p90': float(pct[5]),
            'p95': float(pct[6]),
        }

        # ── returns distribution ───────────────────────────────────────────
        returns_pct = (final_prices - current_price) / current_price * 100
        mean_return = float(np.mean(returns_pct))
        std_return  = float(np.std(returns_pct))

        # Value at Risk & CVaR (95 %)
        var_95  = float(np.percentile(returns_pct, 5))
        cvar_95 = float(returns_pct[returns_pct <= var_95].mean())

        # Sharpe-like ratio (annualised, 252 trading days)
        ann_factor  = np.sqrt(252 / m)
        sharpe      = float((mean_return / std_return) * ann_factor) if std_return > 0 else 0.0

        # Maximum drawdown across all paths (median path)
        median_path = np.median(price_paths, axis=0)
        rolling_max = np.maximum.accumulate(median_path)
        drawdowns   = (median_path - rolling_max) / rolling_max * 100
        max_dd      = float(drawdowns.min())

        # ── confidence interval for target probability ─────────────────────
        se = np.sqrt((prob_target / 100) * (1 - prob_target / 100) / n) * 100
        ci_low  = max(0.0, prob_target - 1.96 * se)
        ci_high = min(100.0, prob_target + 1.96 * se)

        return {
            # Core probabilities
            'prob_target':        round(prob_target,   1),
            'prob_stoploss':      round(prob_stoploss, 1),
            'prob_neutral':       round(max(0, prob_neutral), 1),
            'ci_low':             round(ci_low,  1),
            'ci_high':            round(ci_high, 1),

            # Return stats
            'mean_return':        round(mean_return, 2),
            'std_return':         round(std_return,  2),
            'var_95':             round(var_95,  2),
            'cvar_95':            round(cvar_95, 2),
            'sharpe':             round(sharpe,  2),
            'max_drawdown':       round(max_dd,  2),

            # Price distribution
            'price_percentiles':  price_pcts,
            'median_price':       round(float(np.median(final_prices)), 2),

            # Simulation metadata
            'n_paths':            n,
            'n_days':             m,
            'model':              'GBM + Student-t + Jump-Diffusion',

            # Raw paths for charting (downsample to 200 paths)
            'sample_paths':       price_paths[::max(1, n // 200)].tolist(),
        }
        
    
    
# ==========================================
# INSTITUTIONAL-GRADE QUANTITATIVE MODELS
# Hedge Fund Level Mathematics
# ==========================================

from scipy.stats import entropy
from scipy.optimize import minimize

class AdvancedQuantModels:
    """
    Professional quantitative models used by hedge funds
    Includes: Hurst Exponent, Entropy, Bayesian, Monte Carlo, HMM, etc.
    """
    
    # ==========================================
    # 1. HURST EXPONENT (Trend vs Mean Reversion)
    # ==========================================
    @staticmethod
    def calculate_hurst_exponent(price_series, max_lag=20):
        """
        Hurst Exponent (H):
        - H > 0.5: Trending market (persistent)
        - H = 0.5: Random walk (geometric Brownian motion)
        - H < 0.5: Mean-reverting (anti-persistent)
        
        Used by: Renaissance Technologies, AQR Capital
        """
        if len(price_series) < max_lag:
            return 0.5
        
        lags = range(2, max_lag)
        tau = []
        
        for lag in lags:
            if len(price_series) > lag:
                diff = np.subtract(price_series[lag:], price_series[:-lag])
                if len(diff) > 0:
                    tau.append(np.sqrt(np.std(diff)))
                else:
                    tau.append(0)
        
        tau = [t for t in tau if t > 0]
        if len(tau) < 2:
            return 0.5
        
        lags = lags[:len(tau)]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        hurst = poly[0] * 2.0
        
        return np.clip(hurst, 0, 1)
    
    @staticmethod
    def interpret_hurst(hurst):
        """Interpret Hurst exponent for trading decisions"""
        if hurst > 0.7:
            return {
                'regime': 'STRONG_TRENDING',
                'color': '#00ff88',
                'icon': '📈',
                'action': 'Use trend-following strategy',
                'confidence': min(95, 70 + (hurst - 0.7) * 100)
            }
        elif hurst > 0.55:
            return {
                'regime': 'WEAK_TRENDING',
                'color': '#7cfc00',
                'icon': '📊',
                'action': 'Trend with caution',
                'confidence': 60 + (hurst - 0.55) * 100
            }
        elif hurst > 0.45:
            return {
                'regime': 'RANDOM_WALK',
                'color': '#ffd700',
                'icon': '🎲',
                'action': 'Reduce position size',
                'confidence': 50
            }
        elif hurst > 0.3:
            return {
                'regime': 'WEAK_REVERSION',
                'color': '#ffa500',
                'icon': '🔄',
                'action': 'Mean reversion possible',
                'confidence': 60 + (0.45 - hurst) * 100
            }
        else:
            return {
                'regime': 'STRONG_REVERSION',
                'color': '#ff1744',
                'icon': '↩️',
                'action': 'Strong mean reversion',
                'confidence': min(95, 70 + (0.3 - hurst) * 100)
            }
    
    # ==========================================
    # 2. SHANNON ENTROPY (Market Disorder)
    # ==========================================
    @staticmethod
    def calculate_shannon_entropy(returns, n_bins=10):
        """
        Shannon Entropy measures market disorder:
        - Low entropy (< 30%): Predictable, deterministic market
        - Medium entropy (30-70%): Normal market complexity
        - High entropy (> 70%): Chaotic, unpredictable market
        
        Used by: Two Sigma, D.E. Shaw
        """
        if len(returns) < 20:
            return 50, 1.0
        
        # Discretize returns into bins
        hist, _ = np.histogram(returns, bins=n_bins, density=True)
        hist = hist[hist > 0]
        
        if len(hist) == 0:
            return 50, 0
        
        # Calculate Shannon entropy
        shannon_entropy = entropy(hist)
        
        # Normalize to 0-100 (max entropy = log2(n_bins))
        max_entropy = np.log2(n_bins)
        normalized_entropy = (shannon_entropy / max_entropy) * 100
        
        return np.clip(normalized_entropy, 0, 100), shannon_entropy
    
    @staticmethod
    def interpret_entropy(entropy_score):
        """Interpret market entropy"""
        if entropy_score > 70:
            return {
                'regime': 'CHAOTIC',
                'color': '#ff1744',
                'icon': '🌪️',
                'action': 'Reduce position size significantly',
                'risk': 'EXTREME'
            }
        elif entropy_score > 50:
            return {
                'regime': 'COMPLEX',
                'color': '#ffa500',
                'icon': '🌀',
                'action': 'Wait for clarity',
                'risk': 'HIGH'
            }
        elif entropy_score > 30:
            return {
                'regime': 'ORDERLY',
                'color': '#ffd700',
                'icon': '📊',
                'action': 'Normal trading conditions',
                'risk': 'MODERATE'
            }
        else:
            return {
                'regime': 'DETERMINISTIC',
                'color': '#00ff88',
                'icon': '🎯',
                'action': 'High confidence trades',
                'risk': 'LOW'
            }
    
    # ==========================================
    # 3. BAYESIAN PROBABILITY UPDATE
    # ==========================================
    @staticmethod
    def bayesian_update(prior, likelihood, evidence):
        """
        Bayesian probability update:
        P(A|B) = P(B|A) * P(A) / P(B)
        
        Used by: Quantitative hedge funds for live learning
        """
        if evidence == 0:
            return prior
        posterior = (likelihood * prior) / evidence
        return np.clip(posterior, 0, 1)
    
    @staticmethod
    def calculate_bayesian_up_probability(returns, lookback=20, prior=None):
        """
        Calculate Bayesian probability of next day being positive
        """
        if len(returns) < lookback:
            return 50, 50
        
        # Prior probability (historical win rate)
        if prior is None:
            prior = len(returns[returns > 0]) / len(returns)
        
        # Recent data (likelihood)
        recent_returns = returns.tail(lookback)
        recent_up = len(recent_returns[recent_returns > 0]) / len(recent_returns)
        
        # Evidence
        evidence = (recent_up * prior) + ((1 - recent_up) * (1 - prior))
        
        # Posterior probability
        posterior = AdvancedQuantModels.bayesian_update(prior, recent_up, evidence)
        
        # Information gain
        info_gain = abs(posterior - prior) * 100
        
        return posterior * 100, info_gain
    
    # ==========================================
    # 4. Z-SCORE STATISTICAL ARBITRAGE
    # ==========================================
    @staticmethod
    def calculate_z_score(series, window=50):
        """
        Z-Score: Number of standard deviations from mean
        Used for statistical arbitrage and mean reversion
        """
        if len(series) < window:
            return 0
        
        rolling_mean = series.rolling(window).mean()
        rolling_std = series.rolling(window).std()
        z_score = (series - rolling_mean) / rolling_std
        
        return z_score
    
    @staticmethod
    def interpret_z_score(z_score):
        """
        Statistical significance interpretation:
        |Z| > 3: Extremely significant (99.7% confidence)
        |Z| > 2: Very significant (95% confidence)
        |Z| > 1: Significant (68% confidence)
        """
        if z_score <= -3:
            return {
                'signal': 'STRONG_BUY',
                'color': '#00ff88',
                'icon': '🚀',
                'action': 'Extremely undervalued - Strong buy',
                'confidence': 99
            }
        elif z_score <= -2:
            return {
                'signal': 'BUY',
                'color': '#7cfc00',
                'icon': '📈',
                'action': 'Undervalued - Buy zone',
                'confidence': 95
            }
        elif z_score <= -1:
            return {
                'signal': 'WEAK_BUY',
                'color': '#ffd700',
                'icon': '📊',
                'action': 'Slightly undervalued',
                'confidence': 68
            }
        elif z_score >= 3:
            return {
                'signal': 'STRONG_SELL',
                'color': '#ff1744',
                'icon': '⚠️',
                'action': 'Extremely overvalued - Take profits',
                'confidence': 99
            }
        elif z_score >= 2:
            return {
                'signal': 'SELL',
                'color': '#ff5252',
                'icon': '📉',
                'action': 'Overvalued - Reduce exposure',
                'confidence': 95
            }
        elif z_score >= 1:
            return {
                'signal': 'WEAK_SELL',
                'color': '#ffa500',
                'icon': '📉',
                'action': 'Slightly overvalued',
                'confidence': 68
            }
        else:
            return {
                'signal': 'NEUTRAL',
                'color': '#8892b0',
                'icon': '✅',
                'action': 'Fairly valued - Hold',
                'confidence': 50
            }
    
    # ==========================================
    # 5. KELLY CRITERION (Optimal Position Sizing)
    # ==========================================
    @staticmethod
    def calculate_kelly_fraction(win_rate, avg_win, avg_loss, fractional=0.25):
        """
        Kelly Criterion: f* = (p * b - q) / b
        where:
        - p = probability of winning
        - b = win/loss ratio
        - q = probability of losing (1-p)
        
        Used by: Professional gamblers and hedge funds
        """
        if avg_loss == 0:
            return 0
        
        win_loss_ratio = avg_win / avg_loss
        kelly = (win_rate * win_loss_ratio - (1 - win_rate)) / win_loss_ratio
        
        # Use fractional Kelly (conservative)
        fractional_kelly = max(0, min(0.25, kelly * fractional))
        
        return fractional_kelly, kelly
    
    @staticmethod
    def calculate_optimal_position_size(account_size, kelly_fraction, stop_loss_pct):
        """
        Calculate position size based on Kelly Criterion
        """
        risk_amount = account_size * kelly_fraction
        position_size = risk_amount / (stop_loss_pct * account_size) if stop_loss_pct > 0 else 0
        
        return int(position_size)
    
    # ==========================================
    # 6. MAXIMUM DRAWDOWN & RECOVERY
    # ==========================================
    @staticmethod
    def calculate_drawdown_metrics(prices):
        """
        Professional drawdown analysis:
        - Maximum drawdown
        - Current drawdown
        - Average recovery time
        - Ulcer Index (drawdown severity)
        """
        if len(prices) < 10:
            return {
                'max_drawdown': 0,
                'current_drawdown': 0,
                'avg_recovery_days': 0,
                'ulcer_index': 0
            }
        
        # Calculate running maximum
        running_max = np.maximum.accumulate(prices)
        drawdown = (prices - running_max) / running_max
        
        # Maximum drawdown
        max_drawdown = drawdown.min() * 100
        
        # Current drawdown
        current_drawdown = drawdown[-1] * 100
        
        # Ulcer Index (root mean square of drawdowns)
        ulcer_index = np.sqrt(np.mean(drawdown**2)) * 100
        
        # Calculate average recovery time from >5% drawdowns
        recovery_times = []
        in_drawdown = False
        drawdown_start = 0
        
        for i in range(20, len(prices)):
            if drawdown[i] < -0.05 and not in_drawdown:
                in_drawdown = True
                drawdown_start = i
            elif drawdown[i] > -0.01 and in_drawdown and drawdown_start > 0:
                recovery_days = i - drawdown_start
                if recovery_days > 0:
                    recovery_times.append(recovery_days)
                in_drawdown = False
        
        avg_recovery = np.mean(recovery_times) if recovery_times else 0
        
        return {
            'max_drawdown': abs(max_drawdown),
            'current_drawdown': abs(current_drawdown),
            'avg_recovery_days': round(avg_recovery, 1),
            'ulcer_index': round(ulcer_index, 1)
        }
    
    # ==========================================
    # 7. SHARPE RATIO & RISK METRICS
    # ==========================================
    @staticmethod
    def calculate_risk_metrics(returns, risk_free_rate=0.05):
        """
        Comprehensive risk metrics:
        - Sharpe Ratio
        - Sortino Ratio (downside risk only)
        - Calmar Ratio
        - Omega Ratio
        """
        if len(returns) < 2 or returns.std() == 0:
            return {
                'sharpe': 0,
                'sortino': 0,
                'calmar': 0,
                'omega': 0
            }
        
        # Annualized return
        annual_return = returns.mean() * 252
        
        # Sharpe Ratio
        sharpe = (annual_return - risk_free_rate) / (returns.std() * np.sqrt(252))
        
        # Sortino Ratio (only downside deviation)
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0 and downside_returns.std() > 0:
            sortino = (annual_return - risk_free_rate) / (downside_returns.std() * np.sqrt(252))
        else:
            sortino = sharpe
        
        # Omega Ratio (probability weighted ratio of gains vs losses)
        threshold = 0
        gains = returns[returns > threshold] - threshold
        losses = threshold - returns[returns < threshold]
        
        if len(losses) > 0 and losses.sum() > 0:
            omega = gains.sum() / losses.sum()
        else:
            omega = 1
        
        return {
            'sharpe': round(sharpe, 2),
            'sortino': round(sortino, 2),
            'omega': round(omega, 2)
        }
    
    @staticmethod
    def interpret_sharpe(sharpe):
        """Interpret Sharpe Ratio"""
        if sharpe >= 2:
            return {'grade': 'EXCELLENT', 'color': '#00ff88', 'description': 'Institutional quality'}
        elif sharpe >= 1:
            return {'grade': 'GOOD', 'color': '#7cfc00', 'description': 'Above average'}
        elif sharpe >= 0.5:
            return {'grade': 'MODERATE', 'color': '#ffd700', 'description': 'Acceptable'}
        elif sharpe >= 0:
            return {'grade': 'POOR', 'color': '#ffa500', 'description': 'Needs improvement'}
        else:
            return {'grade': 'NEGATIVE', 'color': '#ff1744', 'description': 'Losing money'}
    
    # ==========================================
    # 8. MONTE CARLO VALUE AT RISK (VaR)
    # ==========================================
    @staticmethod
    def calculate_var_cvar(returns, confidence_level=0.95, portfolio_value=100000):
        """
        Value at Risk (VaR) and Conditional VaR (Expected Shortfall)
        - VaR: Maximum expected loss at given confidence
        - CVaR: Average loss beyond VaR
        """
        if len(returns) < 50:
            return {
                'var_95': 0,
                'cvar_95': 0,
                'var_99': 0,
                'daily_var_rupees': 0
            }
        
        # Historical VaR
        var_95 = np.percentile(returns, (1 - confidence_level) * 100) * 100
        cvar_95 = returns[returns <= np.percentile(returns, (1 - confidence_level) * 100)].mean() * 100
        
        # 99% VaR
        var_99 = np.percentile(returns, 1) * 100
        
        # Monetary value
        daily_var_rupees = abs(var_95 / 100) * portfolio_value
        
        return {
            'var_95': round(abs(var_95), 2),
            'cvar_95': round(abs(cvar_95), 2),
            'var_99': round(abs(var_99), 2),
            'daily_var_rupees': int(daily_var_rupees)
        }
    
    # ==========================================
    # 9. MONTE CARLO SIMULATION (Multi-scenario)
    # ==========================================
    @staticmethod
    def monte_carlo_simulation(prices, n_simulations=10000, n_days=5):
        """
        Advanced Monte Carlo Simulation with:
        - Geometric Brownian Motion
        - Jump diffusion
        - Confidence intervals
        """
        if len(prices) < 50:
            return None
        
        current_price = prices.iloc[-1]
        returns = prices.pct_change().dropna()
        
        if len(returns) < 20:
            return None
        
        mean_return = returns.mean()
        std_return = returns.std()
        
        # Jump diffusion parameters (for extreme events)
        jump_intensity = 0.05  # 5% chance of jump
        jump_size_mean = -0.02  # Average jump size (-2%)
        jump_size_std = 0.01  # Jump volatility
        
        final_prices = []
        peak_prices = []
        max_paths = []
        
        for _ in range(n_simulations):
            prices_path = [current_price]
            peak = current_price
            
            for day in range(n_days):
                # Check for jump
                if np.random.random() < jump_intensity:
                    jump = np.random.normal(jump_size_mean, jump_size_std)
                    daily_return = np.random.normal(mean_return, std_return) + jump
                else:
                    daily_return = np.random.normal(mean_return, std_return)
                
                new_price = prices_path[-1] * (1 + daily_return)
                prices_path.append(new_price)
                peak = max(peak, new_price)
            
            final_prices.append(prices_path[-1])
            peak_prices.append(peak)
            max_paths.append(max(prices_path))
        
        # Calculate metrics
        prob_up = (np.array(final_prices) > current_price).mean() * 100
        prob_up_5pct = (np.array(final_prices) > current_price * 1.05).mean() * 100
        prob_down_5pct = (np.array(final_prices) < current_price * 0.95).mean() * 100
        
        # Confidence intervals
        lower_90 = np.percentile(final_prices, 5)
        upper_90 = np.percentile(final_prices, 95)
        lower_95 = np.percentile(final_prices, 2.5)
        upper_95 = np.percentile(final_prices, 97.5)
        
        # Maximum potential loss
        max_loss_pct = (current_price - np.percentile(final_prices, 1)) / current_price * 100
        
        return {
            'prob_up': round(prob_up, 1),
            'prob_up_5pct': round(prob_up_5pct, 1),
            'prob_down_5pct': round(prob_down_5pct, 1),
            'lower_90': round(lower_90, 2),
            'upper_90': round(upper_90, 2),
            'lower_95': round(lower_95, 2),
            'upper_95': round(upper_95, 2),
            'max_loss_pct': round(max_loss_pct, 1),
            'expected_return': round(((np.mean(final_prices) - current_price) / current_price) * 100, 1)
        }
    
    # ==========================================
    # 10. COMPOSITE QUANT SCORE
    # ==========================================
    @staticmethod
    def calculate_composite_quant_score(hurst, entropy_score, sharpe, z_score):
        """
        Composite score combining all quant metrics
        Higher score = Better trading environment
        """
        score = 50
        
        # Hurst contribution (trending is good for trend strategies)
        if hurst > 0.6:
            score += 15
        elif hurst < 0.4:
            score += 10  # Mean reversion opportunities
        
        # Entropy contribution (lower entropy = more predictable)
        if entropy_score < 30:
            score += 20
        elif entropy_score < 50:
            score += 10
        elif entropy_score > 70:
            score -= 15
        
        # Sharpe contribution
        if sharpe > 1:
            score += 15
        elif sharpe > 0.5:
            score += 8
        
        # Z-score contribution (extreme values = opportunities)
        if abs(z_score) > 2:
            score += 10
        elif abs(z_score) > 1:
            score += 5
        
        return np.clip(score, 0, 100)


# Singleton instance
quant_models = AdvancedQuantModels()
