# brain_ultimate.py - The Ultimate Trading Intelligence System
# Merged: brain.py + brain_v2.py + brain_aggressive.py
# Optimized for maximum performance

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

# ==========================================
# PART 1: KALMAN FILTER (Noise Reduction)
# ==========================================

class KalmanFilter:
    """Advanced noise reduction for cleaner signals"""
    
    def __init__(self, process_variance=1e-3, measurement_variance=1e-2):
        self.q = process_variance
        self.r = measurement_variance
        self.p = 1.0
        self.k = 0.0
        self.x = None
        self.initialized = False
    
    def filter(self, measurement):
        if not self.initialized:
            self.x = measurement
            self.initialized = True
            return measurement
        
        self.p = self.p + self.q
        self.k = self.p / (self.p + self.r)
        self.x = self.x + self.k * (measurement - self.x)
        self.p = (1 - self.k) * self.p
        return self.x
    
    def filter_series(self, series):
        filtered = []
        for value in series:
            filtered.append(self.filter(value))
        return filtered


# ==========================================
# PART 2: INDICATORS ENGINE (41+ Indicators)
# ==========================================

class IndicatorsEngine:
    """Calculates all technical indicators"""
    
    @staticmethod
    def calculate_all(df):
        if df.empty or len(df) < 50:
            return df
        
        c = df["Close"]
        h = df["High"]
        l = df["Low"]
        v = df["Volume"]
        
        # TREND INDICATORS
        df["EMA_9"] = c.ewm(span=9, adjust=False).mean()
        df["EMA_20"] = c.ewm(span=20, adjust=False).mean()
        df["EMA_50"] = c.ewm(span=50, adjust=False).mean()
        df["EMA_200"] = c.ewm(span=200, adjust=False).mean()
        
        # RSI
        delta = c.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = c.ewm(span=12, adjust=False).mean()
        exp2 = c.ewm(span=26, adjust=False).mean()
        df["MACD"] = exp1 - exp2
        df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_Histogram"] = df["MACD"] - df["Signal_Line"]
        
        # ATR
        tr1 = h - l
        tr2 = (h - c.shift()).abs()
        tr3 = (l - c.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df["ATR"] = tr.rolling(14).mean()
        
        # Bollinger Bands - FIXED SECTION
        # Bollinger Bands
        df["BB_Middle"] = df["Close"].rolling(20).mean()
        bb_std = df["Close"].rolling(20).std()
        df["BB_Upper"] = df["BB_Middle"] + (bb_std * 2)
        df["BB_Lower"] = df["BB_Middle"] - (bb_std * 2)
        df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
                
        # ADX
        plus_dm = h.diff()
        minus_dm = l.diff()
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)
        atr_14 = tr.rolling(14).mean()
        plus_di = 100 * (plus_dm.rolling(14).mean() / atr_14)
        minus_di = 100 * (minus_dm.rolling(14).mean() / atr_14)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        df["ADX"] = dx.rolling(14).mean()
        
        # Volume Indicators
        df["Volume_MA"] = v.rolling(20).mean()
        df["Volume_Ratio"] = v / df["Volume_MA"]
        
        # OBV
        obv = [0]
        for i in range(1, len(df)):
            if c.iloc[i] > c.iloc[i-1]:
                obv.append(obv[-1] + v.iloc[i])
            elif c.iloc[i] < c.iloc[i-1]:
                obv.append(obv[-1] - v.iloc[i])
            else:
                obv.append(obv[-1])
        df["OBV"] = obv
        df["OBV_Trend"] = df["OBV"].rolling(20).mean()
        
        # Support/Resistance
        df["Resistance_20"] = h.rolling(20).max()
        df["Support_20"] = l.rolling(20).min()
        df["Pivot"] = (h + l + c) / 3
        df["R1"] = (2 * df["Pivot"]) - l
        df["S1"] = (2 * df["Pivot"]) - h
        
        return df

# ==========================================
# PART 3: SIX POWERFUL STRATEGIES
# ==========================================

class StrategyMomentumBreakout:
    """Catches stocks breaking to new highs with volume"""
    
    def analyze(self, df):
        if len(df) < 50:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        reasons = []
        confidence = 50
        
        year_high = df['High'].tail(252).max()
        if latest['Close'] >= year_high * 0.98:
            confidence += 20
            reasons.append(f"Near 52-week high: {year_high:.2f}")
        
        volume_ratio = latest.get('Volume_Ratio', 1)
        if volume_ratio > 1.5:
            confidence += 15
            reasons.append(f"Volume surge: {volume_ratio:.1f}x")
        
        adx = latest.get('ADX', 20)
        if adx > 30:
            confidence += 15
            reasons.append(f"Strong trend: ADX {adx:.0f}")
        
        if confidence >= 70:
            return 1, min(confidence, 90), reasons
        return 0, confidence, reasons


class StrategyPullbackSnap:
    """Buys dips within strong uptrends"""
    
    def analyze(self, df):
        if len(df) < 50:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        reasons = []
        confidence = 50
        
        ema20 = latest.get('EMA_20', 0)
        ema50 = latest.get('EMA_50', 0)
        price = latest['Close']
        
        if price > ema20 > ema50:
            confidence += 20
            reasons.append("Uptrend intact")
        else:
            return 0, confidence, ["Not in uptrend"]
        
        rsi = latest.get('RSI', 50)
        prev_rsi = prev.get('RSI', 50)
        
        if 30 < rsi < 60 and prev_rsi > rsi:
            confidence += 15
            reasons.append(f"RSI cooling: {prev_rsi:.0f} to {rsi:.0f}")
        
        if price <= ema20 * 1.02:
            confidence += 15
            reasons.append("Price near EMA20 support")
        
        volume_ratio = latest.get('Volume_Ratio', 1)
        if volume_ratio < 0.8:
            confidence += 10
            reasons.append("Low volume pullback - healthy")
        
        if confidence >= 70:
            return 1, min(confidence, 90), reasons
        return 0, confidence, reasons


class StrategyVWAPReversal:
    """Trades extreme oversold/overbought conditions"""
    
    def analyze(self, df):
        if len(df) < 20:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        reasons = []
        confidence = 50
        
        rsi = latest.get('RSI', 50)
        
        if rsi < 25:
            confidence += 35
            reasons.append(f"Extreme oversold: RSI {rsi:.0f}")
            
            bb_lower = latest.get('BB_Lower', 0)
            if bb_lower > 0 and latest['Close'] <= bb_lower * 1.02:
                confidence += 15
                reasons.append("Price at lower Bollinger Band")
            
            return 1, min(confidence, 85), reasons
        
        elif rsi > 75:
            confidence += 35
            reasons.append(f"Extreme overbought: RSI {rsi:.0f}")
            
            bb_upper = latest.get('BB_Upper', 0)
            if bb_upper > 0 and latest['Close'] >= bb_upper * 0.98:
                confidence += 15
                reasons.append("Price at upper Bollinger Band")
            
            return -1, min(confidence, 85), reasons
        
        return 0, confidence, ["No extreme condition"]


class StrategyTrendReversal:
    """Catches early trend reversals"""
    
    def analyze(self, df):
        if len(df) < 30:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        reasons = []
        confidence = 50
        
        macd = latest.get('MACD', 0)
        prev_macd = prev.get('MACD', 0)
        signal = latest.get('Signal_Line', 0)
        prev_signal = prev.get('Signal_Line', 0)
        
        if macd > signal and prev_macd <= prev_signal:
            confidence += 25
            reasons.append("MACD bullish crossover")
        elif macd > signal:
            confidence += 10
            reasons.append("MACD above signal line")
        
        rsi = latest.get('RSI', 50)
        prev_rsi = prev.get('RSI', 50)
        
        if prev_rsi < 50 < rsi:
            confidence += 20
            reasons.append(f"RSI crossed above 50")
        
        ema20 = latest.get('EMA_20', 0)
        if latest['Close'] > ema20:
            confidence += 10
            reasons.append("Price above EMA20")
        
        if confidence >= 70:
            return 1, min(confidence, 85), reasons
        return 0, confidence, reasons


class StrategyVolatilityExpansion:
    """Catches explosive moves after low volatility"""
    
    def analyze(self, df):
        if len(df) < 20:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        reasons = []
        confidence = 50
        
        bb_width = latest.get('BB_Width', 0.1)
        bb_width_20 = df['BB_Width'].rolling(20).mean().iloc[-1] if 'BB_Width' in df.columns else 0.1
        
        if bb_width < bb_width_20 * 0.8:
            confidence += 25
            reasons.append(f"Bollinger squeeze detected")
        
        volume_ratio = latest.get('Volume_Ratio', 1)
        if volume_ratio > 1.5:
            confidence += 15
            reasons.append(f"Volume expansion: {volume_ratio:.1f}x")
        
        bb_upper = latest.get('BB_Upper', 0)
        bb_lower = latest.get('BB_Lower', 0)
        
        if bb_upper > 0:
            if latest['Close'] > bb_upper:
                confidence += 20
                reasons.append("Bullish breakout above upper band")
                return 1, min(confidence, 90), reasons
            elif latest['Close'] < bb_lower:
                confidence += 20
                reasons.append("Bearish breakdown below lower band")
                return -1, min(confidence, 90), reasons
        
        return 0, confidence, reasons


class StrategyConfidenceScoring:
    """Main confidence scoring engine"""
    
    def analyze(self, df, levels=None):
        if df.empty or len(df) < 50:
            return 0, 50, ["Insufficient data"]
        
        latest = df.iloc[-1]
        score = 50
        reasons = []
        
        # RSI (30% weight)
        rsi = latest.get('RSI', 50)
        if rsi < 25:
            score += 20
            reasons.append(f"RSI extreme oversold ({rsi:.0f})")
        elif rsi < 30:
            score += 15
            reasons.append(f"RSI oversold ({rsi:.0f})")
        elif rsi < 35:
            score += 10
            reasons.append(f"RSI nearing oversold ({rsi:.0f})")
        elif rsi > 75:
            score -= 20
            reasons.append(f"RSI extreme overbought ({rsi:.0f})")
        elif rsi > 70:
            score -= 15
            reasons.append(f"RSI overbought ({rsi:.0f})")
        elif rsi > 65:
            score -= 10
            reasons.append(f"RSI nearing overbought ({rsi:.0f})")
        else:
            reasons.append(f"RSI neutral ({rsi:.0f})")
        
        # MACD (25% weight)
        macd = latest.get('MACD', 0)
        signal = latest.get('Signal_Line', 0)
        if macd > signal:
            score += 12
            reasons.append("MACD bullish crossover")
        else:
            score -= 12
            reasons.append("MACD bearish crossover")
        
        # EMA Alignment (20% weight)
        price = latest['Close']
        ema20 = latest.get('EMA_20', price)
        ema50 = latest.get('EMA_50', price)
        
        if price > ema20 > ema50:
            score += 15
            reasons.append("Perfect bullish alignment")
        elif price > ema20:
            score += 8
            reasons.append("Price above EMA20")
        elif price < ema20 < ema50:
            score -= 15
            reasons.append("Perfect bearish alignment")
        elif price < ema20:
            score -= 8
            reasons.append("Price below EMA20")
        
        # Volume (10% weight)
        volume_ratio = latest.get('Volume_Ratio', 1)
        if volume_ratio > 1.5:
            if score > 50:
                score += 10
                reasons.append(f"High volume confirmation ({volume_ratio:.1f}x)")
            else:
                score -= 10
                reasons.append(f"High volume sell-off ({volume_ratio:.1f}x)")
        
        # ADX (10% weight)
        adx = latest.get('ADX', 20)
        if adx > 30:
            if score > 50:
                score += 10
                reasons.append(f"Strong trend confirmation (ADX {adx:.0f})")
        
        # Risk-Reward (5% weight)
        if levels:
            rr = levels.get('risk_reward', 0)
            if rr >= 2:
                score += 8
                reasons.append(f"Excellent risk-reward (1:{rr:.1f})")
            elif rr < 1:
                score -= 10
                reasons.append(f"Poor risk-reward (1:{rr:.1f})")
        
        score = max(0, min(100, score))
        
        if score >= 65:
            return 1, score, reasons
        elif score <= 35:
            return -1, score, reasons
        else:
            return 0, score, reasons


# ==========================================
# PART 4: ENSEMBLE VOTING SYSTEM
# ==========================================

class EnsembleVoting:
    """6 strategies voting together for maximum accuracy"""
    
    def __init__(self):
        self.strategies = [
            StrategyMomentumBreakout(),
            StrategyPullbackSnap(),
            StrategyVWAPReversal(),
            StrategyTrendReversal(),
            StrategyVolatilityExpansion(),
            StrategyConfidenceScoring()
        ]
        
        self.strategy_names = [
            "Momentum Breakout",
            "Pullback Snap",
            "VWAP Reversal",
            "Trend Reversal",
            "Volatility Expansion",
            "Confidence Scoring"
        ]
        
        # Weights for each strategy
        self.weights = [1.2, 1.0, 1.3, 1.0, 1.2, 1.5]
    
    def analyze(self, df, levels=None):
        signals = []
        all_reasons = []
        strategy_results = []
        
        for i, strategy in enumerate(self.strategies):
            if self.strategy_names[i] == "Confidence Scoring":
                signal, confidence, reasons = strategy.analyze(df, levels)
            else:
                signal, confidence, reasons = strategy.analyze(df)
            
            weighted_signal = signal * self.weights[i]
            signals.append(weighted_signal)
            all_reasons.extend(reasons[:2])
            
            strategy_results.append({
                'name': self.strategy_names[i],
                'signal': signal,
                'confidence': confidence,
                'reasons': reasons[:2]
            })
        
        # Calculate weighted average
        total_weight = sum(self.weights)
        weighted_signal = sum(signals) / total_weight
        
        # Calculate average confidence
        avg_confidence = sum(r['confidence'] for r in strategy_results) / len(strategy_results)
        
        # Determine final signal
        if weighted_signal > 0.3:
            final_signal = 1
        elif weighted_signal < -0.3:
            final_signal = -1
        else:
            final_signal = 0
        
        # Boost confidence if multiple strategies agree
        buy_count = sum(1 for r in strategy_results if r['signal'] == 1)
        sell_count = sum(1 for r in strategy_results if r['signal'] == -1)
        
        if final_signal == 1 and buy_count >= 4:
            avg_confidence = min(95, avg_confidence * 1.1)
        elif final_signal == -1 and sell_count >= 4:
            avg_confidence = min(95, avg_confidence * 1.1)
        
        # Determine action text
        if final_signal == 1:
            if avg_confidence >= 80:
                action = "STRONG_BUY"
            elif avg_confidence >= 65:
                action = "BUY"
            else:
                action = "WEAK_BUY"
        elif final_signal == -1:
            if avg_confidence >= 80:
                action = "STRONG_SELL"
            elif avg_confidence >= 65:
                action = "SELL"
            else:
                action = "WEAK_SELL"
        else:
            action = "HOLD"
        
        return {
            'signal': final_signal,
            'confidence': round(avg_confidence, 1),
            'action': action,
            'vote_summary': f"{buy_count}/6 strategies agree on BUY" if final_signal == 1 else f"{sell_count}/6 strategies agree on SELL",
            'strategy_results': strategy_results,
            'reasons': all_reasons[:6]
        }


# ==========================================
# PART 5: MARKET REGIME DETECTOR
# ==========================================

class MarketRegimeDetector:
    """Detects current market conditions"""
    
    def detect(self, df):
        if df.empty or len(df) < 50:
            return "UNKNOWN"
        
        adx = df['ADX'].iloc[-1] if 'ADX' in df.columns else 20
        atr = df['ATR'].iloc[-1] if 'ATR' in df.columns else df['Close'].pct_change().std() * df['Close'].iloc[-1]
        price = df['Close'].iloc[-1]
        volatility_pct = (atr / price) * 100
        
        ema20 = df['EMA_20'].iloc[-1] if 'EMA_20' in df.columns else df['Close'].iloc[-1]
        ema50 = df['EMA_50'].iloc[-1] if 'EMA_50' in df.columns else df['Close'].iloc[-1]
        
        if volatility_pct > 5:
            return "HIGH_VOLATILITY"
        
        if adx > 25:
            return "BULL_TRENDING" if ema20 > ema50 else "BEAR_FALLING"
        else:
            return "SIDEWAYS_RANGING"


# ==========================================
# PART 6: RISK MANAGER
# ==========================================

class RiskManager:
    """Professional risk management system"""
    
    def calculate_advanced_risk_levels(self, df, account_size=100000):
        if df.empty or len(df) < 20:
            return {}
        
        current_price = df["Close"].iloc[-1]
        atr = df["ATR"].iloc[-1] if df["ATR"].iloc[-1] > 0 else current_price * 0.02
        
        volatility_multiplier = 1.0
        if df["ATR"].iloc[-1] / current_price > 0.03:
            volatility_multiplier = 1.3
        elif df["ATR"].iloc[-1] / current_price < 0.01:
            volatility_multiplier = 0.7
        
        support = df["Support_20"].iloc[-1]
        resistance = df["Resistance_20"].iloc[-1]
        
        recent_high = df["High"].tail(50).max()
        recent_low = df["Low"].tail(50).min()
        fib_range = recent_high - recent_low
        
        if df["EMA_20"].iloc[-1] > df["EMA_50"].iloc[-1]:
            entry = current_price
        else:
            entry = support * 1.005
        
        stoploss = entry - (atr * 2.5 * volatility_multiplier)
        stoploss = max(stoploss, support * 0.97)
        
        if resistance > entry:
            target = min(resistance * 0.99, entry + (atr * 5 * volatility_multiplier))
        else:
            target = entry + (atr * 4 * volatility_multiplier)
        
        risk = entry - stoploss
        reward = target - entry
        rr_ratio = reward / risk if risk > 0 else 0
        
        risk_percent = 2
        position_size = (account_size * risk_percent / 100) / risk if risk > 0 else 0
        
        return {
            "entry": round(entry, 2),
            "stoploss": round(stoploss, 2),
            "target": round(target, 2),
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "atr": round(atr, 2),
            "risk_reward": round(rr_ratio, 2),
            "position_size": round(position_size, 0),
            "risk_amount": round(risk, 2),
            "reward_amount": round(reward, 2),
            "volatility": "HIGH" if volatility_multiplier > 1 else "LOW" if volatility_multiplier < 0.8 else "NORMAL",
            "fib_382": round(recent_high - fib_range * 0.382, 2),
            "fib_500": round(recent_high - fib_range * 0.5, 2),
            "fib_618": round(recent_high - fib_range * 0.618, 2)
        }


# ==========================================
# PART 7: ADVANCED MATHEMATICS
# ==========================================

# ==========================================
# PART 7: ADVANCED MATHEMATICS (updated)
# ==========================================

class QuantitativeMetrics:
    """Advanced mathematical metrics — self-contained, no silent failures."""

    def __init__(self):
        from advanced_math import QuantitativeAI
        self.quant = QuantitativeAI()

    def calculate_win_probability(self, df, levels):
        close_col = 'Close' if 'Close' in df.columns else 'close'

        if df.empty or len(df) < 50:
            return {
                'win_probability': 50,
                'expected_value': 0.0,
                'sample_size': 0,
                'verdict': 'NEUTRAL',
                'message': 'Need more data for analysis'
            }

        current_indicators = {
            'rsi':          df['RSI'].iloc[-1]          if 'RSI'          in df.columns else 50,
            'ema_20':       df['EMA_20'].iloc[-1]       if 'EMA_20'       in df.columns else df[close_col].iloc[-1],
            'ema_50':       df['EMA_50'].iloc[-1]       if 'EMA_50'       in df.columns else df[close_col].iloc[-1],
            'volume_ratio': df['Volume_Ratio'].iloc[-1] if 'Volume_Ratio' in df.columns else 1.0,
            'adx':          df['ADX'].iloc[-1]          if 'ADX'          in df.columns else 20,
        }

        win_prob, expected_value, sample_size = self.quant.calculate_win_probability(
            df, current_indicators
        )
        risk_reward = levels.get('risk_reward', 1.5) if isinstance(levels, dict) else 1.5
        verdict, message = self.quant.get_trade_verdict(win_prob, expected_value, risk_reward)

        return {
            'win_probability': round(win_prob, 1),
            'expected_value':  round(expected_value, 2),
            'sample_size':     sample_size,
            'verdict':         verdict,
            'message':         message,
        }


class MonteCarloSimulator:
    """Monte Carlo simulation — GBM + fat tails + jump diffusion."""

    def __init__(self):
        from advanced_math import MonteCarloSimulator as MCSim
        self.mc = MCSim()

    def run_simulation(self, df, current_price, target, stoploss):
        if df is None or df.empty or len(df) < 50:
            return None
        return self.mc.run_simulation(df, current_price, target, stoploss)

# ==========================================
# MULTI-TIMEFRAME ANALYSIS ENGINE
# ==========================================

class MultiTimeframeAnalyzer:
    """
    Advanced Multi-timeframe Analysis
    Analyzes Weekly, Daily, and Hourly charts simultaneously
    """
    
    def __init__(self):
        self.timeframes = {
            'Weekly': {'days': 7, 'interval': '1wk', 'weight': 0.50},
            'Daily': {'days': 1, 'interval': '1d', 'weight': 0.30},
            'Hourly': {'days': 0.04167, 'interval': '1h', 'weight': 0.20}
        }
    
    def fetch_multi_timeframe_data(self, symbol):
        """Fetch data for all three timeframes"""
        import yfinance as yf
        from brain_ultimate import ultimate_brain  # Use existing instance
        
        tf_data = {}
        
        for tf_name, tf_config in self.timeframes.items():
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period="6mo", interval=tf_config['interval'])
                
                if not data.empty and len(data) > 20:
                    # Calculate indicators using the existing brain
                    data = ultimate_brain.calculate_all_indicators(data)
                    tf_data[tf_name] = data
                else:
                    tf_data[tf_name] = None
            except Exception as e:
                tf_data[tf_name] = None
        
        return tf_data
    
    def analyze_timeframe(self, df, timeframe_name):
        """Analyze a single timeframe and return score and direction"""
        if df is None or df.empty or len(df) < 20:
            return {'score': 50, 'direction': 'NEUTRAL', 'confidence': 50, 'reasons': []}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        score = 50
        reasons = []
        
        # 1. Trend Analysis (30% weight)
        ema20 = latest.get('EMA_20', latest['Close'])
        ema50 = latest.get('EMA_50', latest['Close'])
        price = latest['Close']
        
        if price > ema20 > ema50:
            score += 15
            reasons.append(f"Perfect bullish alignment on {timeframe_name}")
        elif price > ema20:
            score += 8
            reasons.append(f"Price above EMA20 on {timeframe_name}")
        elif price < ema20 < ema50:
            score -= 15
            reasons.append(f"Bearish alignment on {timeframe_name}")
        elif price < ema20:
            score -= 8
            reasons.append(f"Price below EMA20 on {timeframe_name}")
        
        # 2. MACD Analysis (25% weight)
        if 'MACD' in df.columns and 'Signal_Line' in df.columns:
            macd = latest['MACD']
            signal = latest['Signal_Line']
            if macd > signal:
                score += 12
                reasons.append(f"MACD bullish on {timeframe_name}")
            else:
                score -= 12
                reasons.append(f"MACD bearish on {timeframe_name}")
        
        # 3. RSI Analysis (20% weight)
        rsi = latest.get('RSI', 50)
        if rsi < 30:
            score += 10
            reasons.append(f"RSI oversold on {timeframe_name} ({rsi:.0f})")
        elif rsi > 70:
            score -= 10
            reasons.append(f"RSI overbought on {timeframe_name} ({rsi:.0f})")
        
        # 4. ADX Trend Strength (15% weight)
        adx = latest.get('ADX', 20)
        if adx > 30:
            if score > 50:
                score += 8
                reasons.append(f"Strong trend on {timeframe_name} (ADX {adx:.0f})")
        elif adx < 20:
            if score < 50:
                score -= 5
        
        # 5. Volume Confirmation (10% weight)
        volume_ratio = latest.get('Volume_Ratio', 1)
        if volume_ratio > 1.5:
            if score > 50:
                score += 5
                reasons.append(f"High volume on {timeframe_name}")
        
        # Determine direction and confidence
        if score >= 70:
            direction = "BULLISH"
            symbol = "📈"
            confidence = min(95, score)
        elif score >= 60:
            direction = "BULLISH"
            symbol = "📈"
            confidence = score
        elif score <= 30:
            direction = "BEARISH"
            symbol = "📉"
            confidence = min(95, 100 - score)
        elif score <= 40:
            direction = "BEARISH"
            symbol = "📉"
            confidence = 100 - score
        else:
            direction = "NEUTRAL"
            symbol = "🔄"
            confidence = 50
        
        return {
            'score': score,
            'direction': direction,
            'symbol': symbol,
            'confidence': round(confidence, 1),
            'reasons': reasons[:2]
        }
    
    def get_unified_signal(self, symbol):
        """Get unified signal from all timeframes"""
        tf_data = self.fetch_multi_timeframe_data(symbol)
        
        results = {}
        total_score = 0
        total_weight = 0
        
        for tf_name, config in self.timeframes.items():
            df = tf_data.get(tf_name)
            analysis = self.analyze_timeframe(df, tf_name)
            results[tf_name] = analysis
            
            weight = config['weight']
            total_score += analysis['score'] * weight
            total_weight += weight
        
        final_score = total_score / total_weight if total_weight > 0 else 50
        final_score = max(0, min(100, final_score))
        
        # Determine final action
        if final_score >= 70:
            final_action = "STRONG BUY"
            action_color = "#00ff88"
            action_icon = "✅"
        elif final_score >= 60:
            final_action = "BUY"
            action_color = "#00e676"
            action_icon = "📈"
        elif final_score <= 30:
            final_action = "STRONG SELL"
            action_color = "#ff1744"
            action_icon = "❌"
        elif final_score <= 40:
            final_action = "SELL"
            action_color = "#ff5252"
            action_icon = "📉"
        else:
            final_action = "HOLD"
            action_color = "#ffd700"
            action_icon = "⚠️"
        
        # Count how many timeframes agree
        bullish_count = sum(1 for r in results.values() if r['direction'] == 'BULLISH')
        bearish_count = sum(1 for r in results.values() if r['direction'] == 'BEARISH')
        
        return {
            'final_score': round(final_score, 1),
            'final_action': final_action,
            'action_color': action_color,
            'action_icon': action_icon,
            'agreement': f"{bullish_count}/3 bullish" if bullish_count > bearish_count else f"{bearish_count}/3 bearish",
            'timeframes': results,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count
        }




# ==========================================
# PART 8: ULTIMATE TRADING BRAIN (Main Class)
# ==========================================

class UltimateTradingBrain:
    """
    THE ULTIMATE TRADING BRAIN
    - 6 strategies voting together
    - Advanced mathematics
    - Professional risk management
    """
    
    def __init__(self):
        self.indicators = IndicatorsEngine()
        self.ensemble = EnsembleVoting()
        self.regime_detector = MarketRegimeDetector()
        self.risk_manager = RiskManager()
        self.quant_metrics = QuantitativeMetrics()
        self.monte_carlo = MonteCarloSimulator()
        self.kalman_filter = KalmanFilter()
    
    def calculate_all_indicators(self, df):
        """Calculate all indicators with Kalman smoothing"""
        df = self.indicators.calculate_all(df)
        return self._apply_kalman(df)
    
    def _apply_kalman(self, df):
        """Apply Kalman filter for noise reduction"""
        if df.empty or len(df) < 10:
            return df
        
        filtered_df = df.copy()
        
        price_filter = KalmanFilter()
        filtered_df['Close_Kalman'] = price_filter.filter_series(df['Close'].values)
        
        if 'RSI' in df.columns:
            rsi_filter = KalmanFilter(process_variance=1e-2, measurement_variance=1e-1)
            filtered_df['RSI_Kalman'] = rsi_filter.filter_series(df['RSI'].values)
        
        return filtered_df
    
    def get_ensemble_analysis(self, df, levels=None):
        """Get analysis from all 6 strategies"""
        return self.ensemble.analyze(df, levels)
    
    def generate_smart_signals(self, df):
        """Generate signals for backtesting compatibility"""
        result = self.ensemble.analyze(df)
        
        buy_signals = []
        sell_signals = []
        
        if result['signal'] == 1:
            latest = df.iloc[-1]
            buy_signals.append({
                'index': df.index[-1],
                'Close': latest['Close'],
                'Score': result['confidence'],
                'Confidence': 'HIGH' if result['confidence'] >= 70 else 'MEDIUM',
                'Reasons': result['reasons'][:3]
            })
        elif result['signal'] == -1:
            latest = df.iloc[-1]
            sell_signals.append({
                'index': df.index[-1],
                'Close': latest['Close'],
                'Score': result['confidence'],
                'Confidence': 'HIGH' if result['confidence'] >= 70 else 'MEDIUM',
                'Reasons': result['reasons'][:3]
            })
        
        buy_df = pd.DataFrame(buy_signals)
        sell_df = pd.DataFrame(sell_signals)
        
        if not buy_df.empty:
            buy_df.set_index("index", inplace=True)
        if not sell_df.empty:
            sell_df.set_index("index", inplace=True)
        
        return buy_df, sell_df, result['confidence'], result['action'], result['confidence'], 30
    
    def calculate_advanced_risk_levels(self, df, account_size=100000):
        return self.risk_manager.calculate_advanced_risk_levels(df, account_size)
    
    def generate_actionable_insights(self, df, levels, buy_signals, sell_signals):
        insights = []
        
        if df.empty or len(df) < 20:
            return ["Waiting for sufficient data..."]
        
        latest = df.iloc[-1]
        
        if latest["EMA_20"] > latest["EMA_50"]:
            if latest["Close"] > latest["EMA_20"]:
                insights.append("📈 **Uptrend Active** - Price is rising. Good time to buy.")
            else:
                insights.append("📈 **Uptrend Pausing** - Price is cooling off. Wait for bounce back.")
        else:
            if latest["Close"] < latest["EMA_20"]:
                insights.append("📉 **Downtrend Active** - Price is falling. Avoid buying.")
            else:
                insights.append("📉 **Attempting Recovery** - Price trying to rise. Wait for confirmation.")
        
        if latest["RSI"] < 30:
            insights.append(f"🟢 **Oversold Zone** - RSI at {latest['RSI']:.0f}. Stock may bounce up soon.")
        elif latest["RSI"] > 70:
            insights.append(f"🔴 **Overbought Zone** - RSI at {latest['RSI']:.0f}. Profit booking likely.")
        else:
            insights.append(f"🟡 **Neutral Zone** - RSI at {latest['RSI']:.0f}. Wait for clearer direction.")
        
        if latest["Volume_Ratio"] > 1.5:
            if latest["Close"] > df["Close"].iloc[-2]:
                insights.append(f"📊 **Bullish Volume Surge** - {latest['Volume_Ratio']:.1f}x normal volume.")
            else:
                insights.append(f"⚠️ **Bearish Volume Surge** - {latest['Volume_Ratio']:.1f}x normal volume.")
        
        if latest["ADX"] > 25:
            direction = "BULLISH" if latest["EMA_20"] > latest["EMA_50"] else "BEARISH"
            insights.append(f"💪 **Strong Trend** - ADX at {latest['ADX']:.0f}. {direction} momentum strong.")
        else:
            insights.append(f"🔄 **Range Bound** - ADX at {latest['ADX']:.0f}. No strong trend.")
        
        if levels:
            rr = levels.get('risk_reward', 0)
            if rr >= 2:
                insights.append(f"✅ **Excellent Risk-Reward** - 1:{rr:.1f}. Favorable for entry.")
            elif rr < 1:
                insights.append(f"⚠️ **Poor Risk-Reward** - 1:{rr:.1f}. Skip this trade.")
            insights.append(f"💰 **Recommended Quantity** - {levels['position_size']:.0f} shares (2% risk model)")
        
        return insights[:6]
    
    def get_trading_recommendation(self, overall, confidence, risk_score, levels):
        if not levels:
            return "HOLD", 50
        
        if "BUY" in overall and risk_score < 50 and levels["risk_reward"] >= 1.5:
            return "BUY", confidence
        elif "SELL" in overall and risk_score < 50:
            return "AVOID", confidence
        else:
            return "HOLD", 40
    
    def run_monte_carlo_simulation(self, df, current_price, target, stoploss):
        return self.monte_carlo.run_simulation(df, current_price, target, stoploss)
    
    def calculate_quantitative_metrics(self, df, levels):
        return self.quant_metrics.calculate_win_probability(df, levels)
    
    def get_signal_from_brain(self, df, levels=None):
        """Simple signal for compatibility"""
        result = self.ensemble.analyze(df, levels)
        return result['signal']

    # Add to UltimateTradingBrain class
    def get_multi_timeframe_analysis(self, symbol):
        """Get multi-timeframe analysis for a stock"""
        analyzer = MultiTimeframeAnalyzer()
        return analyzer.get_unified_signal(symbol)



# ==========================================
# SINGLETON INSTANCE
# ==========================================
ultimate_brain = UltimateTradingBrain()