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
import time
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
from quant_analytics import render_quant_analytics
# At the top with other imports
from indices import render_indices
from about import render_about 
from data_manager import (
    init_database,
    update_all_stocks,
    save_to_database,
    should_update,
    clear_database
)
from yfinance.exceptions import YFRateLimitError

# ==========================================
# FORCE PERMANENT DARK MODE - ADD THIS BLOCK HERE
# ==========================================
st.set_page_config(
    page_title="TORO AI",
    page_icon="🐂",
    layout="wide"
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

/* ========================================== */
/* CYBER THEME TABS - ADD THIS SECTION       */
/* ========================================== */

/* Tab container styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: linear-gradient(135deg, rgba(10,20,40,0.6), rgba(5,10,20,0.8));
    padding: 8px;
    border-radius: 12px;
    border: 1px solid rgba(0, 255, 255, 0.15);
    margin-bottom: 20px;
}

/* Individual tab styling */
.stTabs [data-baseweb="tab"] {
    height: 48px;
    padding: 0 24px;
    background: transparent;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Tab text styling */
.stTabs [data-baseweb="tab"] p {
    font-size: 14px;
    font-weight: 600;
    color: #8892b0;
    transition: all 0.3s ease;
}

/* Active tab styling */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(255, 0, 255, 0.1));
    border: 1px solid rgba(0, 255, 255, 0.4);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] p {
    color: #00ffff;
    text-shadow: 0 0 5px rgba(0, 255, 255, 0.5);
}

/* Hover effect for tabs */
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(0, 255, 255, 0.08);
    border: 1px solid rgba(0, 255, 255, 0.2);
}

.stTabs [data-baseweb="tab"]:hover p {
    color: #00e5ff;
}

/* Tab content panel styling */
.stTabs [data-baseweb="tab-panel"] {
    background: linear-gradient(135deg, rgba(10,20,40,0.3), rgba(5,10,20,0.5));
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(0, 255, 255, 0.1);
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Mobile responsive tabs */
@media (max-width: 768px) {
    .stTabs [data-baseweb="tab"] {
        padding: 0 12px;
        height: 40px;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 11px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 12px;
    }
}

/* ========================================== */
/* END OF CYBER THEME TABS                   */
/* ========================================== */

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
# SESSION STATE INITIALIZATION
# ==========================================
if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()
    
# Add these new ones:
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = None
if "selected_name" not in st.session_state:
    st.session_state.selected_name = None
if "watchlist_clicked_stock" not in st.session_state:
    st.session_state.watchlist_clicked_stock = None
if "watchlist_clicked_name" not in st.session_state:
    st.session_state.watchlist_clicked_name = None


# ==========================================
# READ STOCK FROM URL (from watchlist click or index click)
# ==========================================
query_params = st.query_params
if "stock" in query_params:
    stock = query_params["stock"]
    search = query_params.get("name", stock)
    # Clear the query params after reading to prevent re-use
    st.query_params.clear()
else:
    stock = None
    search = None

#init database (creates tables if not exist)
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
# OVERRIDE FROM INDEX CLICKS (using session state)
# ==========================================
if st.session_state.get("selected_stock"):
    stock = st.session_state.selected_stock
    search = st.session_state.selected_name
    st.session_state.selected_stock = None
    st.session_state.selected_name = None

# ==========================================
# WATCHLIST CLICK HANDLER (backward compatibility)
# ==========================================
if st.session_state.get("watchlist_clicked_stock"):
    stock = st.session_state.watchlist_clicked_stock
    search = st.session_state.watchlist_clicked_name
    st.session_state.watchlist_clicked_stock = None
    st.session_state.watchlist_clicked_name = None

# ==========================================
# FIX: Force chart refresh on stock change
# ==========================================

# Track previous stock to detect changes
if 'previous_stock' not in st.session_state:
    st.session_state.previous_stock = None


    # Reset chart initialization flag
    if 'chart_initialized' in st.session_state:
        st.session_state.chart_initialized = False
    # Update previous stock
    st.session_state.previous_stock = stock

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

# Create placeholder for data loading
data_placeholder = st.empty()

with st.spinner("📡 Fetching market data and analyzing..."):
    data = fetch_stock_data(stock, period, interval)
    
    # Show progress while loading
    if data.empty:
        data_placeholder.warning(f"⏳ Loading data for {stock}... Please wait or refresh.")
        time.sleep(1)
        st.rerun()  # Retry

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
# PROFESSIONAL TABS - 6 TABS
# ==========================================

# Create 6 professional tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧠 AI INSIGHTS",
    "🔬 QUANT ANALYTICS", 
    "📈 CHART & LEVELS",
    "📋 WATCHLIST",
    "📰 NEWS",
    "ℹ️ ABOUT"
])

# ==========================================
# TAB 1: AI INSIGHTS
# ==========================================
with tab1:
    with st.expander("🧠 AI MARKET INSIGHTS", expanded=True):
        
        # Show AI Insights
        for insight in insights:
            st.markdown(f"• {insight}")

        if not levels:
            st.warning("AI premium analysis not available for this stock.")
        else:
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

    # Ensemble Voting Results
    st.markdown("---")
    st.markdown("### 🧠 AI ENSEMBLE VOTING")
    
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
        try:
            regime_data = brain.trading_engine.detect_adaptive_regime(data)
            
            regime = regime_data.get('regime', 'UNKNOWN')
            regime_strength = regime_data.get('strength', regime_data.get('confidence', 50))
            regime_volatility = regime_data.get('volatility', 0)
            
            regime_display = {
                "TRENDING_BULL": {"text": "📈 BULLISH TREND", "color": "#00ff88"},
                "TRENDING_BEAR": {"text": "📉 BEARISH TREND", "color": "#ff1744"},
                "HIGH_VOLATILITY": {"text": "⚡ HIGH VOLATILITY", "color": "#ffa500"},
                "ACCUMULATION": {"text": "💰 ACCUMULATION", "color": "#00e5ff"},
                "SIDEWAYS": {"text": "🔄 SIDEWAYS", "color": "#ffd700"},
            }.get(regime, {"text": "📊 NEUTRAL", "color": "#8892b0"})
            
            st.markdown(f"""
            <div class="compact-box">
                <div class="compact-label">📊 MARKET REGIME</div>
                <div class="compact-value" style="color: {regime_display['color']};">{regime_display['text']}</div>
                <div class="compact-delta">Strength: {regime_strength:.0f}%</div>
                <div class="compact-sub">Volatility: {regime_volatility:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown("""
            <div class="compact-box">
                <div class="compact-label">📊 MARKET REGIME</div>
                <div class="compact-value" style="color: #ffd700;">ANALYZING</div>
                <div class="compact-delta">Please wait...</div>
            </div>
            """, unsafe_allow_html=True)

    with col_e3:
        buy_count = sum(1 for r in ensemble_result['strategy_results'] if r['signal'] == 1)
        sell_count = sum(1 for r in ensemble_result['strategy_results'] if r['signal'] == -1)
        
        st.markdown(f"""
        <div class="compact-box">
            <div class="compact-label">🗳️ STRATEGY VOTES</div>
            <div class="compact-value">🟢 {buy_count} | 🔴 {sell_count}</div>
            <div class="compact-sub">6 total strategies</div>
        </div>
        """, unsafe_allow_html=True)

    # Fibonacci Section
    st.markdown("---")
    st.markdown("<h4 style='text-align: left;'>📐 FIBONACCI RETRACEMENT LEVELS</h4>", unsafe_allow_html=True)

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
# TAB 2: QUANT ANALYTICS
# ==========================================
with tab2:
    render_quant_analytics(brain, data, levels)

# ==========================================
# TAB 3: CHART & LEVELS
# ==========================================
with tab3:
    st.subheader("⚙️ TORO Trading Terminal")
    render_chart(
        symbol=stock,
        levels=levels,
        buy_signals=buy_signals,
        sell_signals=sell_signals
    )

# ==========================================
# TAB 4: WATCHLIST
# ==========================================
with tab4:
    st.markdown("### 📋 My Watchlist")
    st.caption("Track and manage your favorite stocks")
    
    # Display watchlist
    watchlist_fragment(stocks_dict)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("""
    - **Click** on any stock symbol to instantly analyze it
    - **Add** stocks using the search bar or the ⭐ button
    - **Remove** stocks by clicking the ❌ button next to each symbol
    - **Watchlist** is saved automatically
    """)
    
    # Optional: Show watchlist statistics
    watchlist = st.session_state.get('watchlist', [])
    if watchlist:
        st.markdown("---")
        st.markdown("### 📊 Watchlist Stats")
        st.metric("Total Stocks Tracked", len(watchlist))

# ==========================================
# TAB 5: NEWS & CONTACT
# ==========================================
with tab5:
    news_target = search if search else stock
    news = get_stock_news(news_target)
    ui.render_news(news)
    ui.render_contact()

# ==========================================
# TAB 6: ABOUT TORO AI
# ==========================================
with tab6:
    render_about()

# ==========================================
# RISK WARNINGS (Safety Features)
# ==========================================
if risk_score > 70:
    st.warning("⚠️ **HIGH RISK WARNING** - Current market conditions suggest elevated risk.")
elif overall_sentiment == "BEARISH":
    st.info("📉 **Bearish Market Detected** - Consider caution.")
elif levels.get("risk_reward", 0) < 1:
    st.warning("⚠️ **Poor Risk-Reward Ratio** - Wait for better levels.")
