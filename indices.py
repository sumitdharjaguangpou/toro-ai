# indices.py - Clickable Indices (Light & Dark Mode Friendly)

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
# THEME-AWARE CSS FOR INDICES (Light & Dark Mode)
# ==========================================
def get_indices_css():
    """Return theme-aware CSS for indices that works in both light and dark mode"""
    return """
    <style>
    /* Base styles that work for both themes */
    .index-item {
        display: flex;
        align-items: baseline;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid;
        cursor: pointer;
        transition: all 0.2s ease;
        background: var(--bg-card-light);
    }
    
    /* Light mode styles */
    .stApp .index-item {
        background: #f8f9fa;
        border-color: #e0e0e0;
    }
    
    .stApp .index-name {
        color: #666666;
    }
    
    .stApp .index-price {
        color: #0088ff;
    }
    
    .stApp .index-positive {
        color: #00a86b;
    }
    
    .stApp .index-negative {
        color: #ff4757;
    }
    
    /* Dark mode styles - automatically applied by Streamlit */
    @media (prefers-color-scheme: dark) {
        .stApp .index-item {
            background: #2c2c2c !important;
            border-color: #404040 !important;
        }
        
        .stApp .index-name {
            color: #999999 !important;
        }
        
        .stApp .index-price {
            color: #4db8ff !important;
        }
        
        .stApp .index-positive {
            color: #00c853 !important;
        }
        
        .stApp .index-negative {
            color: #ff6b81 !important;
        }
    }
    
    .index-item:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stApp .index-item:hover {
        background: #e9ecef;
        border-color: #0088ff;
    }
    
    @media (prefers-color-scheme: dark) {
        .stApp .index-item:hover {
            background: #3a3a3a !important;
            border-color: #4db8ff !important;
        }
    }
    
    .index-name {
        font-size: 11px;
        font-weight: 600;
    }
    
    .index-price {
        font-size: 13px;
        font-weight: 700;
    }
    
    .index-change {
        font-size: 10px;
        font-weight: 600;
    }
    
    /* Button styling for Streamlit buttons */
    div.stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease;
        text-align: left;
        padding: 0;
    }
    
    div.stButton > button:hover {
        transform: translateY(-1px);
        background: transparent !important;
        border-color: transparent !important;
    }
    
    div.stButton > button p {
        margin: 0;
    }
    </style>
    """

def render_indices():
    """Display clickable indices using Streamlit buttons (Light & Dark Mode Friendly)"""
    
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
            
            # Create a clean button label
            button_label = f"{display_name}  {price_text}  {arrow} {change_pct:.2f}%"
            
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
    """Display clickable indices using HTML (Theme-Aware - Light & Dark Mode)"""
    
    # Inject theme-aware CSS
    st.markdown(get_indices_css(), unsafe_allow_html=True)
    
    indices_data = get_index_data()
    
    # Build HTML container
    html_parts = ['<div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; flex-wrap: wrap;">']
    
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
        
        html_parts.append(f'''
        <div id="{unique_id}" class="index-item" data-symbol="{symbol}" data-name="{display_name}">
            <span class="index-name">{display_name}</span>
            <span class="index-price">{price_text}</span>
            <span class="index-change {change_class}">{arrow} {change_pct:.2f}%</span>
        </div>
        ''')
    
    html_parts.append('</div>')
    
    # Add JavaScript for click handling
    html_parts.append('''
    <script>
    document.querySelectorAll('.index-item').forEach(item => {
        item.addEventListener('click', function() {
            const symbol = this.getAttribute('data-symbol');
            const name = this.getAttribute('data-name');
            
            // Use Streamlit's Component API if available, otherwise use query parameters
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: {symbol: symbol, name: name}
                }, "*");
            } else {
                const url = new URL(window.location);
                url.searchParams.set('stock', symbol);
                url.searchParams.set('name', name);
                window.location.href = url;
            }
        });
    });
    </script>
    ''')
    
    # Render the HTML
    st.markdown(''.join(html_parts), unsafe_allow_html=True)

def render_indices_simple():
    """Simple inline display (no click functionality) - Light & Dark Mode Friendly"""
    
    indices_data = get_index_data()
    
    # Build simple HTML with theme-aware colors
    html_parts = ['<div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; flex-wrap: wrap;">']
    
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
        color_class = "index-positive" if is_positive else "index-negative"
        
        html_parts.append(f'''
        <div style="display: flex; align-items: baseline; gap: 6px;">
            <span style="font-size: 11px; font-weight: 600; color: #666666;" class="index-name">{display_name}</span>
            <span style="font-size: 12px; font-weight: 700; color: #0088ff;" class="index-price">{price_text}</span>
            <span style="font-size: 10px; font-weight: 600;" class="{color_class}">{arrow} {change_pct:.2f}%</span>
        </div>
        ''')
    
    html_parts.append('</div>')
    
    # Render the HTML
    st.markdown(''.join(html_parts), unsafe_allow_html=True)

# ==========================================
# RECOMMENDED: Simple working version
# ==========================================
def show_indices():
    """Simple working version - guaranteed to display properly"""
    
    indices_data = get_index_data()
    
    # Create columns
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
            color = "green" if is_positive else "red"
            
            # Use markdown with colored text
            button_text = f"""
**{display_name}**  
{price_text}  
<font color="{color}">{arrow} {change_pct:.2f}%</font>
"""
            
            if st.button(button_text, key=f"idx_{key}", use_container_width=True):
                st.session_state.selected_stock = symbol
                st.session_state.selected_name = display_name
                st.rerun()
