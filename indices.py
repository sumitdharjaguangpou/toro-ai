# indices.py - Clickable Indices (Fully Customized)

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
                    'color': "#00ff88" if change >= 0 else "#ff1744",
                    'arrow': "▲" if change >= 0 else "▼",
                    'symbol': symbol,
                    'display': info["display"]
                }
            else:
                indices_data[key] = {
                    'price': 0,
                    'change': 0,
                    'change_pct': 0,
                    'color': "#8892b0",
                    'arrow': "●",
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
            'color': "#8892b0",
            'arrow': "●",
            'symbol': info["symbol"],
            'display': info["display"]
        } for key, info in INDICES.items()}


def render_indices():
    """Display clickable indices using Streamlit buttons"""
    
    indices_data = get_index_data()
    
    # Create columns for each index
    cols = st.columns(len(indices_data))
    
    for idx, (key, data) in enumerate(indices_data.items()):
        with cols[idx]:
            price = data['price']
            color = data['color']
            arrow = data['arrow']
            change_pct = abs(data['change_pct'])
            symbol = data['symbol']
            display_name = data['display']
            
            # Format price display
            if price >= 100000:
                price_text = f"{price/1000:.1f}K"
            elif price >= 10000:
                price_text = f"{price:,.0f}"
            else:
                price_text = f"{price:.2f}"
            
            # Create a styled button
            button_label = f"""
**{display_name}**
{price_text}
{arrow} {change_pct:.2f}%
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
    """Alternative: Display clickable indices using HTML (no button feel)"""
    
    indices_data = get_index_data()
    
    # Build HTML with inline styles and JavaScript
    html = '''
    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 15px; flex-wrap: wrap;">
    '''
    
    for key, data in indices_data.items():
        price = data['price']
        color = data['color']
        arrow = data['arrow']
        change_pct = abs(data['change_pct'])
        symbol = data['symbol']
        display_name = data['display']
        
        # Format price
        if price >= 100000:
            price_text = f"{price/1000:.1f}K"
        elif price >= 10000:
            price_text = f"{price:,.0f}"
        else:
            price_text = f"{price:.2f}"
        
        # Generate a unique ID
        unique_id = f"idx_{key.replace(' ', '_')}"
        
        html += f'''
        <div id="{unique_id}" class="index-item" 
             style="display: flex; align-items: baseline; gap: 8px; 
                    background: rgba(0, 255, 255, 0.05); 
                    padding: 6px 14px; 
                    border-radius: 20px; 
                    border: 1px solid rgba(0, 255, 255, 0.15);
                    cursor: pointer;
                    transition: all 0.2s ease;">
            <span style="font-size: 11px; font-weight: 600; color: #8892b0;">{display_name}</span>
            <span style="font-size: 13px; font-weight: 700; color: {color};">{price_text}</span>
            <span style="font-size: 10px; font-weight: 600; color: {color};">{arrow} {change_pct:.2f}%</span>
        </div>
        
        <script>
        document.getElementById('{unique_id}').addEventListener('click', function() {{
            // Use Streamlit's query parameters to set the stock
            const url = new URL(window.location);
            url.searchParams.set('stock', '{symbol}');
            url.searchParams.set('name', '{display_name}');
            window.location.href = url;
        }});
        
        // Add hover effect
        document.getElementById('{unique_id}').addEventListener('mouseenter', function() {{
            this.style.background = 'rgba(0, 255, 255, 0.12)';
            this.style.borderColor = 'rgba(0, 255, 255, 0.4)';
            this.style.transform = 'translateY(-1px)';
        }});
        
        document.getElementById('{unique_id}').addEventListener('mouseleave', function() {{
            this.style.background = 'rgba(0, 255, 255, 0.05)';
            this.style.borderColor = 'rgba(0, 255, 255, 0.15)';
            this.style.transform = 'translateY(0)';
        }});
        </script>
        '''
    
    html += '</div>'
    
    return html