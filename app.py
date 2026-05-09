# ==========================================
# TORO AI - Main Application
# Full-Width Professional Layout
# ==========================================

# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# TORO AI Modules
from stocks import stocks_dict
from chart import render_chart
from news import get_stock_news
from watchlist import load_watchlist, watchlist_fragment
import ui
from backtest_engine import BacktestEngine, BacktestVisualizer
from datetime import timedelta
from brain_ultimate import ultimate_brain as brain


from data_manager import (
    init_database,
    update_all_stocks,
    save_to_database,
    should_update,
    clear_database
)


# ==========================================
# FORCE CSS TO LOAD FIRST (Fixes styling issue)
# ==========================================

# Force CSS to load immediately
st.markdown("""
<style>
/* PREMIUM BOX STYLES - LOADS FIRST */
.compact-box {
    background: linear-gradient(135deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
    border-radius: 10px;
    border: 1px solid rgba(0,255,255,0.15);
    padding: 8px 6px;
    margin: 4px 0;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,255,255,0.04);
    transition: all 0.2s ease;
}
.compact-box:hover {
    border-color: rgba(0,255,255,0.4);
    box-shadow: 0 2px 12px rgba(0,255,255,0.1);
}
.compact-label {
    font-size: 9px;
    color: #8892b0;
    letter-spacing: 0.5px;
    margin-bottom: 2px;
}
.compact-value {
    font-size: 15px;
    font-weight: 700;
    color: #00ffff;
}
.compact-value-success {
    color: #00ff88;
}
.compact-value-danger {
    color: #ff1744;
}
.compact-delta {
    font-size: 9px;
    color: #ffd700;
    margin-top: 2px;
}
.compact-sub {
    font-size: 8px;
    color: #64748b;
    margin-top: 2px;
}
.fib-compact {
    background: rgba(0,255,255,0.05);
    border-radius: 8px;
    padding: 6px 4px;
    text-align: center;
    border: 1px solid rgba(0,255,255,0.1);
}
.fib-label {
    font-size: 7px;
    color: #8892b0;
}
.fib-value {
    font-size: 11px;
    font-weight: 600;
    color: #ffd700;
}

/* Make sure all boxes display properly */
.stMarkdown {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# ENHANCED RESPONSIVE CSS (Mobile + Desktop)
# ==========================================
st.markdown("""
<style>
/* --------------------------------------------------- */
/* 1. DESKTOP DEFAULT STYLES (applies to all devices) */
/* --------------------------------------------------- */
.compact-box {
    background: linear-gradient(135deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
    border-radius: 10px;
    border: 1px solid rgba(0,255,255,0.15);
    padding: 8px 6px;
    margin: 4px 0;
    text-align: center;
    transition: all 0.2s ease;
}

/* --------------------------------------------------- */
/* 2. TABLET STYLES (600px to 768px) - 2 COLUMNS */
/* --------------------------------------------------- */
@media (min-width: 600px) and (max-width: 768px) {
    /* Make containers 2-column grid */
    .stHorizontalBlock {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
    }
    
    /* Ensure individual columns take full width of grid cell */
    div[data-testid="column"] {
        width: 100% !important;
        margin: 0 !important;
    }
    
    /* Adjust text sizes for tablet */
    .compact-value {
        font-size: 15px !important;
    }
    .compact-label {
        font-size: 11px !important;
    }
    .compact-sub {
        font-size: 9px !important;
    }
    
    /* Make buttons tablet-friendly */
    button, .stButton button {
        min-height: 44px !important;
        font-size: 13px !important;
    }
    
    /* Adjust chart height for tablet */
    .stPlotlyChart, iframe {
        height: 380px !important;
    }
    
    /* Adjust sidebar width */
    section[data-testid="stSidebar"] {
        width: 300px !important;
    }
    
    /* Fibonacci boxes on tablet */
    .fib-compact {
        padding: 5px 3px !important;
    }
    .fib-value {
        font-size: 11px !important;
    }
}

/* --------------------------------------------------- */
/* 3. LARGE TABLET (769px to 1024px) */
/* --------------------------------------------------- */
@media (min-width: 769px) and (max-width: 1024px) {
    .compact-value {
        font-size: 13px !important;
    }
    .stPlotlyChart {
        height: 400px !important;
    }
    button, .stButton button {
        min-height: 44px !important;
    }
}

/* --------------------------------------------------- */
/* 4. SMALL PHONES (max-width: 599px) - 1 COLUMN */
/* --------------------------------------------------- */
@media (max-width: 599px) {
   
    /* ----- Text and Fonts ----- */
    .compact-value, .compact-value-success, .compact-value-danger {
        font-size: 14px !important;
    }
    .compact-label {
        font-size: 10px !important;
    }
    .compact-sub, .compact-delta {
        font-size: 8px !important;
    }
    .stMarkdown, .stText, .stCaption {
        font-size: 13px !important;
    }
    .premium-metric-value {
        font-size: 18px !important;
    }
    .streamlit-expanderHeader {
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        min-height: 48px !important;
    }
    .fib-label {
        font-size: 6px !important;
    }
    .fib-value {
        font-size: 10px !important;
    }

    /* ----- Buttons (Touch-friendly) ----- */
    button, .stButton button, div[data-testid="stButton"] button {
        min-height: 48px !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        width: 100% !important;
    }

    /* ----- Layout & Containers ----- */
    .block-container {
        padding: 0.5rem 0.8rem !important;
    }
    .main > div {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .stHorizontalBlock {
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        margin-bottom: 8px !important;
    }
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }

    /* ----- CHARTS (TradingView Lightweight Charts) ----- */
    #chart-container {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Make chart touch-friendly */
    .legend-item, .modebar-btn {
        min-width: 32px !important;
        min-height: 32px !important;
    }
    
    /* Improve crosshair and tooltips */
    .hoverlayer {
        font-size: 10px !important;
    }
    
    /* Price scale readability */
    .price-scale-indicator {
        font-size: 9px !important;
    }

    /* ----- DataFrames ----- */
    .stDataFrame {
        overflow-x: auto !important;
        max-width: 100% !important;
    }

    /* ----- Specific Components ----- */
    .premium-metric-box {
        padding: 8px 4px !important;
        margin: 4px 0 !important;
    }
    .premium-metric-status {
        font-size: 9px !important;
        padding: 2px 6px !important;
    }
    .fib-compact {
        padding: 4px 2px !important;
    }
    .streamlit-expanderContent {
        padding: 8px !important;
    }
    .info-bar {
        font-size: 7px !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
    }
    .watchlist-item {
        padding: 10px !important;
        margin: 5px 0 !important;
    }
}

/* --------------------------------------------------- */
/* 5. VERY SMALL PHONES (max-width: 480px) */
/* --------------------------------------------------- */
@media (max-width: 480px) {
    .compact-value, .compact-value-success, .compact-value-danger {
        font-size: 12px !important;
    }
    .compact-label {
        font-size: 9px !important;
    }
    .premium-metric-value {
        font-size: 16px !important;
    }
    .premium-metric-status {
        font-size: 7px !important;
        padding: 1px 4px !important;
    }
}
</style>
""", unsafe_allow_html=True)



# ==========================================
# PAGE CONFIG - MUST BE FIRST
# ==========================================

st.set_page_config(
    page_title="TORO AI",
    page_icon="🐂",
    layout="wide"
)

init_database()


# ==========================================
# MOBILE DETECTION
# ==========================================
def detect_mobile():
    """Detect if user is on mobile device"""
    try:
        # Check user agent from Streamlit headers
        import streamlit as st
        headers = st.context.headers
        user_agent = headers.get('User-Agent', '')
        
        mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'iPod', 'BlackBerry', 'Windows Phone']
        return any(keyword in user_agent for keyword in mobile_keywords)
    except:
        return False

if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = detect_mobile()
    

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()
    
# Initialize session state for backtest page
if 'show_backtest_page' not in st.session_state:
    st.session_state['show_backtest_page'] = False

if 'trading_mode' not in st.session_state:
    st.session_state['trading_mode'] = "Aggressive"


# ==========================================
# SAFE CACHED DATA FETCHER
# ==========================================
import time
from yfinance.exceptions import YFRateLimitError

@st.cache_data(ttl=300)
def fetch_stock_data(stock, period, interval):
    """Fetch stock data safely"""

    max_retries = 3

    for attempt in range(max_retries):

        try:
            ticker = yf.Ticker(stock)

            data = ticker.history(
                period=period,
                interval=interval,
                auto_adjust=True,
                prepost=False
            )

            if not data.empty:
                data = brain.calculate_all_indicators(data)

            return data

        except YFRateLimitError:

            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                st.warning("⚠️ Yahoo Finance rate limit reached. Please wait a moment and try again.")
                return pd.DataFrame()

        except Exception as e:
            st.error(f"Data fetch error: {str(e)}")
            return pd.DataFrame()

    return pd.DataFrame()


# ==========================================
# TIMEFRAME CONFIGURATION
# ==========================================
TIMEFRAMES = {
    "1D": {"interval": "5m", "period": "1d"},
    "1W": {"interval": "15m", "period": "5d"},
    "1M": {"interval": "1h", "period": "1mo"},
    "3M": {"interval": "1d", "period": "3mo"},
    "6M": {"interval": "1d", "period": "6mo"},
    "1Y": {"interval": "1d", "period": "1y"},
}
DEFAULT_TIMEFRAME = "1Y"


# ==========================================
# UI HEADER
# ==========================================
ui.render_header()


# ==========================================
# MOBILE OPTIMIZATION
# ==========================================
if st.session_state.get('is_mobile', False):
    # Hide less important elements on mobile
    st.markdown("""
    <style>
    /* Hide some decorative elements on mobile */
    .info-bar span:last-child {
        display: none;
    }
    /* Make chart labels smaller */
    .hoverlayer text {
        font-size: 9px !important;
    }
    </style>
    """, unsafe_allow_html=True)



# ==========================================
# SIDEBAR - Responsive (Mobile/Desktop)
# ==========================================
with st.sidebar:
    
    if st.session_state.get('is_mobile', False):
        # ==========================================
        # MOBILE: Compact Sidebar with Toggle
        # ==========================================
        if st.button("☰ MENU", use_container_width=True):
            st.session_state.show_mobile_menu = not st.session_state.get('show_mobile_menu', False)
        
        if st.session_state.get('show_mobile_menu', False):
            # Data Control
            st.markdown("### 🔄 Data")
            if st.button("📥 Update", use_container_width=True):
                progress_bar = st.progress(0)
                with st.spinner("Updating..."):
                    stocks_list = list(set(stocks_dict.values()))
                    def progress_callback(done, total):
                        progress_bar.progress(done / total)
                    results = update_all_stocks(stocks_list, max_workers=2, progress_callback=progress_callback)
                    if len(results) > 0:
                        save_to_database(results)
                        st.success(f"✅ Updated {len(results)} stocks!")
                    else:
                        st.error("❌ No data fetched")
                st.rerun()
            
            st.markdown("---")
            
            # Trading Mode
            st.markdown("### 🎯 Mode")
            st.session_state['trading_mode'] = st.selectbox(
                "Strategy",
                ["Conservative", "Aggressive", "Ultra Aggressive"],
                index=["Conservative", "Aggressive", "Ultra Aggressive"].index(
                    st.session_state['trading_mode']
                ),
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # Backtest
            st.markdown("### ⏱️ Backtest")
            if st.button("📊 Launch", use_container_width=True, key="open_backtest"):
                st.session_state['show_backtest_page'] = True
                st.rerun()
            st.caption("Historical performance")
            
            st.markdown("---")
            
            # Watchlist
            st.markdown("### 📋 Watchlist")
            watchlist_fragment(stocks_dict)
            
            st.markdown("---")
            
            # System Status
            st.markdown("### ⚡ Status")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.caption("Brain")
                st.caption("✅ Active")
            with col_s2:
                st.caption("Kalman")
                st.caption("✅ On")
    
    else:
        
        # ==========================================
        # SIDEBAR - PROFESSIONAL COMPACT LAYOUT
        # ==========================================
        with st.sidebar:
        
            # ==========================================
            # DATA CONTROL (Compact with Admin Protection)
            # ==========================================
            # ==========================================
            # DATA CONTROL (Combined Horizontal)
            # ==========================================
            col_d1, col_d2 = st.columns(2)

            with col_d1:
                if st.button("🔄 Update", use_container_width=True, help="Update Market Data"):
                    progress_bar = st.progress(0)
                    with st.spinner("Updating..."):
                        stocks_list = list(set(stocks_dict.values()))
                        def progress_callback(done, total):
                            progress_bar.progress(done / total)
                        results = update_all_stocks(stocks_list, max_workers=2, progress_callback=progress_callback)
                        if len(results) > 0:
                            save_to_database(results)
                            st.success(f"✅ {len(results)} stocks")
                        else:
                            st.error("❌ No data")
                    st.rerun()

            with col_d2:
                if st.button("🗑️ Clear", use_container_width=True, help="Clear Cache (Admin Only)"):
                    with st.popover("🔐 Admin Verification"):
                        admin_password = st.text_input("Password", type="password", key="admin_clear_pass")
                        if admin_password:
                            if admin_password == "TORO_ADMIN_2024":
                                st.cache_data.clear()
                                st.success("✅ Cache cleared!")
                                st.rerun()
                            else:
                                st.error("❌ Wrong password!")
            
            # ==========================================
            # TRADING MODE
            # ==========================================
            st.selectbox(
                "",
                ["Conservative", "Aggressive", "Ultra Aggressive"],
                index=["Conservative", "Aggressive", "Ultra Aggressive"].index(
                    st.session_state.get('trading_mode', "Aggressive")
                ),
                label_visibility="collapsed",
                key="mode_selector"
            )
            
            # ==========================================
            # BACKTEST
            # ==========================================
            if st.button("📊 Backtest", use_container_width=True, key="open_backtest"):
                st.session_state['show_backtest_page'] = True
                st.rerun()
            
            # ==========================================
            # WATCHLIST
            # ==========================================
            st.markdown("### 📋 Watchlist")
            watchlist_fragment(stocks_dict)
            
            # ==========================================
            # SYSTEM STATUS
            # ==========================================
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("🧠 **Brain**")
                st.caption("Active")
            with col_s2:
                st.markdown("📉 **Kalman**")
                st.caption("On")


# ==========================================
# STOCK SEARCH 
# ==========================================
search, stock = ui.render_search_section(stocks_dict)


# ==========================================
# WATCHLIST CLICK HANDLER
# ==========================================
if "watchlist_clicked_stock" in st.session_state and st.session_state.watchlist_clicked_stock:
    stock = st.session_state.watchlist_clicked_stock
    search = st.session_state.watchlist_clicked_name
    st.session_state.watchlist_clicked_stock = None
    st.session_state.watchlist_clicked_name = None



# ==========================================
# VALIDATE STOCK SELECTION
# ==========================================
if not stock:
    st.stop()

# ==========================================
# FETCH MARKET DATA
# ==========================================
interval = TIMEFRAMES[DEFAULT_TIMEFRAME]["interval"]
period = TIMEFRAMES[DEFAULT_TIMEFRAME]["period"]

with st.spinner("📡 Fetching market data and analyzing..."):
    data = fetch_stock_data(stock, period, interval)
    

if data.empty:
    st.error(f"⚠️ No data available for {stock}")
    st.stop()


# ==========================================
# INTELLIGENT ANALYSIS (Brain at Work)
# ==========================================
buy_signals, sell_signals, signal_score, overall_sentiment, confidence, risk_score = brain.generate_smart_signals(data)
levels = brain.calculate_advanced_risk_levels(data)

# ==========================================
# PAGE ROUTING
# ==========================================

if st.session_state.get('show_backtest_page', False):
    # Show backtest page
    from backtest_page import render_backtest_page
    render_backtest_page(brain, stock)
    st.stop()

insights = brain.generate_actionable_insights(data, levels, buy_signals, sell_signals)
recommendation, rec_confidence = brain.get_trading_recommendation(overall_sentiment, confidence, risk_score, levels)


# ==========================================
# UNIFIED TRADING MODE LOGIC (Using Ultimate Brain Only)
# ==========================================

# Get ensemble analysis (includes confidence and action)
ensemble_result = brain.get_ensemble_analysis(data, levels)
signal_value = ensemble_result['signal']

# Apply position size boost for Ultra Aggressive mode
if st.session_state['trading_mode'] == "Ultra Aggressive" and signal_value == 1:
    if levels:
        levels['position_size'] = levels.get('position_size', 0) * 1.5
        levels['risk_amount'] = levels.get('risk_amount', 0) * 1.5

# Show unified confidence display
st.caption(f"🎯 {ensemble_result['action']} | Confidence: {ensemble_result['confidence']}% | {ensemble_result['vote_summary']}")


# ==========================================
# ADD SIGNAL TO DATAFRAME (Single source of truth)
# ==========================================
data["Signal"] = 0
data.iloc[-1, data.columns.get_loc("Signal")] = signal_value


# ==========================================
# METRICS - USING YOUR ORIGINAL UI FUNCTION
# ==========================================
ui.render_metrics(data, buy_signals, sell_signals, stock)


# ==========================================
# AI MARKET INSIGHTS (6 Compact Premium Boxes)
# ==========================================

with st.expander("🧠 AI MARKET INSIGHTS", expanded=True):

    # Show AI Insights
    for insight in insights:
        st.markdown(f"• {insight}")

    if not levels:
        st.warning("AI premium analysis not available for this stock.")
        st.stop()

    st.markdown("---")

    # Safe get function
    def get_val(key, default=0):
        val = levels.get(key, default)
        if val is None or (isinstance(val, float) and val != val):
            return default
        return val

    # Extract values
    entry = get_val("entry", 0)
    stoploss = get_val("stoploss", 0)
    target = get_val("target", 0)
    risk_amt = get_val("risk_amount", 0)
    reward_amt = get_val("reward_amount", 0)
    rr = get_val("risk_reward", 0)
    position_size = get_val("position_size", 0)
    volatility = levels.get("volatility", "NORMAL")
    fib_382 = get_val("fib_382", 0)
    fib_500 = get_val("fib_500", 0)
    fib_618 = get_val("fib_618", 0)

    # Risk-Reward explanation
    if rr >= 2:
        rr_text = "Excellent"
    elif rr >= 1.5:
        rr_text = "Good"
    elif rr >= 1:
        rr_text = "Okay"
    else:
        rr_text = "Poor"

    # Volatility text
    if volatility == "HIGH":
        vol_text = "Use smaller positions"
    elif volatility == "LOW":
        vol_text = "Normal positions"
    else:
        vol_text = "Standard risk"

    # Row 1: Entry, Stop Loss, Target
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🎯 ENTRY</div>
            <div class="compact-value">₹{entry:.2f}</div>
            <div class="compact-sub">Ideal buy price</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🛑 STOP LOSS</div>
            <div class="compact-value compact-value-danger">₹{stoploss:.2f}</div>
            <div class="compact-sub">Exit if below</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🏁 TARGET</div>
            <div class="compact-value compact-value-success">₹{target:.2f}</div>
            <div class="compact-sub">Book profit here</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Risk/Reward, Position Size, Volatility
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">📈 RISK → REWARD</div>
            <div class="compact-value">₹{risk_amt:.0f} → ₹{reward_amt:.0f}</div>
            <div class="compact-delta">1 : {rr:.1f} ({rr_text})</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">💰 POSITION SIZE</div>
            <div class="compact-value">{position_size:.0f} shares</div>
            <div class="compact-sub">₹1L account · 2% risk</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        color = "#ff1744" if volatility == "HIGH" else "#ffd700" if volatility == "LOW" else "#00ffff"
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">⚡ VOLATILITY</div>
            <div class="compact-value" style="color: {color};">{volatility}</div>
            <div class="compact-sub">{vol_text}</div>
        </div>
        """, unsafe_allow_html=True)



     # ==========================================
    # MULTI-TIMEFRAME ALIGNMENT (SAME SIZE AS OTHER BOXES)
    # ==========================================
    st.markdown("---")
    st.markdown("<div style='font-size: 10px; color: #8892b0; margin-bottom: 8px; text-align: center;'>🕐 MULTI-TIMEFRAME ALIGNMENT</div>", unsafe_allow_html=True)

    try:
        mtf_result = brain.get_multi_timeframe_analysis(stock)
        
        # Row 3: Weekly, Daily, Hourly (SAME 3-column layout as Entry/Stop/Target)
        col7, col8, col9 = st.columns(3)
        
        # WEEKLY BOX
        weekly = mtf_result['timeframes'].get('Weekly', {})
        with col7:
            weekly_dir = weekly.get('direction', 'NEUTRAL')
            weekly_symbol = weekly.get('symbol', '🔄')
            weekly_conf = weekly.get('confidence', 50)
            
            if weekly_dir == 'BULLISH':
                weekly_color = "#00ff88"
                weekly_status = "BULLISH"
            elif weekly_dir == 'BEARISH':
                weekly_color = "#ff1744"
                weekly_status = "BEARISH"
            else:
                weekly_color = "#ffd700"
                weekly_status = "NEUTRAL"
            
            st.markdown(f"""
            <div class="compact-box">
                <div class="compact-label">📅 WEEKLY</div>
                <div class="compact-value" style="color: {weekly_color};">{weekly_symbol} {weekly_status}</div>
                <div class="compact-sub">Confidence: {weekly_conf:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # DAILY BOX
        daily = mtf_result['timeframes'].get('Daily', {})
        with col8:
            daily_dir = daily.get('direction', 'NEUTRAL')
            daily_symbol = daily.get('symbol', '🔄')
            daily_conf = daily.get('confidence', 50)
            
            if daily_dir == 'BULLISH':
                daily_color = "#00ff88"
                daily_status = "BULLISH"
            elif daily_dir == 'BEARISH':
                daily_color = "#ff1744"
                daily_status = "BEARISH"
            else:
                daily_color = "#ffd700"
                daily_status = "NEUTRAL"
            
            st.markdown(f"""
            <div class="compact-box">
                <div class="compact-label">📊 DAILY</div>
                <div class="compact-value" style="color: {daily_color};">{daily_symbol} {daily_status}</div>
                <div class="compact-sub">Confidence: {daily_conf:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # HOURLY BOX
        hourly = mtf_result['timeframes'].get('Hourly', {})
        with col9:
            hourly_dir = hourly.get('direction', 'NEUTRAL')
            hourly_symbol = hourly.get('symbol', '🔄')
            hourly_conf = hourly.get('confidence', 50)
            
            if hourly_dir == 'BULLISH':
                hourly_color = "#00ff88"
                hourly_status = "BULLISH"
            elif hourly_dir == 'BEARISH':
                hourly_color = "#ff1744"
                hourly_status = "BEARISH"
            else:
                hourly_color = "#ffd700"
                hourly_status = "NEUTRAL"
            
            st.markdown(f"""
            <div class="compact-box">
                <div class="compact-label">⏰ HOURLY</div>
                <div class="compact-value" style="color: {hourly_color};">{hourly_symbol} {hourly_status}</div>
                <div class="compact-sub">Confidence: {hourly_conf:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        # FINAL VERDICT (below the 3 boxes)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(0,255,255,0.08), rgba(255,0,255,0.08));
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            margin-top: 8px;
        ">
            <span style="font-size: 10px; color: #00ffff;">🎯 {mtf_result.get('agreement', '0/3')} → </span>
            <span style="font-size: 12px; font-weight: 700; color: {mtf_result.get('action_color', '#ffd700')};">{mtf_result.get('final_action', 'HOLD')}</span>
            <span style="font-size: 10px; color: #64748b;"> (Overall {mtf_result.get('final_score', 50):.0f}%)</span>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🕐 MULTI-TIMEFRAME</div>
            <div class="compact-value" style="font-size: 12px;">Loading...</div>
            <div class="compact-sub">{str(e)[:30]}</div>
        </div>
        """, unsafe_allow_html=True)


    # Fibonacci Section
    st.markdown("---")
    st.markdown("<div style='text-align: center; font-size: 10px; color: #8892b0; margin-bottom: 8px;'>📐 FIBONACCI RETRACEMENT LEVELS</div>", unsafe_allow_html=True)

    fcol1, fcol2, fcol3 = st.columns(3)

    with fcol1:
        st.markdown(f"""
        <div class="fib-compact">
            <div class="fib-label">38.2%</div>
            <div class="fib-value">₹{fib_382:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with fcol2:
        st.markdown(f"""
        <div class="fib-compact">
            <div class="fib-label">50%</div>
            <div class="fib-value">₹{fib_500:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with fcol3:
        st.markdown(f"""
        <div class="fib-compact">
            <div class="fib-label">61.8%</div>
            <div class="fib-value">₹{fib_618:.2f}</div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# ENSEMBLE VOTING RESULTS (6 Strategies)
# ==========================================
st.markdown("---")
st.markdown("### 🧠AI ENSEMBLE VOTING")

# Get ensemble analysis from all 6 strategies
ensemble_result = brain.get_ensemble_analysis(data, levels)

# Display main result
col_e1, col_e2, col_e3 = st.columns(3)

with col_e1:
    action = ensemble_result['action']
    confidence = ensemble_result['confidence']
    
    if "STRONG_BUY" in action:
        action_color = "#00ff88"
        action_icon = "✅"
    elif "BUY" in action:
        action_color = "#7cfc00"
        action_icon = "📈"
    elif "STRONG_SELL" in action:
        action_color = "#ff1744"
        action_icon = "❌"
    elif "SELL" in action:
        action_color = "#ff5252"
        action_icon = "📉"
    else:
        action_color = "#ffd700"
        action_icon = "⚠️"
    
    st.markdown(f"""
    <div class="compact-box">
        <div class="compact-label">{action_icon} FINAL VERDICT</div>
        <div class="compact-value" style="color: {action_color};">{action}</div>
        <div class="compact-delta">Confidence: {confidence}%</div>
        <div class="compact-sub">{ensemble_result['vote_summary']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_e2:
    regime = brain.regime_detector.detect(data)
    if regime == "BULL_TRENDING":
        regime_color = "#00ff88"
        regime_icon = "📈"
    elif regime == "BEAR_FALLING":
        regime_color = "#ff1744"
        regime_icon = "📉"
    elif regime == "HIGH_VOLATILITY":
        regime_color = "#ffa500"
        regime_icon = "⚡"
    else:
        regime_color = "#ffd700"
        regime_icon = "🔄"
    
    st.markdown(f"""
    <div class="compact-box">
        <div class="compact-label">{regime_icon} MARKET REGIME</div>
        <div class="compact-value" style="color: {regime_color};">{regime}</div>
        <div class="compact-sub">6-strategy voting active</div>
    </div>
    """, unsafe_allow_html=True)

with col_e3:
    # Count how many strategies agreed
    buy_count = sum(1 for r in ensemble_result['strategy_results'] if r['signal'] == 1)
    sell_count = sum(1 for r in ensemble_result['strategy_results'] if r['signal'] == -1)
    
    st.markdown(f"""
    <div class="compact-box">
        <div class="compact-label">🗳️ STRATEGY VOTES</div>
        <div class="compact-value">🟢 {buy_count} | 🔴 {sell_count}</div>
        <div class="compact-sub">6 total strategies</div>
    </div>
    """, unsafe_allow_html=True)


# Show individual strategy results
with st.expander("⚙️Ensemble Voting Breakdown"):
    for strategy in ensemble_result['strategy_results']:
        if strategy['signal'] == 1:
            icon = "🟢"
            signal_text = "BUY"
            signal_color = "#00ff88"
        elif strategy['signal'] == -1:
            icon = "🔴"
            signal_text = "SELL"
            signal_color = "#ff1744"
        else:
            icon = "⚪"
            signal_text = "NEUTRAL"
            signal_color = "#ffd700"
        
        # ✅ FIXED: Use st.markdown with proper HTML
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid {signal_color};
        ">
            <b>{icon} {strategy['name']}</b>
            <span style="float: right;">{signal_text} ({strategy['confidence']:.0f}%)</span>
            <div style="font-size: 11px; color: #64748b; margin-top: 5px;">
                {' • '.join(strategy['reasons'][:2]) if strategy['reasons'] else 'No specific reason'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show final vote summary - Fixed HTML structure
    st.markdown(
        f"""
        <div style="
            background: rgba(0,255,255,0.05);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
            margin-top: 10px;
        ">
            <b>Final:</b> {ensemble_result['vote_summary']} → {ensemble_result['action']} ({ensemble_result['confidence']:.0f}% confidence)
        </div>
        """,
        unsafe_allow_html=True
    )

# Show key reasons
with st.expander("⚡Trade Logic Analysis"):
    for reason in ensemble_result['reasons'][:5]:
        st.markdown(f"• {reason}")


# ==========================================
# ADVANCED MATHEMATICS (Expandable)
# ==========================================
with st.expander("📊QUANT ANALYTICS", expanded=False):
    
    # ==========================================
    # QUANTITATIVE INTELLIGENCE
    # ==========================================
    quant_metrics = brain.calculate_quantitative_metrics(data, levels)
    
    st.markdown("<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>📊 QUANTITATIVE INTELLIGENCE</div>", unsafe_allow_html=True)
    
    q_col1, q_col2, q_col3 = st.columns(3)
    
    with q_col1:
        win_prob = quant_metrics['win_probability']
        sample_size = quant_metrics['sample_size']
        
        if win_prob >= 70:
            prob_color = "#00ff88"
            prob_text = "High Probability"
        elif win_prob >= 60:
            prob_color = "#ffd700"
            prob_text = "Good Probability"
        elif win_prob >= 50:
            prob_color = "#ffa500"
            prob_text = "Moderate"
        else:
            prob_color = "#ff1744"
            prob_text = "Low Probability"
        
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🎲 WIN PROBABILITY</div>
            <div class="compact-value" style="color: {prob_color};">{win_prob}%</div>
            <div class="compact-delta">{prob_text}</div>
            <div class="compact-sub">Based on {sample_size} patterns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with q_col2:
        exp_value = quant_metrics['expected_value']
        
        if exp_value > 1:
            ev_color = "#00ff88"
            ev_text = "Strong Positive"
        elif exp_value > 0:
            ev_color = "#ffd700"
            ev_text = "Slightly Positive"
        elif exp_value > -1:
            ev_color = "#ffa500"
            ev_text = "Slightly Negative"
        else:
            ev_color = "#ff1744"
            ev_text = "Strong Negative"
        
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">💰 EXPECTED VALUE</div>
            <div class="compact-value" style="color: {ev_color};">{exp_value:+.2f}%</div>
            <div class="compact-delta">{ev_text}</div>
            <div class="compact-sub">Avg return per trade</div>
        </div>
        """, unsafe_allow_html=True)
    
    with q_col3:
        verdict = quant_metrics['verdict']
        message = quant_metrics['message']
        
        if verdict == "STRONG BUY":
            verdict_color = "#00ff88"
            verdict_icon = "✅"
        elif verdict == "BUY":
            verdict_color = "#7cfc00"
            verdict_icon = "📈"
        elif verdict == "CONSIDER":
            verdict_color = "#ffd700"
            verdict_icon = "⚠️"
        elif verdict == "AVOID":
            verdict_color = "#ff1744"
            verdict_icon = "❌"
        else:
            verdict_color = "#8892b0"
            verdict_icon = "⚡"
        
        short_message = message[:35] + "..." if len(message) > 35 else message
        
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">{verdict_icon} AI VERDICT</div>
            <div class="compact-value" style="color: {verdict_color};">{verdict}</div>
            <div class="compact-delta">{short_message}</div>
            <div class="compact-sub">Math-based decision</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
        
    # ==========================================
    # MONTE CARLO SIMULATION (FIXED)
    # ==========================================
    st.markdown("<div style='font-size: 11px; color: #8892b0; margin-bottom: 10px;'>🎲 MONTE CARLO SIMULATION</div>", unsafe_allow_html=True)

    current_price = data["Close"].iloc[-1]
    target_price = levels.get("target", current_price * 1.05)
    stoploss_price = levels.get("stoploss", current_price * 0.98)

    try:
        from advanced_math import MonteCarloSimulator
        mc = MonteCarloSimulator()
        monte_carlo_results = mc.run_simulation(data, current_price, target_price, stoploss_price)
        
        if monte_carlo_results:
            st.markdown(f"<div style='font-size: 10px; color: #64748b; margin-bottom: 10px;'>📊 Based on {monte_carlo_results.get('n_paths', 5000):,} simulated scenarios</div>", unsafe_allow_html=True)
            
            mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
            
            with mc_col1:
                prob_target = monte_carlo_results.get('prob_target', 50)
                color = "#00ff88" if prob_target >= 60 else "#ffd700" if prob_target >= 50 else "#ff1744"
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">🎯 HIT TARGET</div>
                    <div class="compact-value" style="color: {color};">{prob_target}%</div>
                    <div class="compact-sub">Probability</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc_col2:
                prob_stop = monte_carlo_results.get('prob_stoploss', 50)
                color_stop = "#ff1744" if prob_stop > 30 else "#ffd700"
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">🛑 HIT STOP LOSS</div>
                    <div class="compact-value" style="color: {color_stop};">{prob_stop}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc_col3:
                exp_return = monte_carlo_results.get('mean_return', 0)
                return_color = "#00ff88" if exp_return > 0 else "#ff1744"
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">📈 EXPECTED RETURN</div>
                    <div class="compact-value" style="color: {return_color};">{exp_return:+.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with mc_col4:
                sharpe = monte_carlo_results.get('sharpe', 0)
                adj_color = "#00ff88" if sharpe > 0.5 else "#ffd700" if sharpe > 0 else "#ff1744"
                st.markdown(f"""
                <div class="compact-box">
                    <div class="compact-label">⚡ SHARPE RATIO</div>
                    <div class="compact-value" style="color: {adj_color};">{sharpe:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Best/Worst case - FIXED
            with st.expander("📊 View Best & Worst Case Scenarios"):
                bc_col1, bc_col2 = st.columns(2)
                
                # Calculate percentage returns
                p95_price = monte_carlo_results.get('price_percentiles', {}).get('p95', current_price)
                p5_price = monte_carlo_results.get('price_percentiles', {}).get('p5', current_price)
                
                best_return = ((p95_price - current_price) / current_price) * 100
                worst_return = ((p5_price - current_price) / current_price) * 100
                
                with bc_col1:
                    st.metric("🚀 BEST CASE", f"+{best_return:.1f}%")
                    st.caption(f"Target (95th percentile): ₹{p95_price:.2f}")
                
                with bc_col2:
                    st.metric("⚠️ WORST CASE", f"{worst_return:.1f}%")
                    st.caption(f"Stop (5th percentile): ₹{p5_price:.2f}")
        else:
            st.info("📊 Monte Carlo: Need more data for simulation")
            
    except Exception as e:
        st.info(f"📊 Monte Carlo simulation unavailable")
    
    
    # ==========================================
    # KALMAN FILTER STATUS (Noise Reduction)
    # ==========================================
    st.markdown("---")
    with st.expander("📉 Kalman Filter (Noise Reduction)", expanded=False):
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
            border-radius: 10px;
            padding: 12px;
            margin: 5px 0;
            border-left: 3px solid #00ffff;
        ">
            <div style="font-size: 11px; color: #00ffff; margin-bottom: 8px;">
                🔄 What is Kalman Filter?
            </div>
            <div style="font-size: 10px; color: #94a3b8; margin-bottom: 8px;">
                Removes market "noise" (random price wiggles) to reveal the true trend.
                Used by hedge funds and institutional traders.
            </div>
            <div style="font-size: 9px; color: #64748b;">
                Status: <span style="color: #00ff88;">✓ ACTIVE</span> - Smoothing price, RSI, and MACD signals
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show before/after comparison if data available
        if 'Close_Kalman' in data.columns:
            st.markdown("---")
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.metric("Raw Price", f"₹{data['Close'].iloc[-1]:.2f}")
            with col_k2:
                st.metric("Kalman Smoothed", f"₹{data['Close_Kalman'].iloc[-1]:.2f}", 
                         delta=f"Difference: ₹{data['Close_Kalman'].iloc[-1] - data['Close'].iloc[-1]:+.2f}")
                
                
                
# Add explanation if data is insufficient
if quant_metrics.get('sample_size', 0) == 0:
    st.caption("📊 *Need more historical data for accurate quantitative analysis. Keep using TORO AI daily!*")


# ==========================================
# PROFESSIONAL CHART - FULL WIDTH
# ==========================================
st.subheader("⚙️TORO Trading Terminal")
render_chart(
    symbol=stock,
    levels=levels,
    buy_signals=buy_signals,
    sell_signals=sell_signals
)


# ==========================================
# RISK WARNINGS (Safety Features)
# ==========================================
if risk_score > 70:
    st.warning("⚠️ **HIGH RISK WARNING** - Current market conditions suggest elevated risk.")
elif overall_sentiment == "BEARISH":
    st.info("📉 **Bearish Market Detected** - Consider caution.")
elif levels.get("risk_reward", 0) < 1:
    st.warning("⚠️ **Poor Risk-Reward Ratio** - Wait for better levels.")


# ==========================================
# MARKET NEWS
# ==========================================
news_target = search if search else stock
news = get_stock_news(news_target)
ui.render_news(news)


# ==========================================
# CONTACT & FOOTER
# ==========================================
ui.render_contact()
