# indices.py - Clickable Indices with Explicit Theme Detection

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
    """Render clickable indices - Works in both light and dark mode"""
    
    indices_data = get_index_data()
    
    # Detect current Streamlit theme
    try:
        # Get the current theme from Streamlit config
        theme = st.get_option("theme.base")
        is_dark = theme == "dark"
    except:
        # Fallback to system preference detection
        is_dark = False
    
    # Theme-specific colors
    if is_dark:
        bg_gradient_start = "#2d2d2d"
        bg_gradient_end = "#1a1a1a"
        border_color = "#404040"
        text_color = "#e0e0e0"
        hover_bg_start = "#404040"
        hover_bg_end = "#2d2d2d"
        hover_border = "#666666"
        positive_color = "#00ff88"
        negative_color = "#ff6b6b"
    else:
        bg_gradient_start = "#f8f9fa"
        bg_gradient_end = "#e9ecef"
        border_color = "#dee2e6"
        text_color = "#212529"
        hover_bg_start = "#e9ecef"
        hover_bg_end = "#dee2e6"
        hover_border = "#adb5bd"
        positive_color = "#008000"
        negative_color = "#dc3545"
    
    # Inject theme-aware CSS
    st.markdown(f"""
    <style>
    /* Button styling */
    .stButton button {{
        background: linear-gradient(135deg, {bg_gradient_start}, {bg_gradient_end}) !important;
        border: 1px solid {border_color} !important;
        border-radius: 20px !important;
        padding: 6px 12px !important;
        height: auto !important;
        transition: all 0.2s ease !important;
        font-size: 12px !important;
        white-space: nowrap !important;
        color: {text_color} !important;
        font-weight: 500 !important;
    }}
    
    .stButton button:hover {{
        transform: translateY(-1px) !important;
        background: linear-gradient(135deg, {hover_bg_start}, {hover_bg_end}) !important;
        border-color: {hover_border} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }}
    
    /* Mobile responsive */
    @media (max-width: 768px) {{
        .stButton button {{
            padding: 4px 8px !important;
            font-size: 10px !important;
            white-space: normal !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Create columns for each index
    cols = st.columns(len(indices_data))
    
    for idx, (key, data) in enumerate(indices_data.items()):
        with cols[idx]:
            price = data['price']
            change_pct = data['change_pct']
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
            
            # Create button text with colored change
            if is_positive:
                button_text = (
                    f"{display_name} {price_text} "
                    f":green[{arrow} {abs(change_pct):.2f}%]"
                )
            else:
                button_text = (
                    f"{display_name} {price_text} "
                    f":red[{arrow} {abs(change_pct):.2f}%]"
    )
            
            if st.button(button_text, key=f"index_{key}", use_container_width=True):
                st.session_state.selected_stock = symbol
                st.session_state.selected_name = display_name
                st.rerun()
