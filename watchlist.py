# watchlist.py
import streamlit as st
import yfinance as yf
import json
import os
import time

# ==========================================
# FILE PATH FOR PERSISTENT STORAGE
# ==========================================
WATCHLIST_FILE = "watchlist_data.json"

# ==========================================
# LOAD WATCHLIST FROM FILE
# ==========================================
def load_watchlist():
    """Load watchlist from JSON file"""
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# ==========================================
# INITIALIZE WATCHLIST
# ==========================================
if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()

# save_watchlist
def save_watchlist():
    """Save watchlist to JSON file"""
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(st.session_state.watchlist, f, indent=2)



# ==========================================
# WATCHLIST FUNCTIONS
# ==========================================
def add_to_watchlist(stock_symbol, stock_name=""):
    """Add stock to watchlist and save to file"""
    if stock_symbol not in [s['symbol'] for s in st.session_state.watchlist]:
        st.session_state.watchlist.append({
            'symbol': stock_symbol,
            'name': stock_name if stock_name else stock_symbol,
            'added_at': time.time()
        })
        save_watchlist()
        return True
    return False

def remove_from_watchlist(stock_symbol):
    """Remove stock from watchlist and save to file"""
    st.session_state.watchlist = [
        s for s in st.session_state.watchlist 
        if s['symbol'] != stock_symbol
    ]
    save_watchlist()

# ==========================================
# FETCH LIVE DATA FOR WATCHLIST
# ==========================================
@st.fragment(run_every=5)
def watchlist_fragment(stocks_dict):
    """Updates watchlist prices every 5 seconds"""
    if not st.session_state.watchlist:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 20px;
                color: #94a3b8;
                font-size: 13px;
            ">
                📋 Your watchlist is empty<br>
                <span style="font-size: 11px;">Search a stock and click ⭐ to add</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    for item in st.session_state.watchlist:
        symbol = item['symbol']
        name = item.get('name', symbol)
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            live_price = info.get("lastPrice", None)
            prev_close = info.get("previousClose", None)
            
            if live_price and prev_close:
                change = live_price - prev_close
                pct = (change / prev_close) * 100
                
                if change >= 0:
                    color = "#16a34a"
                    arrow = "▲"
                else:
                    color = "#dc2626"
                    arrow = "▼"
                
                # Row layout
                col1, col2, col3 = st.columns([4, 2, 0.8])
                
                with col1:
                    if st.button(f"📈 {name}", key=f"wl_{symbol}", use_container_width=True):
                       st.session_state.watchlist_clicked_stock = symbol
                       st.session_state.watchlist_clicked_name = name
                    
                    st.markdown(
                        f"""<div style="font-size:10px; color:#94a3b8;">{symbol}</div>""",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.markdown(
                        f"""
                        <div style="text-align: right;">
                            <div style="font-size: 14px; font-weight: 700; color: #0f172a;">
                                ₹{live_price:,.2f}
                            </div>
                            <div style="font-size: 11px; color: {color};">
                                {arrow} {abs(pct):.2f}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col3:
                    if st.button("✕", key=f"del_{symbol}", help="Remove from watchlist"):
                        remove_from_watchlist(symbol)
                        st.rerun()
                
                st.markdown("<hr style='margin:4px 0; opacity:0.3;'>", unsafe_allow_html=True)
                
        except:
            st.markdown(
                f"""
                <div style="
                    padding: 8px;
                    border-radius: 6px;
                    background: rgba(100,116,139,0.05);
                    margin: 4px 0;
                ">
                    <span style="font-size:12px; color:#94a3b8;">{name}</span>
                    <span style="font-size:10px; color:#dc2626;"> — Data unavailable</span>
                </div>
                """,
                unsafe_allow_html=True
            )