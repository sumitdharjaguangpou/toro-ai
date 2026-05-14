# indices.py - Clickable Indices (Theme-Friendly)

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
        # Return fallback data
        return {key: {
            'price': 0,
            'change': 0,
            'change_pct': 0,
            'symbol': info["symbol"],
            'display': info["display"]
        } for key, info in INDICES.items()}

# ==========================================
# THEME-AWARE CSS FOR INDICES
# ==========================================
def get_indices_css():
    """Return theme-aware CSS for indices"""
    return """
    <style>
    .index-item {
        display: flex;
        align-items: baseline;
        gap: 8px;
        background: var(--bg-card);
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid var(--border-glow);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .index-item:hover {
        background: var(--bg-secondary);
        border-color: var(--accent-cyan);
        transform: translateY(-1px);
    }
    
    .index-name {
        font-size: 11px;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .index-price {
        font-size: 13px;
        font-weight: 700;
    }
    
    .index-change {
        font-size: 10px;
        font-weight: 600;
    }
    
    .index-positive {
        color: var(--accent-green);
    }
    
    .index-negative {
        color: var(--accent-red);
    }
    </style>
    """

def render_indices():
    """Display clickable indices using Streamlit buttons (Theme-Friendly)"""
    
    # Inject theme-aware CSS
    st.markdown(get_indices_css(), unsafe_allow_html=True)
    
    indices_data = get_index_data()
    
    # Create columns for each index
    cols = st.columns(len(indices_data))
    
    for idx, (key, data) in enumerate(indices_data.items()):
        with cols[idx]:
            price = data['price']
            change_pct = abs(data['change_pct'])
            symbol = data['symbol']
            display_name = data['display']
            is_positive = data['change'] >= 0
            
            # Format price display
            if price >= 100000:
                price_text = f"{price/1000:.1f}K"
            elif price >= 10000:
                price_text = f"{price:,.0f}"
            else:
                price_text = f"{price:.2f}"
            
            # Set color class based on change
            change_class = "index-positive" if is_positive else "index-negative"
            arrow = "▲" if is_positive else "▼"
            
            # Create a styled button with theme-aware colors
            button_label = f"""
**{display_name}**
<span style="font-size:13px; font-weight:700;">{price_text}</span>
<span class="{change_class}">{arrow} {change_pct:.2f}%</span>
"""
            
            # Use a button with custom styling
            if st.button(
                button_label,
                key=f"index_{key}",
                use_container_width=True,
                help=f"Click to analyze {display_name}"
            ):
                # Set the selected stock in session state
                st.session_state.selected_stock = symbol
                st.session_state.selected_name = display_name
                st.rerun()


def render_indices_html():
    """Display clickable indices using HTML (Theme-Aware - No rerun needed)"""
    
    # Inject theme-aware CSS
    st.markdown(get_indices_css(), unsafe_allow_html=True)
    
    indices_data = get_index_data()
    
    # Build HTML with theme-aware CSS variables and JavaScript
    html = '''
    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; flex-wrap: wrap;">
    '''
    
    for key, data in indices_data.items():
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
        
        # Set color class
        change_class = "index-positive" if is_positive else "index-negative"
        arrow = "▲" if is_positive else "▼"
        
        # Generate a unique ID
        unique_id = f"idx_{key.replace(' ', '_')}"
        
        html += f'''
        <div id="{unique_id}" class="index-item">
            <span class="index-name">{display_name}</span>
            <span class="index-price" style="color: var(--accent-cyan);">{price_text}</span>
            <span class="index-change {change_class}">{arrow} {change_pct:.2f}%</span>
        </div>
        
        <script>
        (function() {{
            const element = document.getElementById('{unique_id}');
            if (element) {{
                // Remove any existing listeners to prevent duplicates
                const newElement = element.cloneNode(true);
                element.parentNode.replaceChild(newElement, element);
                
                newElement.addEventListener('click', function(e) {{
                    e.preventDefault();
                    // Use Streamlit's query parameters
                    const url = new URL(window.location);
                    url.searchParams.set('stock', '{symbol}');
                    url.searchParams.set('name', '{display_name}');
                    window.location.href = url;
                }});
            }}
        }})();
        </script>
        '''
    
    html += '</div>'
    
    return html


def render_indices_simple():
    """Simple inline display (no click functionality) - Theme-Friendly"""
    
    indices_data = get_index_data()
    
    # Build simple HTML with theme-aware colors
    html = '<div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; flex-wrap: wrap;">'
    
    for key, data in indices_data.items():
        price = data['price']
        change_pct = abs(data['change_pct'])
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
        color = "var(--accent-green)" if is_positive else "var(--accent-red)"
        
        html += f'''
        <div style="display: flex; align-items: baseline; gap: 6px;">
            <span style="font-size: 11px; font-weight: 600; color: var(--text-secondary);">{display_name}</span>
            <span style="font-size: 12px; font-weight: 700; color: var(--accent-cyan);">{price_text}</span>
            <span style="font-size: 10px; font-weight: 600; color: {color};">{arrow} {change_pct:.2f}%</span>
        </div>
        '''
    
    html += '</div>'
    
    return html
