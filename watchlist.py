# watchlist.py - Optimized Compact Version

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
# FETCH LIVE DATA FOR WATCHLIST (OPTIMIZED)
# ==========================================
@st.fragment(run_every=5)
def watchlist_fragment(stocks_dict):
    """Updates watchlist prices every 5 seconds - Compact version"""
    
    # Add custom CSS for compact watchlist
    st.markdown("""
    <style>
    /* Compact watchlist styling */
    .watchlist-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0;
        margin: 2px 0;
        border-bottom: 1px solid rgba(0,255,255,0.08);
    }
    .watchlist-name {
        font-size: 12px;
        font-weight: 600;
        color: #ffffff;
        cursor: pointer;
    }
    .watchlist-symbol {
        font-size: 9px;
        color: #64748b;
    }
    .watchlist-price {
        font-size: 12px;
        font-weight: 600;
        text-align: right;
    }
    .watchlist-change {
        font-size: 10px;
        text-align: right;
    }
    .watchlist-remove {
        font-size: 14px;
        cursor: pointer;
        color: #64748b;
        padding: 0 4px;
    }
    .watchlist-remove:hover {
        color: #ff1744;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.watchlist:
        st.markdown(
            """
            <div style="
                text-align: center;
                padding: 15px;
                color: #64748b;
                font-size: 11px;
            ">
                📋 Empty<br>
                <span style="font-size: 9px;">Click ⭐ to add stocks</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    for item in st.session_state.watchlist:
        symbol = item['symbol']
        name = item.get('name', symbol)
        display_name = name.replace('.NS', '').replace('.BO', '')[:12]  # Truncate long names
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            live_price = info.get("lastPrice", None)
            prev_close = info.get("previousClose", None)
            
            if live_price and prev_close:
                change = live_price - prev_close
                pct = (change / prev_close) * 100
                
                if change >= 0:
                    color = "#00ff88"
                    arrow = "▲"
                else:
                    color = "#ff1744"
                    arrow = "▼"
                
                # Compact layout without columns
                col1, col2, col3 = st.columns([3.5, 1.5, 0.5])
                
                with col1:
                    # Smaller button for stock name
                    if st.button(f"📊 {display_name}", key=f"wl_{symbol}", use_container_width=True):
                        st.session_state.watchlist_clicked_stock = symbol
                        st.session_state.watchlist_clicked_name = name
                    st.caption(symbol.replace('.NS', '').replace('.BO', ''))
                
                with col2:
                    st.markdown(
                        f"""
                        <div style="text-align: right;">
                            <span style="font-size: 13px; font-weight: 700;">₹{live_price:,.2f}</span>
                            <br>
                            <span style="font-size: 10px; color: {color};">{arrow} {abs(pct):.2f}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col3:
                    if st.button("✕", key=f"del_{symbol}", help="Remove"):
                        remove_from_watchlist(symbol)
                        st.rerun()
                
                # Minimal separator
                st.markdown("<hr style='margin:2px 0; opacity:0.2;'>", unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 6px 0;
                ">
                    <div>
                        <span style="font-size: 11px; font-weight: 500;">{display_name}</span>
                        <br>
                        <span style="font-size: 8px; color: #64748b;">{symbol}</span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #ff1744;">⚠️ No data</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
