"""
TORO AI - MATHEMATICS-FIRST TRADING SYSTEM
Minimal indicators, maximum math
FULLY COMPATIBLE with app.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
from regime_models import market_regime_engine
from advanced_math import AdvancedQuantModels

# ==========================================
# ONLY 6 CORE INDICATORS (Plus compatibility columns)
# ==========================================

class SimplifiedIndicators:
    """Only essential indicators - rest is math"""
    
    @staticmethod
    def calculate_all(df):
        if df.empty or len(df) < 50:
            return df
        
        c = df["Close"]
        h = df["High"]
        l = df["Low"]
        v = df["Volume"]
        
        # 1. TREND (EMA 9,20,50,200 for compatibility)
        df["EMA_9"] = c.ewm(span=9, adjust=False).mean()
        df["EMA_20"] = c.ewm(span=20, adjust=False).mean()
        df["EMA_50"] = c.ewm(span=50, adjust=False).mean()
        df["EMA_200"] = c.ewm(span=200, adjust=False).mean()
        
        # 2. MOMENTUM (MACD with all components)
        exp1 = c.ewm(span=12, adjust=False).mean()
        exp2 = c.ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Histogram"] = df["MACD"] - df["Signal_Line"]
        
        # 3. VOLATILITY (ATR)
        tr1 = h - l
        tr2 = (h - c.shift()).abs()
        tr3 = (l - c.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df["ATR"] = tr.rolling(14).mean()
        
        # 4. MEAN REVERSION (RSI)
        delta = c.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # 5. VOLUME (Ratio and MA)
        df["Volume_MA"] = v.rolling(20).mean()
        df["Volume_Ratio"] = v / df["Volume_MA"]
        
        # 6. Bollinger Bands (for compatibility)
        df["BB_Middle"] = c.rolling(20).mean()
        bb_std = c.rolling(20).std()
        df["BB_Upper"] = df["BB_Middle"] + (bb_std * 2)
        df["BB_Lower"] = df["BB_Middle"] - (bb_std * 2)
        df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
        
        # 7. Support/Resistance (for compatibility)
        df["Support_20"] = l.rolling(20).min()
        df["Resistance_20"] = h.rolling(20).max()
        
        # 8. ADX (for compatibility)
        plus_dm = h.diff()
        minus_dm = l.diff()
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)
        atr_14 = tr.rolling(14).mean()
        plus_di = 100 * (plus_dm.rolling(14).mean() / atr_14)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr_14)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        df["ADX"] = dx.rolling(14).mean()
        
        # 9. Signal column (default 0)
        df["Signal"] = 0
        
        return df


# ==========================================
# MATHEMATICAL MODELS (The Real Power)
# ==========================================

class MathematicalModels:
    """Pure math - no indicators needed"""
    
    @staticmethod
    def calculate_expected_value(returns, win_rate, avg_win, avg_loss):
        """Expected value per trade"""
        return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.05):
        """Risk-adjusted returns"""
        if len(returns) < 2 or returns.std() == 0:
            return 0
        excess_returns = returns.mean() * 252 - risk_free_rate
        return excess_returns / (returns.std() * np.sqrt(252))
    
    @staticmethod
    def calculate_kelly_criterion(win_prob, win_loss_ratio):
        """Optimal position sizing"""
        if win_loss_ratio <= 0:
            return 0
        return (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio
    
    @staticmethod
    def calculate_z_score(price, mean, std):
        """Statistical distance from mean"""
        if std == 0:
            return 0
        return (price - mean) / std
    
    @staticmethod
    def calculate_monte_carlo_probability(data, n_simulations=10000):
        """Simple Monte Carlo probability"""
        if len(data) < 20:
            return 50
        
        returns = data['Close'].pct_change().dropna()
        if len(returns) < 10:
            return 50
        
        mean_return = returns.mean()
        std_return = returns.std()
        
        simulations = np.random.normal(mean_return, std_return, n_simulations)
        positive_sims = np.sum(simulations > 0)
        
        return (positive_sims / n_simulations) * 100


# ==========================================
# ADVANCED MARKET REGIME ENGINE
# ==========================================

class MarketRegimeEngine:
    """Advanced market regime detection with adaptive weights"""
    
    def __init__(self):
        # Regime-specific weights for different market conditions
        self.regime_weights = {
            "TRENDING_BULL": {
                "trend": 1.4,
                "momentum": 1.3,
                "mean_reversion": 0.5,
                "volume": 1.2,
                "volatility": 0.8
            },
            "TRENDING_BEAR": {
                "trend": 1.3,
                "momentum": 1.2,
                "mean_reversion": 0.6,
                "volume": 1.1,
                "volatility": 0.9
            },
            "SIDEWAYS": {
                "trend": 0.6,
                "momentum": 0.7,
                "mean_reversion": 1.5,
                "volume": 1.0,
                "volatility": 1.2
            },
            "HIGH_VOLATILITY": {
                "trend": 0.5,
                "momentum": 0.6,
                "mean_reversion": 1.2,
                "volume": 1.3,
                "volatility": 1.5  # Actually increase caution, but weight for filtering
            },
            "ACCUMULATION": {
                "trend": 1.2,
                "momentum": 1.1,
                "mean_reversion": 0.8,
                "volume": 1.4,
                "volatility": 0.7
            },
            "DISTRIBUTION": {
                "trend": 0.8,
                "momentum": 0.9,
                "mean_reversion": 1.1,
                "volume": 1.3,
                "volatility": 0.9
            }
        }
    
    def detect(self, df):
        """
        Detect current market regime
        Returns regime name and confidence
        """
        if df is None or df.empty or len(df) < 50:
            return {"regime": "UNKNOWN", "confidence": 50}
        
        latest = df.iloc[-1]
        
        # Get key indicators
        ema20 = latest.get('EMA_20', df['Close'].iloc[-1])
        ema50 = latest.get('EMA_50', df['Close'].iloc[-1])
        price = df['Close'].iloc[-1]
        
        # Calculate volatility
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) if len(returns) > 0 else 0.2
        
        # Calculate trend strength (using ADX or simple slope)
        if 'ADX' in df.columns:
            adx = df['ADX'].iloc[-1]
        else:
            # Simple slope calculation
            slope = (df['Close'].iloc[-1] - df['Close'].iloc[-20]) / df['Close'].iloc[-20] if len(df) >= 20 else 0
            adx = 25 + abs(slope * 100)  # Rough estimate
        
        # Calculate volume trend
        volume_ratio = latest.get('Volume_Ratio', 1.0)
        obv_trend = 0
        if 'OBV' in df.columns and len(df) >= 20:
            obv_trend = (df['OBV'].iloc[-1] - df['OBV'].iloc[-20]) / (df['OBV'].iloc[-20] + 1)
        
        # RSI for accumulation/distribution
        rsi = latest.get('RSI', 50)
        
        # Determine regime
        regime = "SIDEWAYS"
        confidence = 70
        
        # Check volatility first
        if volatility > 0.35:  # >35% annualized volatility
            regime = "HIGH_VOLATILITY"
            confidence = min(85, 70 + (volatility - 0.35) * 50)
        
        # Check trend direction with ADX
        elif adx > 30:
            if price > ema20 and ema20 > ema50:
                regime = "TRENDING_BULL"
                confidence = min(90, 70 + (adx - 30) * 1.5)
            elif price < ema20 and ema20 < ema50:
                regime = "TRENDING_BEAR"
                confidence = min(90, 70 + (adx - 30) * 1.5)
        
        # Check accumulation/distribution
        elif 40 <= rsi <= 60 and volume_ratio > 1.2 and obv_trend > 0:
            regime = "ACCUMULATION"
            confidence = 75
        elif rsi > 70 and volume_ratio > 1.5 and obv_trend < 0:
            regime = "DISTRIBUTION"
            confidence = 75
        
        # Default: sideways market
        else:
            regime = "SIDEWAYS"
            confidence = 65
        
        return {
            "regime": regime,
            "confidence": min(95, confidence),
            "adx": round(adx, 1),
            "volatility": round(volatility * 100, 1),
            "rsi": round(rsi, 1)
        }
    
    def get_regime_weights(self, regime):
        """Get adaptive weights for current regime"""
        if regime in self.regime_weights:
            return self.regime_weights[regime]
        # Default weights
        return {
            "trend": 1.0,
            "momentum": 1.0,
            "mean_reversion": 1.0,
            "volume": 1.0,
            "volatility": 1.0
        }


# ==========================================
# SIMPLIFIED TRADING LOGIC (Math-Based)
# ==========================================

class MathTradingEngine:
    """Adaptive quantitative trading engine"""
    
    def __init__(self):
        self.regime_engine = MarketRegimeEngine()
    
    # ==========================================
    # ADAPTIVE REGIME DETECTOR
    # ==========================================
    def detect_adaptive_regime(self, df):
        """Detect market regime with adaptive parameters"""
        
        if df is None or df.empty or len(df) < 50:
            return {
                "regime": "UNKNOWN",
                "confidence": 0,
                "risk_level": "HIGH",
                "strength": "WEAK",
                "volatility": 0
            }
        
        regime_data = self.regime_engine.detect(df)
        
        regime = regime_data.get("regime", "SIDEWAYS")
        confidence = regime_data.get("confidence", 70)
        
        # Risk level based on regime
        if regime in ["HIGH_VOLATILITY", "TRENDING_BEAR"]:
            risk_level = "HIGH"
        elif regime == "SIDEWAYS":
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Strength (as percentage)
        if confidence >= 80:
            strength = 90
        elif confidence >= 65:
            strength = 70
        elif confidence >= 50:
            strength = 50
        else:
            strength = 30
        
        # Calculate volatility
        returns = df['Close'].pct_change().dropna()
        volatility_value = (
            returns.std() * np.sqrt(252) * 100
            if len(returns) > 0 else 0
        )
        
        return {
            "regime": regime,
            "confidence": confidence,
            "risk_level": risk_level,
            "strength": strength,
            "volatility": round(volatility_value, 2)
        }
    
    # ==========================================
    # MAIN ANALYSIS ENGINE
    # ==========================================
    def analyze(self, df):
        """Main analysis with adaptive regime detection"""
        
        if df is None or df.empty or len(df) < 50:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        
        # ==========================================
        # ADAPTIVE MARKET REGIME
        # ==========================================
        
        regime_data = self.regime_engine.detect(df)
        regime = regime_data["regime"]
        
        weights = self.regime_engine.get_regime_weights(regime)
        
        trend_weight = weights["trend"]
        momentum_weight = weights["momentum"]
        mean_reversion_weight = weights["mean_reversion"]
        volume_weight = weights["volume"]
        volatility_weight = weights["volatility"]
        
        # ==========================================
        # INITIAL SCORE
        # ==========================================
        
        score = 50
        reasons = []
        
        reasons.append(f"Regime: {regime} ({regime_data['confidence']:.0f}%)")
        
        # ==========================================
        # MATH MODEL 1:
        # MEAN REVERSION
        # ==========================================
        
        z_score = MathematicalModels.calculate_z_score(
            latest['Close'],
            df['Close'].tail(20).mean(),
            df['Close'].tail(20).std()
        )
        
        if z_score < -2:
            boost = 20 * mean_reversion_weight
            score += boost
            reasons.append(f"Statistical overshoot (z={z_score:.2f}) +{boost:.0f}")
        
        elif z_score < -1:
            boost = 10 * mean_reversion_weight
            score += boost
            reasons.append(f"Below mean (z={z_score:.2f}) +{boost:.0f}")
        
        elif z_score > 2:
            penalty = 20 * mean_reversion_weight
            score -= penalty
            reasons.append(f"Statistical overbought (z={z_score:.2f}) -{penalty:.0f}")
        
        # ==========================================
        # MATH MODEL 2:
        # TREND ANALYSIS
        # ==========================================
        
        ema_diff = (
            latest['EMA_20'] - latest['EMA_50']
        ) / latest['EMA_50']
        
        if ema_diff > 0.02:
            boost = 15 * trend_weight
            score += boost
            reasons.append(f"Strong trend momentum +{boost:.0f}")
        
        elif ema_diff < -0.02:
            penalty = 15 * trend_weight
            score -= penalty
            reasons.append(f"Strong downtrend -{penalty:.0f}")
        
        # ==========================================
        # MATH MODEL 3:
        # MOMENTUM ANALYSIS
        # ==========================================
        
        macd_strength = abs(
            latest['MACD']
        ) / latest['Close']
        
        if macd_strength > 0.01 and latest['MACD'] > 0:
            boost = 12 * momentum_weight
            score += boost
            reasons.append(f"Positive momentum +{boost:.0f}")
        
        elif macd_strength > 0.01 and latest['MACD'] < 0:
            penalty = 12 * momentum_weight
            score -= penalty
            reasons.append(f"Negative momentum -{penalty:.0f}")
        
        # ==========================================
        # MATH MODEL 4:
        # VOLUME CONFIRMATION
        # ==========================================
        
        if latest['Volume_Ratio'] > 1.5:
            if score > 50:
                boost = 10 * volume_weight
                score += boost
                reasons.append(f"Volume confirmation +{boost:.0f}")
            else:
                penalty = 10 * volume_weight
                score -= penalty
                reasons.append(f"Volume sell pressure -{penalty:.0f}")
        
        # ==========================================
        # MATH MODEL 5:
        # VOLATILITY FILTER
        # ==========================================
        
        vol_percent = (
            latest['ATR'] / latest['Close']
        )
        
        if vol_percent > 0.03:
            penalty = 5 * volatility_weight
            score -= penalty
            reasons.append(f"High volatility ({vol_percent:.1%}) -{penalty:.0f}")
        
        # ==========================================
        # REGIME-SPECIFIC ADJUSTMENTS
        # ==========================================
        
        if regime == "TRENDING_BULL":
            score += 5
            reasons.append("Bull regime boost +5")
        
        elif regime == "TRENDING_BEAR":
            score -= 5
            reasons.append("Bear regime penalty -5")
        
        elif regime == "SIDEWAYS":
            if abs(z_score) > 1:
                score += 5
                reasons.append("Mean reversion favorable +5")
        
        elif regime == "HIGH_VOLATILITY":
            score -= 8
            reasons.append("Defensive mode active -8")
        
        elif regime == "ACCUMULATION":
            score += 3
            reasons.append("Accumulation detected +3")
        
        # ==========================================
        # SCORE NORMALIZATION
        # ==========================================
        
        adjusted_score = (
            (score - 50) * 0.7
        ) + 50
        
        adjusted_score = max(
            5,
            min(adjusted_score, 95)
        )
        
        # ==========================================
        # FINAL SIGNAL
        # ==========================================
        
        if adjusted_score >= 65:
            return (
                1,
                round(adjusted_score, 1),
                reasons[:5]  # Limit to 5 reasons for display
            )
        
        elif adjusted_score <= 35:
            bearish_confidence = 100 - adjusted_score
            return (
                -1,
                round(bearish_confidence, 1),
                reasons[:5]
            )
        
        else:
            return (
                0,
                round(adjusted_score, 1),
                reasons[:5]
            )

# ==========================================
# RISK MANAGEMENT (Pure Math)
# ==========================================

class MathRiskManager:
    """Mathematical position sizing"""
    
    def calculate_position_size(self, df, account_size=100000):
        if df.empty or len(df) < 20:
            return {
                'entry': 0, 'stoploss': 0, 'target': 0, 
                'position_size': 0, 'risk_reward': 0, 
                'risk_amount': 0, 'reward_amount': 0,
                'volatility': 'NORMAL', 'kelly_fraction': 0
            }
        
        current_price = df["Close"].iloc[-1]
        atr = df["ATR"].iloc[-1]
        returns = df['Close'].pct_change().dropna()
        
        # Kelly Criterion for optimal sizing
        win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0.5
        avg_win = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0.02
        avg_loss = abs(returns[returns < 0].mean()) if len(returns[returns < 0]) > 0 else 0.01
        
        win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 1
        kelly = MathematicalModels.calculate_kelly_criterion(win_rate, win_loss_ratio)
        
        # Conservative Kelly (use 25% of Kelly)
        risk_percent = max(0.5, min(5, kelly * 0.25 * 100))
        
        # Position size based on ATR
        stop_distance = atr * 1.5
        position_size = (account_size * risk_percent / 100) / stop_distance if stop_distance > 0 else 0
        
        # Fibonacci levels for compatibility
        recent_high = df["High"].tail(50).max()
        recent_low = df["Low"].tail(50).min()
        fib_range = recent_high - recent_low
        
        return {
            'entry': round(current_price, 2),
            'stoploss': round(current_price - stop_distance, 2),
            'target': round(current_price + (stop_distance * 2), 2),
            'position_size': round(position_size, 0),
            'risk_reward': round(2.0, 2),  # Fixed 2:1 ratio
            'risk_amount': round(stop_distance, 2),
            'reward_amount': round(stop_distance * 2, 2),
            'volatility': 'HIGH' if (atr / current_price) > 0.03 else 'LOW' if (atr / current_price) < 0.01 else 'NORMAL',
            'kelly_fraction': round(kelly, 2),
            'fib_382': round(recent_high - fib_range * 0.382, 2),
            'fib_500': round(recent_high - fib_range * 0.5, 2),
            'fib_618': round(recent_high - fib_range * 0.618, 2)
        }


# ==========================================
# MARKET REGIME DETECTOR
# ==========================================

class MarketRegimeDetector:
    """Simple market regime detection"""
    
    def detect(self, df):
        if df.empty or len(df) < 50:
            return "UNKNOWN"
        
        ema20 = df['EMA_20'].iloc[-1] if 'EMA_20' in df.columns else df['Close'].iloc[-1]
        ema50 = df['EMA_50'].iloc[-1] if 'EMA_50' in df.columns else df['Close'].iloc[-1]
        
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) if len(returns) > 0 else 0
        
        if volatility > 0.3:
            return "HIGH_VOLATILITY"
        elif ema20 > ema50:
            return "BULL_TRENDING"
        elif ema20 < ema50:
            return "BEAR_FALLING"
        else:
            return "SIDEWAYS_RANGING"



# ==========================================
# ULTIMATE MATH BRAIN (FULLY COMPATIBLE)
# ==========================================

class UltimateMathBrain:
    """Pure math - minimal indicators - FULLY COMPATIBLE with app.py"""
    
    def __init__(self):
        self.indicators = SimplifiedIndicators()
        self.trading_engine = MathTradingEngine()
        self.risk_manager = MathRiskManager()
        self.regime_detector = MarketRegimeDetector()
        
        # NEW ADAPTIVE QUANT ENGINE
        self.math_engine = MathTradingEngine()
        
        # ==========================================
        # QUANT MODELS INITIALIZATION
        # ==========================================
        self.quant_models = AdvancedQuantModels()  
    
    # ==========================================
    # QUANTITATIVE ANALYSIS METHODS
    # ==========================================
    
    def get_quant_analysis(self, df):
        """
        Complete quantitative analysis for a stock
        Returns all advanced quant metrics
        """
        if df is None or df.empty or len(df) < 50:
            return {
                'error': 'Insufficient data for quant analysis',
                'hurst': {'value': 0.5, 'regime': 'UNKNOWN'},
                'entropy': {'score': 50, 'regime': 'UNKNOWN'},
                'z_score': {'value': 0, 'signal': 'NEUTRAL'},
                'bayesian': {'up_probability': 50, 'info_gain': 0},
                'risk_metrics': {'sharpe': 0, 'sortino': 0, 'omega': 0},
                'drawdown': {'max_drawdown': 0, 'current_drawdown': 0},
                'var': {'var_95': 0, 'daily_var_rupees': 0},
                'monte_carlo': None,
                'composite_score': 50
            }
        
        prices = df['Close']
        returns = prices.pct_change().dropna()
        
        # 1. Hurst Exponent
        hurst = self.quant_models.calculate_hurst_exponent(prices.values[-100:])
        hurst_interpret = self.quant_models.interpret_hurst(hurst)
        
        # 2. Shannon Entropy
        entropy_score, raw_entropy = self.quant_models.calculate_shannon_entropy(returns)
        entropy_interpret = self.quant_models.interpret_entropy(entropy_score)
        
        # 3. Bayesian Probability
        bayesian_prob, info_gain = self.quant_models.calculate_bayesian_up_probability(returns)
        
        # 4. Z-Score
        z_scores = self.quant_models.calculate_z_score(prices)
        current_z = z_scores.iloc[-1] if len(z_scores) > 0 else 0
        z_interpret = self.quant_models.interpret_z_score(current_z)
        
        # 5. Risk Metrics
        risk_metrics = self.quant_models.calculate_risk_metrics(returns)
        
        # 6. Drawdown Metrics
        drawdown = self.quant_models.calculate_drawdown_metrics(prices.values)
        
        # 7. Value at Risk
        var = self.quant_models.calculate_var_cvar(returns)
        
        # 8. Monte Carlo Simulation
        monte_carlo = self.quant_models.monte_carlo_simulation(prices)
        
        # 9. Composite Score
        composite_score = self.quant_models.calculate_composite_quant_score(
            hurst, entropy_score, risk_metrics['sharpe'], current_z
        )
        
        return {
            'hurst': {
                'value': round(hurst, 3),
                'regime': hurst_interpret['regime'],
                'color': hurst_interpret['color'],
                'icon': hurst_interpret['icon'],
                'action': hurst_interpret['action'],
                'confidence': hurst_interpret['confidence']
            },
            'entropy': {
                'score': round(entropy_score, 1),
                'regime': entropy_interpret['regime'],
                'color': entropy_interpret['color'],
                'icon': entropy_interpret['icon'],
                'action': entropy_interpret['action'],
                'risk': entropy_interpret['risk']
            },
            'z_score': {
                'value': round(current_z, 2),
                'signal': z_interpret['signal'],
                'color': z_interpret['color'],
                'icon': z_interpret['icon'],
                'action': z_interpret['action'],
                'confidence': z_interpret['confidence']
            },
            'bayesian': {
                'up_probability': round(bayesian_prob, 1),
                'info_gain': round(info_gain, 1),
                'bias': 'BULLISH' if bayesian_prob >= 60 else 'BEARISH' if bayesian_prob <= 40 else 'NEUTRAL'
            },
            'risk_metrics': {
                'sharpe': risk_metrics['sharpe'],
                'sharpe_grade': self.quant_models.interpret_sharpe(risk_metrics['sharpe'])['grade'],
                'sharpe_color': self.quant_models.interpret_sharpe(risk_metrics['sharpe'])['color'],
                'sortino': risk_metrics['sortino'],
                'omega': risk_metrics['omega']
            },
            'drawdown': {
                'max_drawdown': round(drawdown['max_drawdown'], 1),
                'current_drawdown': round(drawdown['current_drawdown'], 1),
                'avg_recovery_days': drawdown['avg_recovery_days'],
                'ulcer_index': drawdown['ulcer_index']
            },
            'var': {
                'var_95': var['var_95'],
                'cvar_95': var['cvar_95'],
                'var_99': var['var_99'],
                'daily_var_rupees': var['daily_var_rupees']
            },
            'monte_carlo': monte_carlo,
            'composite_score': round(composite_score, 1)
        }
    
    
    
    
    def calculate_all_indicators(self, df):
        """Calculate only essential indicators"""
        if df is None:
            return pd.DataFrame()
        return self.indicators.calculate_all(df)
    
    
    def generate_smart_signals(self, df):
        """Math-based signals - returns 6 values expected by app.py"""
        if df is None or df.empty:
            return pd.DataFrame(), pd.DataFrame(), 50, "NEUTRAL", 50, 30
        
        signal, confidence, reasons = self.trading_engine.analyze(df)
        
        buy_signals = pd.DataFrame()
        sell_signals = pd.DataFrame()
        
        if signal == 1:
            buy_signals = pd.DataFrame([{
                'index': df.index[-1],
                'Close': df['Close'].iloc[-1],
                'Score': confidence,
                'Confidence': 'HIGH' if confidence >= 70 else 'MEDIUM',
                'Reasons': reasons
            }])
            buy_signals.set_index("index", inplace=True)
        
        elif signal == -1:
            sell_signals = pd.DataFrame([{
                'index': df.index[-1],
                'Close': df['Close'].iloc[-1],
                'Score': confidence,
                'Confidence': 'HIGH' if confidence >= 70 else 'MEDIUM',
                'Reasons': reasons
            }])
            sell_signals.set_index("index", inplace=True)
        
        overall_sentiment = "BULLISH" if signal == 1 else "BEARISH" if signal == -1 else "NEUTRAL"
        risk_score = 30
        
        return buy_signals, sell_signals, confidence, overall_sentiment, confidence, risk_score
    
    
    def get_signal_from_brain(self, df, levels=None):
        """
        Backtest-compatible signal generator
        Returns:
            1  = BUY
            -1 = SELL
            0  = HOLD
        """

        if df is None or df.empty or len(df) < 50:
            return 0

        try:
            signal, confidence, reasons = self.trading_engine.analyze(df)

            # Strong signal filtering
            if confidence >= 65:
                return signal

            return 0

        except Exception:
            return 0
    
    
    
    def calculate_advanced_risk_levels(self, df, account_size=100000):
        """Math-based risk management"""
        if df is None or df.empty:
            return {}
        return self.risk_manager.calculate_position_size(df, account_size)
    
    
    def generate_actionable_insights(self, df, levels, buy_signals, sell_signals):
        """Math-based insights"""
        insights = []
        
        if df is None or df.empty or len(df) < 20:
            return ["Calculating mathematical probabilities..."]
        
        latest = df.iloc[-1]
        returns = df['Close'].pct_change().tail(50).dropna()
        
        mc_prob = MathematicalModels.calculate_monte_carlo_probability(df)
        sharpe = MathematicalModels.calculate_sharpe_ratio(returns)
        win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0.5
        expected_return = returns.mean() * 252 if len(returns) > 0 else 0
        
        insights.append(f"📊 **Monte Carlo Win Probability**: {mc_prob:.0f}%")
        insights.append(f"📈 **Sharpe Ratio**: {sharpe:.2f}")
        insights.append(f"💰 **Expected Annual Return**: {expected_return:.1%}")
        
        rsi = latest.get('RSI', 50)
        if rsi < 30:
            insights.append(f"🟢 **Oversold** - RSI at {rsi:.0f}")
        elif rsi > 70:
            insights.append(f"🔴 **Overbought** - RSI at {rsi:.0f}")
        
        if levels:
            insights.append(f"💰 **Position**: {levels.get('position_size', 0):.0f} shares")
            insights.append(f"🎯 **Target**: ₹{levels.get('target', 0):.2f}")
        
        return insights[:6]
    
    #==========================================
    # ENSEMBLE ANALYSIS (FIXED)
    #==========================================
    def get_ensemble_analysis(self, df, levels=None):
        """Ensemble analysis for compatibility"""
        # Handle None case
        if df is None:
            # Return default values without analyzing
            return {
                'signal': 0,
                'confidence': 50,
                'action': 'HOLD',
                'vote_summary': 'Waiting for data',
                'strategy_results': []
            }
        
        signal, confidence, reasons = self.trading_engine.analyze(df)
        
        if signal == 1:
            action = "STRONG_BUY" if confidence >= 75 else "BUY"
        elif signal == -1:
            action = "STRONG_SELL" if confidence >= 75 else "SELL"
        else:
            action = "HOLD"
        
        strategy_results = [
            {'name': 'Math Engine', 'signal': signal, 'confidence': confidence, 'reasons': reasons[:2]}
        ]
        
        return {
            'signal': signal,
            'confidence': confidence,
            'action': action,
            'vote_summary': f"Confidence: {confidence:.0f}%",
            'strategy_results': strategy_results
        }
    
    
    #==========================================
        # TRADING RECOMMENDATION (FIXED)
    #==========================================    
    def get_trading_recommendation(self, overall_sentiment, confidence, risk_score, levels):
        """Get trading recommendation - FIXED: No None passed to get_ensemble_analysis"""
        if not levels:
            return "HOLD", 50
        
        # Determine signal from sentiment instead of calling get_ensemble_analysis with None
        signal = 0
        
        # Try to determine signal from sentiment
        sentiment_str = str(overall_sentiment).upper()
        if "BUY" in sentiment_str:
            signal = 1
        elif "SELL" in sentiment_str or "BEARISH" in sentiment_str:
            signal = -1
        
        # Also check confidence level
        if confidence >= 70 and signal == 1:
            signal = 1
        elif confidence >= 70 and signal == -1:
            signal = -1
        
        rr = levels.get('risk_reward', 0)
        
        if signal == 1 and risk_score < 50:
            if rr >= 1.5:
                return "BUY", min(confidence, 85)
            elif rr >= 1:
                return "BUY", min(confidence, 70)
            else:
                return "CONSIDER", 60
        elif signal == -1:
            return "AVOID", confidence
        elif "BULLISH" in sentiment_str and risk_score < 50:
            return "CONSIDER", 60
        else:
            return "HOLD", 50
    
    
    #=======================================  
    # MUTI-TIMEFRAME ANALYSIS 
    #=========================================
    def get_multi_timeframe_analysis(self, data_dict):
        """
        PROFESSIONAL MULTI-TIMEFRAME ANALYSIS
        """

        if not data_dict:
            return {
                'final_action': 'HOLD',
                'action_color': '#ffd700',
                'agreement': '0/3',
                'final_score': 50,
                'timeframes': {}
            }

        results = {}

        # ==========================================
        # ANALYZE EACH TIMEFRAME
        # ==========================================

        for timeframe, df in data_dict.items():

            if df is None or df.empty or len(df) < 50:
                results[timeframe] = {
                    'direction': 'NEUTRAL',
                    'symbol': '🟡',
                    'confidence': 25,
                    'score': 0,
                    'reasons': ['Insufficient data']
                }
                continue

            latest = df.iloc[-1]

            score = 0
            reasons = []

            # ==========================================
            # TREND ANALYSIS
            # ==========================================

            ema20 = latest.get("EMA_20", latest["Close"])
            ema50 = latest.get("EMA_50", latest["Close"])
            ema200 = latest.get("EMA_200", latest["Close"])
            price = latest["Close"]

            if price > ema20 > ema50 > ema200:
                score += 40
                reasons.append("Strong bullish trend")

            elif price > ema20 > ema50:
                score += 25
                reasons.append("Bullish momentum")

            elif price < ema20 < ema50 < ema200:
                score -= 40
                reasons.append("Strong bearish trend")

            elif price < ema20 < ema50:
                score -= 25
                reasons.append("Bearish momentum")

            # ==========================================
            # RSI
            # ==========================================

            rsi = latest.get("RSI", 50)

            if 55 <= rsi <= 70:
                score += 15
                reasons.append("Healthy bullish RSI")

            elif rsi > 75:
                score -= 10
                reasons.append("Overbought")

            elif 30 <= rsi <= 45:
                score -= 15
                reasons.append("Weak momentum")

            elif rsi < 25:
                score += 10
                reasons.append("Oversold bounce")

            # ==========================================
            # MACD
            # ==========================================

            macd = latest.get("MACD", 0)
            signal = latest.get("Signal_Line", 0)

            if macd > signal:
                score += 15
                reasons.append("MACD bullish")

            elif macd < signal:
                score -= 15
                reasons.append("MACD bearish")

            # ==========================================
            # VOLUME
            # ==========================================

            vol_ratio = latest.get("Volume_Ratio", 1)

            if vol_ratio > 1.5:

                if score > 0:
                    score += 10
                    reasons.append("Strong buying volume")

                else:
                    score -= 10
                    reasons.append("Strong selling volume")

            # ==========================================
            # VOLATILITY
            # ==========================================

            atr = latest.get("ATR", 0)

            if price > 0:

                volatility = atr / price

                if volatility > 0.04:
                    score -= 5
                    reasons.append("High volatility")

            # ==========================================
            # FINAL TIMEFRAME RESULT
            # ==========================================

            confidence = min(max(abs(score), 40), 95)

            if score >= 35:

                direction = "BULLISH"
                symbol = "🟢"

            elif score <= -35:

                direction = "BEARISH"
                symbol = "🔴"

            else:

                direction = "NEUTRAL"
                symbol = "🟡"

            results[timeframe] = {
                'direction': direction,
                'symbol': symbol,
                'confidence': confidence,
                'score': score,
                'reasons': reasons[:3]
            }

        # ==========================================
        # FINAL ANALYSIS
        # ==========================================

        bullish_count = sum(
            1 for tf in results.values()
            if tf['direction'] == 'BULLISH'
        )

        bearish_count = sum(
            1 for tf in results.values()
            if tf['direction'] == 'BEARISH'
        )

        avg_confidence = np.mean([
            tf['confidence'] for tf in results.values()
        ])

        weekly_score = results.get('Weekly', {}).get('score', 0) * 0.50
        daily_score = results.get('Daily', {}).get('score', 0) * 0.35
        hourly_score = results.get('Hourly', {}).get('score', 0) * 0.15

        total_score = weekly_score + daily_score + hourly_score

        # ==========================================
        # FINAL ACTION
        # ==========================================

        if bullish_count >= 2 and total_score > 20:

            final_action = (
                "STRONG BUY"
                if avg_confidence >= 75
                else "BUY"
            )

            action_color = "#00ff88"

        elif bearish_count >= 2 and total_score < -20:

            final_action = (
                "STRONG SELL"
                if avg_confidence >= 75
                else "SELL"
            )

            action_color = "#ff1744"

        else:

            final_action = "HOLD"
            action_color = "#ffd700"

        # ==========================================
        # AGREEMENT
        # ==========================================

        if bullish_count == 3 or bearish_count == 3:

            agreement = "3/3"

        elif bullish_count == 2 or bearish_count == 2:

            agreement = "2/3"

        else:

            agreement = "Mixed"

        return {
            'final_action': final_action,
            'action_color': action_color,
            'agreement': agreement,
            'final_score': round(avg_confidence, 1),
            'timeframes': results
        }
      
      
      
    #==========================================
    # QUANTITATIVE METRICS FOR COMPATIBILITY
    #==========================================   
    def calculate_quantitative_metrics(self, df, levels):
        """Quantitative metrics for compatibility"""
        if df is None or df.empty or len(df) < 50:
            return {
                'win_probability': 50,
                'expected_value': 0,
                'sample_size': 0,
                'verdict': 'NEUTRAL',
                'message': 'Need more data'
            }
        
        returns = df['Close'].pct_change().dropna()
        win_rate = len(returns[returns > 0]) / len(returns) if len(returns) > 0 else 0.5
        avg_win = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0.02
        avg_loss = abs(returns[returns < 0].mean()) if len(returns[returns < 0]) > 0 else 0.01
        
        expected_value = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
        
        if win_rate >= 0.6:
            verdict = "STRONG BUY"
            message = "High probability setup"
        elif win_rate >= 0.55:
            verdict = "BUY"
            message = "Good probability"
        elif win_rate >= 0.45:
            verdict = "CONSIDER"
            message = "Wait for confirmation"
        else:
            verdict = "AVOID"
            message = "Poor risk-reward"
        
        return {
            'win_probability': round(win_rate * 100, 1),
            'expected_value': round(expected_value * 100, 2),
            'sample_size': len(returns),
            'verdict': verdict,
            'message': message
        }
    
    # ==========================================
    # MONTE CARLO SIMULATION (PROFESSIONAL VERSION)
    # ==========================================
    def run_monte_carlo_simulation(self, df, current_price, target, stoploss):

        if df is None or df.empty or len(df) < 100:
            return None

        returns = df['Close'].pct_change().dropna()

        if len(returns) < 30:
            return None

        mean_return = returns.mean()
        std_return = returns.std()

        n_simulations = 5000
        n_days = 30

        target_hits = 0
        stop_hits = 0

        final_prices = []

        for _ in range(n_simulations):

            simulated_price = current_price

            hit_target = False
            hit_stop = False

            for _ in range(n_days):

                daily_return = np.random.normal(
                    mean_return,
                    std_return
                )

                simulated_price *= (1 + daily_return)

                # TARGET HIT
                if simulated_price >= target:
                    target_hits += 1
                    hit_target = True
                    break

                # STOPLOSS HIT
                if simulated_price <= stoploss:
                    stop_hits += 1
                    hit_stop = True
                    break

            final_prices.append(simulated_price)

        prob_target = (target_hits / n_simulations) * 100
        prob_stop = (stop_hits / n_simulations) * 100

        expected_return = (
            (np.mean(final_prices) - current_price)
            / current_price
        ) * 100

        sharpe = (
            returns.mean() / returns.std() * np.sqrt(252)
            if returns.std() > 0 else 0
        )

        return {
            'prob_target': round(prob_target, 1),
            'prob_stoploss': round(prob_stop, 1),
            'mean_return': round(expected_return, 1),
            'sharpe': round(sharpe, 2),
            'n_paths': n_simulations,
            'price_percentiles': {
                'p95': round(np.percentile(final_prices, 95), 2),
                'p50': round(np.percentile(final_prices, 50), 2),
                'p5': round(np.percentile(final_prices, 5), 2),
            }
        }

# ==========================================
# SINGLETON INSTANCE
# ==========================================
ultimate_brain = UltimateMathBrain()
