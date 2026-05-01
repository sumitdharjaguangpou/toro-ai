# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
from urllib.parse import quote_plus

from signals import getsignal
from news import get_stock_news
from stocks import stocks_dict
from charts import plot_price_chart
from watchlist import load_watchlist, watchlist_fragment
import ui
import screener


# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="TORO AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# SESSION STATE
# ==========================================
if "screener_running" not in st.session_state:
    st.session_state.screener_running = False

if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()


# ==========================================
# CACHE STOCK DATA
# ==========================================
@st.cache_data(ttl=300)
def fetch_stock_data(stock, period, interval):
    ticker = yf.Ticker(stock)
    return ticker.history(period=period, interval=interval)


# ==========================================
# HEADER
# ==========================================
ui.render_header()


# ==========================================
# SIDEBAR WATCHLIST
# ==========================================
with st.sidebar:
    st.markdown("## 📋 Watchlist")
    watchlist_fragment(stocks_dict)
    st.markdown("---")


# ==========================================
# SEARCH + SCREENER
# ==========================================
search, stock, screener_clicked = ui.render_search_section(stocks_dict)


# ==========================================
# WATCHLIST CLICK SUPPORT
# ==========================================
if (
    "watchlist_clicked_stock" in st.session_state
    and st.session_state.watchlist_clicked_stock
):
    stock = st.session_state.watchlist_clicked_stock
    search = st.session_state.watchlist_clicked_name

    st.session_state.watchlist_clicked_stock = None
    st.session_state.watchlist_clicked_name = None


# ==========================================
# SMART SCREENER
# ==========================================
if screener_clicked:
    st.session_state.screener_running = True

    results = screener.run_screener(stocks_dict)
    screener.display_screener_results(results)

    st.session_state.screener_running = False


# ==========================================
# STOP IF NO STOCK
# ==========================================
if not stock:
    st.stop()


# ==========================================
# TIMEFRAME SELECTOR
# ==========================================
timeframe = "Daily"
interval = "1d"
period = "6mo"


# ==========================================
# FETCH DATA
# ==========================================
with st.spinner("📡 Fetching latest market data..."):
    data = fetch_stock_data(stock, period, interval)

if data.empty:
    st.markdown(f"""
    <div style="
        display: inline-block;
        max-width: 420px;
        padding: 14px 18px;
        border-radius: 10px;
        background: rgba(220, 38, 38, 0.12); /* translucent red overlay */
        border: 1px solid rgba(220, 38, 38, 0.35);
        margin: 20px auto;
    ">
        <div style="
            font-size: 14px;
            font-weight: 600;
            color: var(--error-color); /* auto adapts */
            margin-bottom: 6px;
        ">
            ⚠️ Stock Not Found
        </div>
        <div style="
            font-size: 13px;
            color: var(--text-color); /* adapts to theme */
            line-height: 1.6;
            font-weight: 500;
        ">
            We couldn't find market data for 
            <b style="color: var(--text-color);">{stock}</b>.<br>
            Please try a different stock name or symbol.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()



# ==========================================
# INDICATORS
# ==========================================
# RSI
window = 14

delta = data["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.ewm(alpha=1 / window, adjust=False).mean()
avg_loss = loss.ewm(alpha=1 / window, adjust=False).mean()

rs = avg_gain / avg_loss
data["RSI"] = 100 - (100 / (1 + rs))


# MACD

data["EMA_12"] = data["Close"].ewm(span=12).mean()
data["EMA_26"] = data["Close"].ewm(span=26).mean()
data["MACD"] = data["EMA_12"] - data["EMA_26"]
data["MACD_Signal"] = data["MACD"].ewm(span=9).mean()


# Moving Averages

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()


# ADX
high = data["High"]
low = data["Low"]
close = data["Close"]

plus_dm = high.diff()
minus_dm = low.diff()

plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)

tr1 = high - low
tr2 = (high - close.shift()).abs()
tr3 = (low - close.shift()).abs()

tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
atr = tr.rolling(14).mean()

plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
minus_di = 100 * (minus_dm.rolling(14).mean() / atr)

dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
data["ADX"] = dx.rolling(14).mean()


# Bollinger Bands

data["BB_Middle"] = data["Close"].rolling(20).mean()
std = data["Close"].rolling(20).std()

data["BB_Upper"] = data["BB_Middle"] + (2 * std)
data["BB_Lower"] = data["BB_Middle"] - (2 * std)


# ==========================================
# SIGNAL GENERATION
# ==========================================
signal_value = getsignal(data)

data["Signal"] = 0
data.iloc[-1, data.columns.get_loc("Signal")] = signal_value

if signal_value == 1:
    buy = data.tail(1)
    sell = data.iloc[0:0]
elif signal_value == -1:
    sell = data.tail(1)
    buy = data.iloc[0:0]
else:
    buy = data.iloc[0:0]
    sell = data.iloc[0:0]


# ==========================================
# METRICS
# ==========================================
ui.render_metrics(data, buy, sell, stock)


# ==========================================
# CHARTS
# ==========================================
st.subheader("📊 Charts")
plot_price_chart(data, buy, sell, timeframe)


# ==========================================
# NEWS
# ==========================================
news_target = search if search else stock
news = get_stock_news(news_target)
ui.render_news(news)


# ==========================================
# CONTACT
# ==========================================
ui.render_contact()
