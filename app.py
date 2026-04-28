# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import time
from urllib.parse import quote_plus

from signals import getsignal
from stocks import stocks_dict
from charts import plot_price_chart
import ui
import screener

# ==========================================
# SESSION STATE
# ==========================================
if "screener_running" not in st.session_state:
    st.session_state.screener_running = False

if "first_load" not in st.session_state:
    st.session_state.first_load = True

# ==========================================
# NEWS FETCHING FUNCTION
# ==========================================
def get_stock_news(stock_name):
    try:
        query = quote_plus(stock_name)
        url = f"https://news.google.com/rss/search?q={query}%20stock&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        
        if feed.bozo:
            return [{"title": "⚠️ Error fetching news.", "link": "", "source": "", "time": ""}]
        if not feed.entries:
            return [{"title": "❌ No news found.", "link": "", "source": "", "time": ""}]
        
        news_list = []
        for entry in feed.entries[:5]:
            news_list.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", "#"),
                "source": entry.get("source", {}).get("title", "Unknown"),
                "time": entry.get("published", "No time")
            })
        return news_list
    except Exception as e:
        return [{"title": f"⚠️ Error: {str(e)}", "link": "", "source": "", "time": ""}]

# ==========================================
# HEADER
# ==========================================
ui.render_header()

# ==========================================
# 📋 WATCHLIST (Sidebar)
# ==========================================
# ✅ Ensure watchlist is initialized even after st.rerun()
if "watchlist" not in st.session_state:
    from watchlist import load_watchlist
    st.session_state.watchlist = load_watchlist()

with st.sidebar:
    st.markdown("## 📋 Watchlist")
    from watchlist import watchlist_fragment
    watchlist_fragment(stocks_dict)
    st.markdown("---")

# ==========================================
# SEARCH + SCREENER
# ==========================================
search, stock, screener_clicked = ui.render_search_section(stocks_dict)

# ✅ If a stock was clicked from watchlist, use it
if "watchlist_clicked_stock" in st.session_state and st.session_state.watchlist_clicked_stock:
    stock = st.session_state.watchlist_clicked_stock
    search = st.session_state.watchlist_clicked_name
    # Clear after use
    st.session_state.watchlist_clicked_stock = None
    st.session_state.watchlist_clicked_name = None

if screener_clicked:
    st.session_state.screener_running = True
    results = screener.run_screener(stocks_dict)
    screener.display_screener_results(results)
    st.session_state.screener_running = False

# ==========================================
# TIMEFRAME LOGIC
# ==========================================
timeframe = "Daily"

if timeframe == "Daily":
    interval = "1d"
    period = "6mo"
elif timeframe == "Weekly":
    interval = "1wk"
    period = "1y"
elif timeframe == "Monthly":
    interval = "1mo"
    period = "5y"
elif timeframe == "5 Min":
    interval = "5m"
    period = "5d"
elif timeframe == "15 Min":
    interval = "15m"
    period = "1mo"
elif timeframe == "1 Hour":
    interval = "60m"
    period = "3mo"

# ==========================================
# FETCH DATA (Silent after first load)
# ==========================================
if not stock:
    st.stop()

if st.session_state.first_load:
    with st.spinner("📡 Fetching latest market data..."):
        ticker = yf.Ticker(stock)
        data = ticker.history(period=period, interval=interval)
    st.session_state.first_load = False
else:
    # Silent refresh — no spinner, no flash
    ticker = yf.Ticker(stock)
    data = ticker.history(period=period, interval=interval)

if data.empty:
    st.error(f"❌ No data found for {stock}.")
    st.stop()

# ==========================================
# INDICATOR CALCULATIONS
# ==========================================
# RSI
delta = data['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
window = 14
avg_gain = gain.ewm(alpha=1/window, adjust=False).mean()
avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# MACD
data['EMA_12'] = data['Close'].ewm(span=12).mean()
data['EMA_26'] = data['Close'].ewm(span=26).mean()
data['MACD'] = data['EMA_12'] - data['EMA_26']
data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()

# Moving Averages
data['MA20'] = data['Close'].rolling(20).mean()
data['MA50'] = data['Close'].rolling(50).mean()
data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

# ADX
high = data['High']
low = data['Low']
close = data['Close']
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
data['ADX'] = dx.rolling(14).mean()

# Bollinger Bands
data['BB_Middle'] = data['Close'].rolling(20).mean()
std = data['Close'].rolling(20).std()
data['BB_Upper'] = data['BB_Middle'] + (2 * std)
data['BB_Lower'] = data['BB_Middle'] - (2 * std)

# ==========================================
# SIGNAL GENERATION
# ==========================================
signal_value = getsignal(data)
data['Signal'] = 0
data.iloc[-1, data.columns.get_loc('Signal')] = signal_value

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
news = get_stock_news(search)
ui.render_news(news)

# ==========================================
# CONTACT
# ==========================================
ui.render_contact()