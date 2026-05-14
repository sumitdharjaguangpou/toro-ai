# indices.py - Clickable Indices for TORO AI (Light & Dark Mode Compatible)

import streamlit as st
import yfinance as yf

INDICES = {
    "NIFTY 50": {"symbol": "^NSEI", "display": "NIFTY 50"},
    "SENSEX": {"symbol": "^BSESN", "display": "SENSEX"}, 
    "BANK NIFTY": {"symbol": "^NSEBANK", "display": "BANK NIFTY"}
}

@st.cache_data(ttl=5, show_spinner=False)
def get_index_data():
    """Fetch live index data"""
    try:
        indices_data = {}
        for key, info in INDICES.items():
            symbol = info["symbol"]
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            
            if not data.empty and len(data) >= 2:
                current_price = data['Close'].iloc[-1]
                prev_close = data['Close'].iloc[-2]
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                indices_data[key] = {
                    'price': current_price,
                    'change': change,
                    'change_pct': change_pct,
                    'symbol': symbol,
                    'display': info["display"]
                }
            else:
                indices_data[key] = {
                    'price': 0,
                    'change': 0,
                    'change_pct': 0,
                    'symbol': symbol,
                    'display': info["display"]
                }
        return indices_data
    except Exception as e:
        return {key: {
            'price': 0,
            'change': 0,
            'change_pct': 0,
            'symbol': info["symbol"],
            'display': info["display"]
        } for key, info in INDICES.items()}

def render_indices():
    """Render clickable indices - Light & Dark Mode Compatible"""
    
    indices_data = get_index_data()
    
    # Theme-aware CSS for index buttons (works in both light and dark mode)
    st.markdown("""
    <style>
    /* Light mode styles */
    @media (prefers-color-scheme: light) {
        .stButton button {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef) !important;
            border: 1px solid #dee2e6 !important;
            color: #212529 !important;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #e9ecef, #dee2e6) !important;
            border-color: #adb5bd !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }
        
        .positive-change {
            color: #008000 !important;
        }
        
        .negative-change {
            color: #dc3545 !important;
        }
    }
    
    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        .stButton button {
            background: linear-gradient(135deg, #2d2d2d, #1a1a1a) !important;
            border: 1px solid #404040 !important;
            color: #e0e0e0 !important;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #404040, #2d2d2d) !important;
            border-color: #666666 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        }
        
        .positive-change {
            color: #00ff88 !important;
        }
        
        .negative-change {
            color: #ff6b6b !important;
        }
    }
    
    /* Base button styling */
    .stButton button {
        border-radius: 20px !important;
        padding: 6px 12px !important;
        height: auto !important;
        transition: all 0.2s ease !important;
        font-size: 12px !important;
        white-space: nowrap !important;
        font-weight: 500 !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .stButton button {
            padding: 4px 8px !important;
            font-size: 10px !important;
            white-space: normal !important;
        }
    }
    
    /* Ensure text contrast in both themes */
    .stButton button p {
        margin: 0 !important;
        line-height: 1.4 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create columns for each index
    cols = st.columns(len(indices_data))
    
    for idx, (key, data) in enumerate(indices_data.items()):
        with cols[idx]:
            price = data['price']
            change_pct = abs(data['change_pct'])
            symbol = data['symbol']
            display_name = data['display']
            is_positive = data['change'] >= 0
            
            # Format price
            if price >= 100000:
                price_text = f"{price/1000:.1f}K"
            elif price >= 10000:
                price_text = f"{price:,.0f}"
            else:
                price_text = f"{price:.2f}"
            
            arrow = "▲" if is_positive else "▼"
            
            # Use markdown formatting within button for colored text
            if is_positive:
                button_text = f"{display_name} {price_text} :green[{arrow} {change_pct:.1f}%]"
            else:
                button_text = f"{display_name} {price_text} :red[{arrow} {change_pct:.1f}%]"
            
            if st.button(button_text, key=f"index_{key}", use_container_width=True):
                st.session_state.selected_stock = symbol
                st.session_state.selected_name = display_name
                st.rerun()
