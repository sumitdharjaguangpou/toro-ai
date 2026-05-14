# regime_models.py
# ==========================================
# ADAPTIVE MARKET REGIME ENGINE
# ==========================================

import numpy as np
import pandas as pd


class MarketRegimeEngine:
    """
    Detects current market regime dynamically.

    Regimes:
    - TRENDING_BULL
    - TRENDING_BEAR
    - SIDEWAYS
    - HIGH_VOLATILITY
    - ACCUMULATION
    """

    def __init__(self):
        self.adx_trend_threshold = 25
        self.high_volatility_threshold = 0.04
        self.low_volatility_threshold = 0.012

    # ==========================================
    # MAIN DETECTOR
    # ==========================================

    def detect(self, df):

        if df is None or df.empty or len(df) < 50:
            return {
                "regime": "UNKNOWN",
                "confidence": 0,
                "description": "Insufficient data",
                "market_bias": "NEUTRAL",
                "risk_level": "HIGH"
            }

        latest = df.iloc[-1]

        # --------------------------------------
        # SAFE VALUE EXTRACTION
        # --------------------------------------

        close = latest.get("Close", 0)

        ema20 = latest.get("EMA_20", close)
        ema50 = latest.get("EMA_50", close)
        ema200 = latest.get("EMA_200", close)

        adx = latest.get("ADX", 20)
        atr = latest.get("ATR", 0)

        rsi = latest.get("RSI", 50)

        volume_ratio = latest.get("Volume_Ratio", 1)

        # --------------------------------------
        # VOLATILITY
        # --------------------------------------

        atr_percent = atr / close if close > 0 else 0

        # --------------------------------------
        # TREND STRENGTH
        # --------------------------------------

        bullish_structure = (
            close > ema20 > ema50
        )

        strong_bull_structure = (
            close > ema20 > ema50 > ema200
        )

        bearish_structure = (
            close < ema20 < ema50
        )

        strong_bear_structure = (
            close < ema20 < ema50 < ema200
        )

        # ==========================================
        # REGIME CLASSIFICATION
        # ==========================================

        # --------------------------------------
        # HIGH VOLATILITY
        # --------------------------------------

        if atr_percent >= self.high_volatility_threshold:

            confidence = min(95, int(atr_percent * 1000))

            return {
                "regime": "HIGH_VOLATILITY",
                "confidence": confidence,
                "description": "Large price swings detected",
                "market_bias": "DEFENSIVE",
                "risk_level": "VERY_HIGH",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # STRONG TRENDING BULL
        # --------------------------------------

        if strong_bull_structure and adx >= self.adx_trend_threshold:

            confidence = min(
                95,
                int(
                    50 +
                    (adx - 20) +
                    (volume_ratio * 5)
                )
            )

            return {
                "regime": "TRENDING_BULL",
                "confidence": confidence,
                "description": "Strong bullish trend structure",
                "market_bias": "BULLISH",
                "risk_level": "MODERATE",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # STRONG TRENDING BEAR
        # --------------------------------------

        if strong_bear_structure and adx >= self.adx_trend_threshold:

            confidence = min(
                95,
                int(
                    50 +
                    (adx - 20) +
                    (volume_ratio * 5)
                )
            )

            return {
                "regime": "TRENDING_BEAR",
                "confidence": confidence,
                "description": "Strong bearish trend structure",
                "market_bias": "BEARISH",
                "risk_level": "HIGH",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # ACCUMULATION PHASE
        # --------------------------------------

        if (
            atr_percent <= self.low_volatility_threshold and
            45 <= rsi <= 55 and
            adx < 20
        ):

            return {
                "regime": "ACCUMULATION",
                "confidence": 70,
                "description": "Low volatility consolidation",
                "market_bias": "NEUTRAL",
                "risk_level": "LOW",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # SIDEWAYS MARKET
        # --------------------------------------

        if adx < 20:

            confidence = max(
                50,
                int(70 - adx)
            )

            return {
                "regime": "SIDEWAYS",
                "confidence": confidence,
                "description": "Weak directional movement",
                "market_bias": "NEUTRAL",
                "risk_level": "LOW",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # DEFAULT BULLISH
        # --------------------------------------

        if bullish_structure:

            return {
                "regime": "MILD_BULLISH",
                "confidence": 60,
                "description": "Moderate bullish structure",
                "market_bias": "BULLISH",
                "risk_level": "MODERATE",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # DEFAULT BEARISH
        # --------------------------------------

        if bearish_structure:

            return {
                "regime": "MILD_BEARISH",
                "confidence": 60,
                "description": "Moderate bearish structure",
                "market_bias": "BEARISH",
                "risk_level": "MODERATE",
                "atr_percent": round(atr_percent * 100, 2)
            }

        # --------------------------------------
        # FINAL FALLBACK
        # --------------------------------------

        return {
            "regime": "NEUTRAL",
            "confidence": 50,
            "description": "Mixed market conditions",
            "market_bias": "NEUTRAL",
            "risk_level": "MODERATE",
            "atr_percent": round(atr_percent * 100, 2)
        }

    # ==========================================
    # ADAPTIVE SIGNAL WEIGHTS
    # ==========================================

    def get_regime_weights(self, regime_name):
        """
        Returns adaptive weights for different models.
        """

        weights = {

            # ----------------------------------
            # BULL TREND
            # ----------------------------------

            "TRENDING_BULL": {
                "trend": 0.40,
                "momentum": 0.30,
                "volume": 0.15,
                "mean_reversion": 0.05,
                "volatility": 0.10
            },

            # ----------------------------------
            # BEAR TREND
            # ----------------------------------

            "TRENDING_BEAR": {
                "trend": 0.35,
                "momentum": 0.30,
                "volume": 0.20,
                "mean_reversion": 0.05,
                "volatility": 0.10
            },

            # ----------------------------------
            # SIDEWAYS
            # ----------------------------------

            "SIDEWAYS": {
                "trend": 0.10,
                "momentum": 0.10,
                "volume": 0.10,
                "mean_reversion": 0.50,
                "volatility": 0.20
            },

            # ----------------------------------
            # HIGH VOLATILITY
            # ----------------------------------

            "HIGH_VOLATILITY": {
                "trend": 0.15,
                "momentum": 0.15,
                "volume": 0.20,
                "mean_reversion": 0.10,
                "volatility": 0.40
            },

            # ----------------------------------
            # ACCUMULATION
            # ----------------------------------

            "ACCUMULATION": {
                "trend": 0.10,
                "momentum": 0.15,
                "volume": 0.25,
                "mean_reversion": 0.35,
                "volatility": 0.15
            }
        }

        return weights.get(
            regime_name,
            {
                "trend": 0.20,
                "momentum": 0.20,
                "volume": 0.20,
                "mean_reversion": 0.20,
                "volatility": 0.20
            }
        )


# ==========================================
# SINGLETON INSTANCE
# ==========================================

market_regime_engine = MarketRegimeEngine()