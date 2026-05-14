# about.py
# ==========================================
# ABOUT TORO AI - Streamlit Native Expanders
# ==========================================

import streamlit as st

def render_about():
    """Render the About TORO AI page with expandable sections"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-bottom: 20px;">
        <div style="font-size: 36px; font-weight: 800; background: linear-gradient(135deg, #00ffff, #ff00ff); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">
            🐃 TORO AI
        </div>
        <div style="font-size: 14px; color: #8892b0; margin-top: 8px;">
            Quantitative Stock Intelligence Platform
        </div>
        <div style="font-size: 11px; color: #64748b; margin-top: 5px;">
            Version 2.0 | Mathematics-First Trading System
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # CATEGORY 1: GETTING STARTED
    # ==========================================
    st.markdown("### 🚀 GETTING STARTED")
        
    with st.expander("❓ What is TORO AI?"):
        st.markdown("""
        <style>
        .compact-content {
            font-size: 13px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .compact-content h4 {
            font-size: 14px;
            color: #00ff88;
            margin: 12px 0 6px 0;
            font-weight: 600;
        }
        .compact-content h5 {
            font-size: 13px;
            color: #00ffff;
            margin: 8px 0 4px 0;
            font-weight: 600;
        }
        .compact-content strong {
            color: #00ffff;
        }
        .compact-content table {
            font-size: 12px;
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        .compact-content td, .compact-content th {
            padding: 6px 8px;
            border-bottom: 1px solid rgba(0,255,255,0.1);
        }
        .compact-content th {
            color: #00ffff;
            font-weight: 600;
        }
        .highlight-box {
            background: rgba(0, 255, 255, 0.05);
            padding: 8px 12px;
            border-left: 3px solid #00ffff;
            border-radius: 0 6px 6px 0;
            margin: 10px 0;
            font-size: 12px;
        }
        .info-box {
            background: rgba(0, 255, 136, 0.05);
            border-left: 3px solid #00ff88;
            padding: 8px 12px;
            margin: 10px 0;
            font-size: 12px;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin: 10px 0;
        }
        .metric-item {
            background: rgba(0,255,255,0.03);
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 12px;
        }
        hr {
            margin: 12px 0;
            opacity: 0.3;
        }
        </style>
        
        <div class="compact-content">
        
        <strong>TORO AI</strong> is a professional-grade quantitative trading platform that combines <strong>institutional mathematical models</strong> with real-time market data. Unlike traditional trading tools that rely on lagging technical indicators, TORO AI uses <strong>pure mathematics and statistical probability</strong> to analyze markets and generate actionable trading signals.
        
        <hr>
        
        <h4>🏛️ What Does "Quantitative Trading Platform" Mean?</h4>
        
        A <strong>quantitative trading platform</strong> uses mathematical and statistical models to make trading decisions instead of relying on human judgment or traditional technical analysis.
        
        | Aspect | Traditional Approach | Quantitative Approach |
        |--------|---------------------|----------------------|
        | **Decision Basis** | "RSI is high, so sell" | "78% probability of downward move" |
        | **Analysis Method** | Visual chart patterns | Mathematical formulas |
        | **Risk Management** | Fixed stop loss | Dynamic, probability-based sizing |
        | **Market Adaptation** | Manual | Automatic regime detection |
        
        <hr>
        
        <h4>🔬 What Are "Institutional Mathematical Models"?</h4>
        
        These are the same mathematical models used by <strong>quantitative hedge funds</strong> like Renaissance Technologies, Two Sigma, and D.E. Shaw:
        
        <div class="metric-grid">
            <div class="metric-item"><strong>🌀 Hurst Exponent</strong><br>Detects if market is trending or mean-reverting</div>
            <div class="metric-item"><strong>📡 Shannon Entropy</strong><br>Measures market disorder & predictability</div>
            <div class="metric-item"><strong>💰 Kelly Criterion</strong><br>Calculates optimal position size for growth</div>
            <div class="metric-item"><strong>📈 Bayesian Probability</strong><br>Updates confidence as new data arrives</div>
            <div class="metric-item"><strong>⚠️ Value at Risk (VaR)</strong><br>Maximum expected loss at 95% confidence</div>
            <div class="metric-item"><strong>🎲 Monte Carlo Simulation</strong><br>Thousands of scenarios to calculate probabilities</div>
        </div>
        
        <hr>
        
        <h4>❌ Moving Beyond Traditional Technical Indicators</h4>
        
        Traditional indicators like RSI, MACD, and Bollinger Bands have significant limitations:
        
        <table>
        <tr><th>Indicator</th><th>Problem</th><th>TORO AI Solution</th></tr>
        <tr><td>RSI</td><td>Can stay overbought for weeks</td><td>Uses statistical z-scores</td></tr>
        <tr><td>MACD</td><td>Always lags behind price</td><td>Uses real-time probability models</td></tr>
        <tr><td>Bollinger Bands</td><td>Assumes normal distribution</td><td>Uses adaptive volatility models</td></tr>
        <tr><td>Moving Averages</td><td>Always react after price moves</td><td>Uses predictive Hurst Exponent</td></tr>
        </table>
        
        <hr>
        
        <h4>📊 How TORO AI Actually Works</h4>
        
        <h5>Step 1: Data Ingestion</h5>
        Fetches real-time and historical price data, volume, and other market metrics from Yahoo Finance.
        
        <h5>Step 2: Mathematical Analysis</h5>
        Applies 6+ institutional mathematical models to detect patterns that aren't visible to the naked eye.
        
        <h5>Step 3: Regime Detection</h5>
        Identifies current market conditions — trending, sideways, or high volatility — and adapts strategy accordingly.
        
        <h5>Step 4: Signal Generation</h5>
        Combines all models to produce BUY/SELL/HOLD signals with confidence scores (0-100%).
        
        <h5>Step 5: Risk Management</h5>
        Calculates optimal position size, stop loss, and target based on Kelly Criterion and ATR.
        
        <h5>Step 6: Output</h5>
        Presents actionable insights in a clean, professional dashboard.
        
        <hr>
        
        <h4>🎯 What Makes TORO AI Different?</h4>
        
        <div class="metric-grid">
            <div class="metric-item">🔮 <strong>Predictive</strong><br>Not reactive like indicators</div>
            <div class="metric-item">📊 <strong>Probability-Based</strong><br>"78% chance" not "maybe"</div>
            <div class="metric-item">🔄 <strong>Adaptive</strong><br>Changes with market conditions</div>
            <div class="metric-item">📐 <strong>Mathematical</strong><br>No subjective interpretation</div>
            <div class="metric-item">⚡ <strong>Real-Time</strong><br>Processes live market data</div>
            <div class="metric-item">🎯 <strong>Actionable</strong><br>Clear entry/exit levels</div>
        </div>
        
        <hr>
        
        <h4>🚀 Who Should Use TORO AI?</h4>
        
        <table>
        <tr><th>If You Are...</th><th>TORO AI Helps You...</th></tr>
        <tr><td>A swing trader</td><td>Catch trends early with multi-timeframe analysis</td></tr>
        <tr><td>A positional trader</td><td>Protect capital with professional risk metrics</td></tr>
        <tr><td>A quant enthusiast</td><td>Access institutional mathematical models for free</td></tr>
        <tr><td>A beginner</td><td>Understand market conditions with clear signals</td></tr>
        <tr><td>A professional</td><td>Get institutional-grade analytics without expensive software</td></tr>
        </table>
        
        <hr>
        
        <h4>🔬 Real-World Example: Analyzing RELIANCE</h4>
        
        <div class="metric-grid">
            <div class="metric-item">📡 <strong>Hurst: 0.67</strong><br>→ Trending market detected</div>
            <div class="metric-item">🌀 <strong>Entropy: 28%</strong><br>→ Highly predictable</div>
            <div class="metric-item">🎲 <strong>Monte Carlo: 72%</strong><br>→ Probability of hitting target</div>
            <div class="metric-item">💰 <strong>Kelly: 12%</strong><br>→ Suggested position size</div>
            <div class="metric-item">📊 <strong>Signal: BUY</strong><br>→ At ₹2,450</div>
            <div class="metric-item">🎯 <strong>Confidence: 78%</strong><br>→ High probability setup</div>
        </div>
        
        <div class="info-box">
        📈 <strong>Result:</strong> The AI correctly identified an uptrend, provided a clear entry price, suggested position size, and set a target with 78% confidence.
        </div>
        
        <hr>
        
        <h4>⚠️ Important Disclaimers</h4>
        
        <div class="highlight-box">
        💡 <strong>TORO AI is a tool, not a crystal ball.</strong> It provides probabilities and insights based on mathematical models, but no model is 100% accurate.
        </div>
        
        <div class="highlight-box">
        📊 <strong>Always combine AI insights with your own research.</strong> Use TORO AI as one of multiple inputs in your trading decision process.
        </div>
        
        <div class="highlight-box">
        💰 <strong>Never risk more than you can afford to lose.</strong> Even high-probability setups can fail.
        </div>
        
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🔍 How to search for stocks?"):
        st.markdown("""
        1. Use the **search bar** at the top of the application
        2. Type a stock symbol (e.g., `RELIANCE`, `TCS`, `HDFC`)
        3. The AI will auto-suggest matching stocks as you type
        4. Click on any suggestion to analyze that stock instantly
        
        > 💡 **Pro Tip:** You can also click on any stock in your watchlist to instantly switch to it!
        """)
    
    with st.expander("⭐ How to add stocks to watchlist?"):
        st.markdown("""
        **Method 1:** Click the **⭐ button** next to any stock suggestion in the search results.
        
        **Method 2:** Go to the **WATCHLIST tab** and manage your stocks there.
        
        Your watchlist is **automatically saved** and will persist even after closing the app.
        
        > 💡 **Pro Tip:** Click on any stock in your watchlist to instantly analyze it!
        """)
    
    # ==========================================
    # CATEGORY 2: AI SIGNALS
    # ==========================================
    st.markdown("### 🧠 UNDERSTANDING AI SIGNALS")

    with st.expander("📊 What do the AI signals mean?"):
        st.markdown("""
        <style>
        .signal-content {
            font-size: 12px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .signal-content strong {
            color: #00ffff;
        }
        .signal-table {
            font-size: 12px;
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        .signal-table td, .signal-table th {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(0,255,255,0.1);
        }
        .signal-table th {
            color: #00ffff;
            text-align: left;
            font-weight: 600;
        }
        .pro-tip {
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #ffd700;
            padding: 8px 12px;
            margin: 12px 0 0 0;
            font-size: 11px;
            border-radius: 0 6px 6px 0;
        }
        </style>
        
        <div class="signal-content">
        
        <strong>TORO AI generates 5 types of signals</strong> based on mathematical probability, not subjective interpretation:
        
        <table class="signal-table">
            <tr><th>Signal</th><th>Meaning</th><th>What You Should Do</th></tr>
            <tr><td>🟢 <strong>STRONG BUY</strong></td>
                <td>High-probability setup (75%+ confidence)</td>
                <td>Enter full position size, set tight stop loss</td>
            </tr>
            <tr><td>📈 <strong>BUY</strong></td>
                <td>Good probability setup (65-75% confidence)</td>
                <td>Enter normal position size, standard stop loss</td>
            </tr>
            <tr><td🟡 <strong>HOLD / CONSIDER</strong></td>
                <td>Neutral or waiting for confirmation (50-65% confidence)</td>
                <td>Wait for better entry or skip the trade</td>
            </tr>
            <tr><td📉 <strong>SELL</strong></td>
                <td>Bearish signals (35-50% confidence in upside)</td>
                <td>Exit existing positions, avoid new buys</td>
            </tr>
            <tr><td🔴 <strong>STRONG SELL / AVOID</strong></td>
                <td>Strong bearish signals (below 35% confidence)</td>
                <td>Close all positions, stay in cash</td>
            </tr>
        </table>
        
        <div class="pro-tip">
        💡 <strong>Pro Tip:</strong> Only trade when confidence is above <strong>65%</strong> AND risk-reward ratio is at least <strong>1:1.5</strong>. Lower confidence signals often result in losing trades.
        </div>
        
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📈 What is Market Regime?"):
        st.markdown("""
        <style>
        .regime-content {
            font-size: 12px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .regime-table {
            font-size: 12px;
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        .regime-table td, .regime-table th {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(0,255,255,0.1);
        }
        .regime-table th {
            color: #00ffff;
            text-align: left;
            font-weight: 600;
        }
        .regime-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }
        .info-note {
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #00ff88;
            padding: 8px 12px;
            margin: 12px 0 0 0;
            font-size: 11px;
            border-radius: 0 6px 6px 0;
        }
        </style>
        
        <div class="regime-content">
        
        <strong>Market Regime</strong> is the current "personality" or "behavior pattern" of the market. Just like weather has seasons (summer, winter, monsoon), the stock market has different behavioral phases. TORO AI automatically detects which regime the market is in and adapts its strategy accordingly.
        
        <table class="regime-table">
            <tr><th>Regime</th><th>What It Means</th><th>Trading Strategy</th><th>Position Size</th></tr>
            <tr>
                <td>🟢 <strong>BULLISH TREND</strong></td>
                <td>Price moving consistently upward, making higher highs and higher lows</td>
                <td>Aggressive buying, trend-following strategy</td>
                <td>100% of normal size</td>
            </tr>
            <tr>
                <td>🔴 <strong>BEARISH TREND</strong></td>
                <td>Price moving consistently downward, making lower highs and lower lows</td>
                <td>Avoid buying, consider selling or staying in cash</td>
                <td>0-30% of normal size</td>
            </tr>
            <tr>
                <td>🟡 <strong>SIDEWAYS / RANGING</strong></td>
                <td>Price moving horizontally between support and resistance</td>
                <td>Mean reversion strategy — buy at support, sell at resistance</td>
                <td>50-70% of normal size</td>
            </tr>
            <tr>
                <td>🟠 <strong>HIGH VOLATILITY</strong></td>
                <td>Large price swings in both directions, unpredictable movement</td>
                <td>Defensive mode — wider stops, smaller positions, wait for clarity</td>
                <td>25-40% of normal size</td>
            </tr>
            <tr>
                <td>🔵 <strong>ACCUMULATION</strong></td>
                <td>Smart money (institutions) quietly buying; price is bottoming</td>
                <td>Prepare to buy — start accumulating small positions</td>
                <td>30-50% of normal size, scale in gradually</td>
            </tr>
            <tr>
                <td>🔴⚪ <strong>DISTRIBUTION</strong></td>
                <td>Smart money selling; price is topping</td>
                <td>Take profits, reduce exposure, avoid new buys</td>
                <td>0% — stay in cash</td>
            </tr>
        }</table>
        
        <div class="info-note">
        📊 <strong>How TORO AI Detects Regimes:</strong> The system analyzes multiple factors including price structure (EMA alignment), trend strength (ADX), volatility (ATR), volume patterns, and RSI levels to determine the current regime with 70-95% confidence.
        </div>
        
        <div class="pro-tip">
        💡 <strong>Pro Tip:</strong> In BULLISH regimes, trust the BUY signals and use normal position sizes. In BEARISH regimes, ignore BUY signals — they are often false positives. In HIGH VOLATILITY, reduce all positions by 50-70%.
        </div>
        
        </div>
        """, unsafe_allow_html=True)
        

    # ==========================================
    # CATEGORY 3: QUANT ANALYTICS
    # ==========================================
    st.markdown("### 🔬 QUANTITATIVE ANALYTICS")

    with st.expander("🌀 What is Hurst Exponent?"):
        st.markdown("""
        <style>
        .quant-content {
            font-size: 12px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .quant-content strong {
            color: #00ffff;
        }
        .quant-table {
            font-size: 12px;
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        .quant-table td, .quant-table th {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(0,255,255,0.1);
        }
        .quant-table th {
            color: #00ffff;
            text-align: left;
            font-weight: 600;
        }
        .formula-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 8px 12px;
            font-family: monospace;
            font-size: 11px;
            color: #00ff88;
            border-radius: 6px;
            margin: 10px 0;
            text-align: center;
        }
        .insight-box {
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #00ffff;
            padding: 8px 12px;
            margin: 12px 0 0 0;
            font-size: 11px;
            border-radius: 0 6px 6px 0;
        }
        </style>
        
        <div class="quant-content">
        
        <strong>Hurst Exponent (H)</strong> is a mathematical formula that tells you whether a market is trending, random, or mean-reverting. It was developed by Harold Hurst, a British hydrologist, and later adapted for financial markets by Benoit Mandelbrot.
        
        <div class="formula-box">
        H = log(R/S) / log(N) where R = range, S = standard deviation, N = number of observations
        </div>
        
        <strong>How to Interpret Hurst Exponent:</strong>
        
        <table class="quant-table">
            <tr><th>H Value</th><th>Market Behavior</th><th>What It Means</th><th>Best Strategy</th></tr>
            <tr>
                <td><strong>H > 0.7</strong></td>
                <td><strong style="color:#00ff88;">Strongly Trending</strong></td>
                <td>Price moves persistently in one direction; momentum is strong</td>
                <td>Use trend-following strategy; add to winning positions</td>
            </tr>
            <tr>
                <td><strong>0.55 < H < 0.7</strong></td>
                <td><strong style="color:#7cfc00;">Weakly Trending</strong></td>
                <td>Trend exists but with pullbacks; momentum is moderate</td>
                <td>Trend-following with caution; use tighter stops</td>
            </tr>
            <tr>
                <td><strong>H = 0.5</strong></td>
                <td><strong style="color:#ffd700;">Random Walk</strong></td>
                <td>Price moves randomly; no predictable pattern; efficient market</td>
                <td>Be cautious; reduce position size; wait for clarity</td>
            </tr>
            <tr>
                <td><strong>0.3 < H < 0.45</strong></td>
                <td><strong style="color:#ffa500;">Weakly Mean-Reverting</strong></td>
                <td>Price tends to bounce back to average after moves</td>
                <td>Buy dips, sell rallies; fade extreme moves</td>
            </tr>
            <tr>
                <td><strong>H < 0.3</strong></td>
                <td><strong style="color:#ff1744;">Strongly Mean-Reverting</strong></td>
                <td>Price strongly pulls back to mean; range-bound market</td>
                <td>Strong mean reversion strategy; trade at extremes</td>
            </tr>
        </table>
        
        <div class="insight-box">
        📊 <strong>How TORO AI Uses Hurst Exponent:</strong> The system automatically detects the current Hurst value and adjusts its strategy — using trend-following for H > 0.55 and mean reversion for H < 0.45. This ensures the right strategy for current market conditions.
        </div>
        
        <div class="insight-box">
        💡 <strong>Pro Tip:</strong> When H > 0.6, avoid mean reversion strategies (buying dips can be dangerous in strong trends). When H < 0.4, avoid trend-following (you'll get whipsawed).
        </div>
        
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📊 What is Sharpe Ratio?"):
        st.markdown("""
        <div class="quant-content">
        
        <strong>Sharpe Ratio</strong> measures how much return you're getting for the amount of risk you're taking. It was developed by Nobel laureate William F. Sharpe and is the most widely used metric in institutional finance.
        
        <div class="formula-box">
        Sharpe Ratio = (Return - Risk-Free Rate) / Standard Deviation of Returns
        </div>
        
        <strong>Why It Matters:</strong> Two investments can have the same return, but the one with lower risk (volatility) has a higher Sharpe Ratio and is considered better.
        
        <table class="quant-table">
            <tr><th>Sharpe Ratio</th><th>Rating</th><th>What It Means</th><th>Example</th></tr>
            <tr>
                <td><strong>> 2.0</strong></td>
                <td><span style="color:#00ff88;">Exceptional</span></td>
                <td>Better than 99% of funds; hedge fund quality</td>
                <table>Top quant funds like Renaissance Technologies</td>
            </tr>
            <tr>
                <td><strong>1.0 - 2.0</strong></td>
                <td><span style="color:#00ff88;">Excellent</span></td>
                <td>Better than 90% of professional managers</td>
                <td>Top mutual funds and institutional portfolios</td>
            </tr>
            <tr>
                <td><strong>0.5 - 1.0</strong></td>
                <td><span style="color:#ffd700;">Good</span></td>
                <td>Above average; acceptable for most investors</td>
                <td>Well-diversified portfolio</td>
            </tr>
            <tr>
                <td><strong>0 - 0.5</strong></td>
                <td><span style="color:#ffa500;">Moderate</span></td>
                <td>Below average; returns don't justify the risk</td>
                <td>Passive index funds typically score here</td>
            </tr>
            <tr>
                <td><strong>< 0</strong></td>
                <td><span style="color:#ff1744;">Poor</span></td>
                <td>Losing money or risk outweighs returns</td>
                <td>Avoid such investments</td>
            </tr>
        </table>
        
        <div class="insight-box">
        📊 <strong>How TORO AI Uses Sharpe Ratio:</strong> The system calculates the rolling Sharpe Ratio of each stock. Higher Sharpe stocks are preferred for the watchlist. The Sharpe Ratio in Quant Analytics helps you compare which stocks have delivered the best risk-adjusted returns.
        </div>
        
        <div class="insight-box">
        💡 <strong>Pro Tip:</strong> A Sharpe Ratio above 1 is considered excellent. If a stock has Sharpe < 0.5, the risk is too high for the returns — consider alternatives.
        </div>
        
        </div>
        """, unsafe_allow_html=True)

    with st.expander("💰 What is Kelly Criterion?"):
        st.markdown("""
        <div class="quant-content">
        
        <strong>Kelly Criterion</strong> is a mathematical formula that tells you exactly how much of your capital to risk on each trade to maximize long-term growth. It was developed by John Kelly while working at Bell Labs.
        
        <div class="formula-box">
        Kelly % = (Win Rate × Win/Loss Ratio - Loss Rate) / Win/Loss Ratio
        </div>
        
        <strong>Simple Example:</strong>
        - You win 60% of your trades (Win Rate = 0.6)
        - Your average win is ₹200, average loss is ₹100 (Win/Loss Ratio = 2)
        - Kelly % = (0.6 × 2 - 0.4) / 2 = (1.2 - 0.4) / 2 = 0.8 / 2 = 0.4
        - The formula says: risk 40% of your capital on each trade
        
        <strong>Why TORO AI Uses 25% of Kelly:</strong>
        
        <table class="quant-table">
            <tr><th>Kelly Fraction</th><th>Risk Level</th><th>Suitable For</th></tr>
            <tr>
                <td><strong>100% Kelly</strong></td>
                <td>Extreme Risk</td>
                <td>Only for perfect systems with zero errors</td>
            </tr>
            <tr>
                <td><strong>50% Kelly</strong></td>
                <td>High Risk</td>
                <td>Aggressive traders with high tolerance</td>
            </tr>
            <tr>
                <td><strong>25% Kelly (TORO AI)</strong></td>
                <td><span style="color:#00ff88;">Moderate Risk</span></td>
                <td>Optimal for most traders — maximizes growth with lower drawdown</td>
            </tr>
            <tr>
                <td><strong>10% Kelly</strong></td>
                <td>Conservative Risk</td>
                <td>Beginners or capital preservation focus</td>
            </tr>
        </table>
        
        <div class="insight-box">
        📊 <strong>How TORO AI Uses Kelly Criterion:</strong> The system calculates your historical win rate and average win/loss from the stock's past returns. It then applies 25% Kelly to suggest a position size based on your ₹1,00,000 account.
        </div>
        
        <div class="insight-box">
        💡 <strong>Pro Tip:</strong> If Kelly suggests 10% position size, you should risk 10% of your capital on that trade. Never bet more than Kelly suggests — it's mathematically proven to be optimal for long-term growth.
        </div>
        
        <div class="insight-box">
        📈 <strong>Who Uses Kelly?</strong> Warren Buffett, Bill Gross (bond king), Edward Thorp (blackjack legend turned hedge fund manager), and most professional quantitative traders all use variations of the Kelly Criterion.
        </div>
        
        </div>
        """, unsafe_allow_html=True)
        
        
        # ==========================================
    # CATEGORY 4: PRO TIPS & BEST PRACTICES
    # ==========================================
    st.markdown("### 💡 PRO TIPS & BEST PRACTICES")

    with st.expander("🎯 Best Timeframes for Trading"):
        st.markdown("""
        <style>
        .tips-content {
            font-size: 12px;
            line-height: 1.5;
            color: #cbd5e1;
        }
        .tips-content strong {
            color: #00ffff;
        }
        .timeframe-table {
            font-size: 12px;
            width: 100%;
            margin: 10px 0;
            border-collapse: collapse;
        }
        .timeframe-table td, .timeframe-table th {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(0,255,255,0.1);
        }
        .timeframe-table th {
            color: #00ffff;
            text-align: left;
            font-weight: 600;
        }
        .pro-box {
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #ffd700;
            padding: 8px 12px;
            margin: 12px 0 0 0;
            font-size: 11px;
            border-radius: 0 6px 6px 0;
        }
        </style>
        
        <div class="tips-content">
        
        <strong>Choosing the right timeframe is critical for successful trading.</strong> Different timeframes reveal different market dynamics. Here's how to use each timeframe effectively:
        
        <table class="timeframe-table">
            <tr><th>Timeframe</th><th>Best For</th><th>Typical Hold Time</th><th>When to Use</th></tr>
            <tr>
                <td><strong>1D (Daily)</strong></td>
                <td>Short-term swing trading</td>
                <td>1-5 days</td>
                <td>Catching quick momentum moves, news-based trading</td>
            </tr>
            <tr>
                <td><strong>1W (Weekly)</strong></td>
                <td>Swing trading & positional</td>
                <td>1-4 weeks</td>
                <td>Following medium-term trends, avoiding daily noise</td>
            </tr>
            <tr>
                <td><strong>1M (Monthly)</strong></td>
                <td>Medium-term analysis</td>
                <td>1-3 months</td>
                <td>Identifying intermediate trends, sector rotation</td>
            </tr>
            <tr>
                <td><strong>3M (Quarterly)</strong></td>
                <td>Trend confirmation</td>
                <td>3-6 months</td>
                <td>Validating longer-term trends, reducing false signals</td>
            </tr>
            <tr>
                <td><strong>6M - 1Y</strong></td>
                <td>Long-term investment</td>
                <td>6-12 months</td>
                <td>Understanding major trends, strategic allocation</td>
            </tr>
        </table>
        
        <strong>Recommended Workflow:</strong>
        
        1. <strong>Start with 1Y timeframe</strong> → Understand the big picture, identify major support/resistance levels
        2. <strong>Switch to 3M or 6M</strong> → Confirm the trend direction
        3. <strong>Drill down to 1W or 1D</strong> → Find precise entry and exit points
        4. <strong>Use multi-timeframe alignment</strong> → Trade only when all timeframes agree
        
        <div class="pro-box">
        💡 <strong>Pro Tip:</strong> Don't trade against the 1Y trend. If the 1Y chart shows a downtrend, even 1D buy signals are more likely to fail. Always align your trading timeframe with the longer-term trend.
        </div>
        
        <div class="pro-box">
        📊 <strong>Multi-Timeframe Feature:</strong> TORO AI's Multi-Timeframe Alignment tab automatically analyzes weekly, daily, and hourly charts together. Look for 3/3 alignment (all timeframes bullish) for the highest probability trades.
        </div>
        
        </div>
        """, unsafe_allow_html=True)

    with st.expander("⚡ Trading Modes Explained"):
        st.markdown("""
        <div class="tips-content">
        
        <strong>TORO AI offers three trading modes</strong> that affect position sizing and risk tolerance. Choose the mode that matches your risk appetite and market conditions.
        
        <table class="timeframe-table">
            <tr><th>Mode</th><th>Position Size</th><th>Risk Level</th><th>Best Market Condition</th><th>Who Should Use</th></tr>
            <tr>
                <td><strong>🛡️ Conservative</strong></td>
                <td>50-70% of normal</td>
                <td><span style="color:#00ff88;">Low</span></td>
                <td>Sideways or high volatility</td>
                <td>Beginners, capital preservation, uncertain markets</td>
            </tr>
            <tr>
                <td><strong>⚡ Aggressive</strong></td>
                <td>100% of normal (baseline)</td>
                <td><span style="color:#ffd700;">Moderate</span></td>
                <td>Normal trending markets</td>
                <td>Experienced traders, normal conditions</td>
            </tr>
            <tr>
                <td><strong>🔥 Ultra Aggressive</strong></td>
                <td>150% of normal (1.5x)</td>
                <td><span style="color:#ff1744;">High</span></td>
                <td>Strong bull trends only</td>
                <td>Aggressive traders, high risk tolerance</td>
            </tr>
        </table>
        
        <strong>How Position Sizing Works:</strong>
        
        | Account Size | Conservative | Aggressive | Ultra Aggressive |
        |--------------|--------------|------------|------------------|
        | ₹50,000 | ₹25,000-35,000 risk | ₹50,000 risk | ₹75,000 risk |
        | ₹1,00,000 | ₹50,000-70,000 risk | ₹1,00,000 risk | ₹1,50,000 risk |
        | ₹5,00,000 | ₹2,50,000-3,50,000 risk | ₹5,00,000 risk | ₹7,50,000 risk |
        
        <div class="pro-box">
        ⚠️ <strong>Warning:</strong> Ultra Aggressive mode significantly increases drawdown risk. Use only when:
        - Market regime is STRONG BULL (Hurst > 0.65)
        - Your confidence in the trade is > 75%
        - You have a proven track record with the strategy
        - You can afford to lose the increased position size
        </div>
        
        <div class="pro-box">
        💡 <strong>Pro Tip:</strong> Start with Conservative mode for your first 20 trades. Once you have a winning record (>60% win rate), gradually increase to Aggressive. Use Ultra Aggressive only sparingly and only in strong trends.
        </div>
        
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📉 Risk Management Rules"):
        st.markdown("""
        <div class="tips-content">
        
        <strong>Risk management is the single most important factor in trading success.</strong> Even the best strategy will fail without proper risk controls. Follow these golden rules:
        
        <table class="timeframe-table">
            <tr><th>Rule</th><th>Why It Matters</th><th>How TORO AI Helps</th></tr>
            <tr>
                <td><strong>1% to 2% Risk Per Trade</strong></td>
                <td>Prevents catastrophic losses; one bad trade won't wipe you out</td>
                <td>AI calculates position size based on 2% risk model</td>
            </tr>
            <tr>
                <td><strong>Always Use Stop Loss</strong></td>
                <td>Limits downside; removes emotion from exits</td>
                <td>AI provides recommended stop loss levels</td>
            </tr>
            <tr>
                <td><strong>Risk-Reward ≥ 1:1.5</strong></td>
                <td>You can be wrong more often and still be profitable</td>
                <td>AI calculates risk-reward ratio before every trade</td>
            </tr>
            <tr>
                <td><strong>Reduce Size in Bear Markets</strong></td>
                <td>Bear markets have lower win rates and larger drawdowns</td>
                <td>Market Regime detection warns you automatically</td>
            </tr>
            <tr>
                <td><strong>Reduce Size in High Volatility</strong></td>
                <td>Volatile markets have wider swings; stop losses get hit more often</td>
                <td>Volatility metric (ATR %) shows you current risk level</td>
            </tr>
            <tr>
                <td><strong>Never Average Down</strong></td>
                <td>Adding to losing positions increases risk exponentially</td>
                <td>AI signals help you avoid catching falling knives</td>
            </tr>
        <table>
        
        <strong>The Mathematics of Risk Management:</strong>
        
        | Win Rate | Risk Per Trade | Max Consecutive Losses | Account Drawdown |
        |----------|---------------|----------------------|------------------|
        | 60% | 2% | 4-5 losses | 8-10% |
        | 55% | 2% | 6-7 losses | 12-14% |
        | 50% | 2% | 8-10 losses | 16-20% |
        | 50% | 5% | 8-10 losses | 40-50% (danger zone!) |
        
        <div class="pro-box">
        📊 <strong>Position Size Formula Used by TORO AI:</strong><br>
        Position Size = (Account Size × Risk Percentage) ÷ Stop Loss Distance<br>
        <br>
        Example: ₹1,00,000 account × 2% = ₹2,000 risk<br>
        Stop loss at 5% below entry → Position Size = ₹2,000 ÷ 0.05 = ₹40,000 invested
        </div>
        
        <div class="pro-box">
        💡 <strong>Pro Tip:</strong> The Kelly Criterion in Quant Analytics shows you the mathematically optimal risk percentage. For most traders, 25% Kelly (1-2% risk per trade) is the sweet spot between growth and safety.
        </div>
        
        <div class="pro-box">
        🛡️ <strong>Emergency Rules:</strong>
        - Stop trading after 3 consecutive losses (review your strategy)
        - Reduce position size by 50% after a 10% drawdown
        - Go to cash if you lose 20% of your account
        - Never trade with money you cannot afford to lose
        </div>
        
        </div>
        """, unsafe_allow_html=True)
        
    # ==========================================
    # RISK DISCLAIMER
    # ==========================================
    st.markdown("---")
    st.markdown("""
    > ⚠️ **RISK DISCLAIMER:** Trading involves substantial risk of loss. Past performance does not guarantee future results. 
    TORO AI is a quantitative analysis tool — not financial advice. Always do your own research 
    and never trade more than you can afford to lose.
    """)
    
    # Footer
    st.caption("TORO AI v2.0 | Built with Streamlit & Quantitative Mathematics")