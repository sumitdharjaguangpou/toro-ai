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