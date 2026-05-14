# watchlist.py - Groww Style Watchlist (Single Line, Compact)

import streamlit as st
import yfinance as yf
import json
import os
import time

WATCHLIST_FILE = "watchlist_data.json"

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_watchlist():
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(st.session_state.watchlist, f, indent=2)

def add_to_watchlist(stock_symbol, stock_name=""):
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
    st.session_state.watchlist = [
        s for s in st.session_state.watchlist 
        if s['symbol'] != stock_symbol
    ]
    save_watchlist()

@st.cache_data(ttl=5, show_spinner=False)
def get_cached_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        live_price = info.get("lastPrice", None)
        prev_close = info.get("previousClose", None)
        
        if live_price and prev_close:
            change = ((live_price - prev_close) / prev_close) * 100
            return {'price': live_price, 'change': change}
    except:
        pass
    return None

def watchlist_fragment(stocks_dict):
    """Compact single-line watchlist"""
    
    if not st.session_state.watchlist:
        st.info("✨ Your watchlist is empty. Search and click ⭐ to add!", icon="📋")
        return
    
    # Ultra compact CSS
    st.markdown("""
    <style>
    /* Make buttons single line and compact */
    .stButton button {
        background: transparent !important;
        border: none !important;
        padding: 6px 8px !important;
        margin: 0px !important;
        min-height: 32px !important;
        height: auto !important;
        text-align: left !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        box-shadow: none !important;
    }
    
    .stButton button:hover {
        background: rgba(0, 255, 255, 0.08) !important;
        border: none !important;
    }
    
    /* Compact columns */
    div[data-testid="column"] {
        padding: 0px 2px !important;
    }
    
    /* Compact row */
    .compact-row {
        background: rgba(10, 20, 40, 0.4);
        border-radius: 8px;
        padding: 4px 8px;
        margin-bottom: 2px;
        border: 1px solid rgba(0, 255, 255, 0.06);
    }
    
    hr {
        margin: 1px 0 !important;
        opacity: 0.03 !important;
    }
    
    /* Remove button smaller */
    .remove-btn button {
        font-size: 14px !important;
        padding: 6px 0px !important;
        text-align: center !important;
        color: #64748b !important;
    }
    
    .remove-btn button:hover {
        color: #ff1744 !important;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .stButton button {
            font-size: 10px !important;
            padding: 5px 4px !important;
            min-height: 28px !important;
        }
        .remove-btn button {
            font-size: 12px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    for item in st.session_state.watchlist:
        symbol = item['symbol']
        name = item.get('name', symbol)
        
        # Clean up display name - single name only
        clean_name = name.replace('.NS', '').replace('.BO', '')
        
        # Remove "BANK" word for better display
        if "BANK" in clean_name:
            clean_name = clean_name.replace(" BANK", "")
        
        # Truncate long names
        if len(clean_name) > 10:
            clean_name = clean_name[:9] + "."
        
        price_data = get_cached_price(symbol)
        
        if price_data and price_data['price']:
            live_price = price_data['price']
            change_pct = price_data['change']
            color = "#00ff88" if change_pct >= 0 else "#ff1744"
            arrow = "▲" if change_pct >= 0 else "▼"
            price_text = f"₹{live_price:,.0f}"
            change_text = f"{arrow} {abs(change_pct):.1f}%"
        else:
            color = "#64748b"
            price_text = "..."
            change_text = "..."
        
        # Single line layout - 3 columns
        col1, col2, col3 = st.columns([1.5, 1.2, 0.3], gap="small")
        
        with col1:
            # Single name button (no duplicate)
            if st.button(
                f"📈 {clean_name}",
                key=f"watch_{symbol}",
                use_container_width=True
            ):
                st.session_state.selected_stock = symbol
                st.session_state.selected_name = clean_name
                st.rerun()
        
        with col2:
            st.markdown(
                f"""
                <div style="text-align: right;">
                    <span style="font-size: 12px; font-weight: 700; color: {color};">{price_text}</span>
                    <span style="font-size: 9px; font-weight: 600; color: {color}; margin-left: 4px;">{change_text}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            if st.button("✕", key=f"remove_{symbol}", use_container_width=True):
                remove_from_watchlist(symbol)
                st.rerun()
