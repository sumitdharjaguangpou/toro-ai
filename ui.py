import streamlit as st
import yfinance as yf
import pandas as pd
import time
from difflib import get_close_matches

# ══════════════════════════
# SESSION STATE
# ══════════════════════════
if "price_cache" not in st.session_state:
    st.session_state.price_cache = {}

# ══════════════════════════
# HELPER FUNCTIONS (TOP)
# ══════════════════════════
def get_realtime_price(stock):
    """Get real-time price without full fetch"""
    try:
        ticker = yf.Ticker(stock)
        info = ticker.fast_info
        live_price = info.get("lastPrice", None)
        prev_close = info.get("previousClose", None)
        
        if live_price and prev_close:
            change = live_price - prev_close
            pct = (change / prev_close) * 100
            return {
                'price': live_price,
                'change': change,
                'pct': pct,
                'timestamp': time.time()
            }
    except:
        pass
    return None

# DELTA
def get_delta_update(stock):
    """Only update price if 3+ seconds passed"""
    current_time = time.time()
    
    if "price_cache" not in st.session_state:
        st.session_state.price_cache = {}
    
    if stock in st.session_state.price_cache:
        cached = st.session_state.price_cache[stock]
        if current_time - cached['timestamp'] < 3:
            return cached
    
    price_data = get_realtime_price(stock)
    if price_data and price_data['price']:
        st.session_state.price_cache[stock] = price_data
    
    return price_data

# ══════════════════════════
# RENDER HEADER
# ══════════════════════════
def render_header():
    st.set_page_config(
        page_title="TORO AI",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>

    /* ============================= */
    /* PREMIUM THEME + FIXED HEADER  */
    /* ============================= */

    :root {
        --bg-primary: #F8FAFC;
        --bg-card: #FFFFFF;
        --text-primary: #0F172A;
        --text-secondary: #64748B;
        --border-color: #E2E8F0;
        --ai-accent: #4F46E5;
    }

    /* Dark Mode Support */
    [data-theme="dark"],
    .dark,
    .stApp[data-theme="dark"] {
        --bg-primary: #0B1120;
        --bg-card: #111827;
        --text-primary: #F8FAFC;
        --text-secondary: #CBD5E1;
        --border-color: #334155;
        --ai-accent: #818CF8;
    }

    /* Full Background */
    .stApp,
    .main,
    .block-container {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* VERY IMPORTANT → fixes hidden top logo */
    .block-container {
        padding-top: 2.5rem !important;
    }

    /* Remove white top strip */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    /* Header Title */
    .header-text h1 {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
    }

    .header-text p {
        font-size: 11px !important;
        color: var(--text-secondary) !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .divider {
        margin-top: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    @media (max-width: 768px) {
        .header-text h1 {
            font-size: 18px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    # slightly bigger left column so full logo is visible
    col_img, col_text = st.columns([0.05, 0.93], gap="small")

    with col_img:
        # slightly smaller to avoid top cut
        st.image("toro_ai_logo.png", width=100)

    with col_text:
        st.markdown("""
        <div class="header-text">
            <h1>TORO AI</h1>
            <p>AI Stock Intelligence</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# RENDER SEARCH
def render_search_section(stocks_dict):
    left_col, right_col = st.columns([4, 6])

    with left_col:
        st.markdown(
            """
            <div style="font-size: 13px; color: var(--text-secondary); font-weight: 600; letter-spacing: 0.5px; margin-bottom: 6px;">
                🔍 SEARCH
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <style>
                div[data-testid="stTextInput"] {
                    max-width: 320px !important;
                }
                @media (max-width: 768px) {
                    div[data-testid="stTextInput"] {
                        max-width: 100% !important;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        search = st.text_input(
            "",
            placeholder="Symbol...",
            label_visibility="collapsed",
            key="search_input"
        ).upper().strip()

        stock = ""

        if search:
            # First try exact match
            if search in stocks_dict:
                stock = stocks_dict[search]
                matches = [search]
            else:
                # Try partial match with stricter cutoff
                matches = get_close_matches(search, list(stocks_dict.keys()), n=4, cutoff=0.5)
                
                if not matches:
                    # Try matching by searching INSIDE stock names
                    matches = [name for name in stocks_dict.keys() if search in name][:4]
                
                if matches:
                    stock = stocks_dict[matches[0]]
                else:
                    stock = search if ".NS" in search else search + ".NS"
                    matches = []
            
            if matches:
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.caption(f"✅ {matches[0]}")
                with col_b:
                    from watchlist import add_to_watchlist
                    if st.button("⭐", key="add_watchlist", help="Add to watchlist"):
                        if add_to_watchlist(stock, matches[0]):
                            st.toast(f"✅ {matches[0]} added!", icon="⭐")
                        else:
                            st.toast("Already in watchlist!", icon="⚠️")
            else:
                st.caption(f"🔍 No match. Using: {stock}")
        else:
            st.caption("💡 Type RELIANCE, TCS, INFY...")

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        screener_clicked = st.button("🔍 Run Smart Screener")

    with right_col:
        pass

    return search, stock, screener_clicked



# RENDER METRICS
def render_metrics(data, buy, sell, stock):
    st.markdown("## 📊 Market Overview")

    st.markdown("""
        <style>
            div[data-testid="column"] {
                padding: 0 4px !important;
            }
            .stMarkdown {
                margin-bottom: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # ── BOX 1: LIVE PRICE ──
    with col1:
        from live_data import live_price_fragment
        live_price_fragment(stock)

    # ── BOX 2: RSI ──
    with col2:
        rsi = data['RSI'].iloc[-1]
        if rsi > 70:
            status, icon = "Overbought", "🔴"
            bg, clr, bd = "var(--sell-bg)", "var(--sell-color)", "var(--sell-border)"
        elif rsi < 30:
            status, icon = "Oversold", "🟢"
            bg, clr, bd = "var(--buy-bg)", "var(--buy-color)", "var(--buy-border)"
        else:
            status, icon = "Neutral", "🟡"
            bg, clr, bd = "var(--neutral-bg)", "var(--neutral-color)", "var(--neutral-border)"

        st.markdown(
            f"""
            <div style="
                background: var(--bg-primary, #ffffff);
                border: 1px solid var(--border-color, #e2e8f0);
                border-radius: 8px;
                padding: 8px 4px;
                text-align: center;
            ">
                <div style="font-size: 10px; color: var(--text-secondary, #64748b); margin-bottom: 2px; font-weight: 600;">📈 RSI</div>
                <div style="font-size: 18px; font-weight: 700; color: var(--text-primary, #0f172a); line-height: 1.1; margin-bottom: 4px;">
                    {rsi:.1f}
                </div>
                <div style="
                    display: inline-block;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-weight: 600;
                    background-color: {bg};
                    color: {clr};
                    font-size: 10px;
                    border: 1px solid {bd};
                ">
                    {icon} {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ── BOX 3: VOLUME ──
    with col3:
        current_volume = data['Volume'].iloc[-1]
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]

        if current_volume >= 1e7:
            vol_display = f"{current_volume/1e7:.2f}Cr"
        elif current_volume >= 1e5:
            vol_display = f"{current_volume/1e5:.2f}L"
        elif current_volume >= 1e3:
            vol_display = f"{current_volume/1e3:.2f}K"
        else:
            vol_display = f"{current_volume:.0f}"

        if pd.notna(avg_volume):
            vol_ratio = (current_volume / avg_volume - 1) * 100
            if vol_ratio > 20:
                vol_status, vol_icon = "High", "🔥"
                bg, clr, bd = "var(--buy-bg)", "var(--buy-color)", "var(--buy-border)"
            elif vol_ratio < -20:
                vol_status, vol_icon = "Low", "❄️"
                bg, clr, bd = "var(--sell-bg)", "var(--sell-color)", "var(--sell-border)"
            else:
                vol_status, vol_icon = "Avg", "📊"
                bg, clr, bd = "var(--neutral-bg)", "var(--neutral-color)", "var(--neutral-border)"
        else:
            vol_status, vol_icon = "N/A", "📊"
            bg, clr, bd = "var(--bg-tertiary, #f1f5f9)", "var(--text-muted, #94a3b8)", "var(--border-color, #e2e8f0)"

        st.markdown(
            f"""
            <div style="
                background: var(--bg-primary, #ffffff);
                border: 1px solid var(--border-color, #e2e8f0);
                border-radius: 8px;
                padding: 8px 4px;
                text-align: center;
            ">
                <div style="font-size: 10px; color: var(--text-secondary, #64748b); margin-bottom: 2px; font-weight: 600;">📊 VOL</div>
                <div style="font-size: 18px; font-weight: 700; color: var(--text-primary, #0f172a); line-height: 1.1; margin-bottom: 4px;">
                    {vol_display}
                </div>
                <div style="
                    display: inline-block;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-weight: 600;
                    background-color: {bg};
                    color: {clr};
                    font-size: 10px;
                    border: 1px solid {bd};
                ">
                    {vol_icon} {vol_status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ── BOX 4: SIGNAL ──
    with col4:
        ma50 = data['Close'].rolling(50).mean().iloc[-1]
        current_price = data['Close'].iloc[-1]

        if pd.notna(ma50) and current_price > ma50:
            trend, t_icon = "UPTREND", "📈"
            t_bg, t_clr, t_bd = "var(--buy-bg)", "var(--buy-color)", "var(--buy-border)"
        else:
            trend, t_icon = "DOWNTREND", "📉"
            t_bg, t_clr, t_bd = "var(--sell-bg)", "var(--sell-color)", "var(--sell-border)"

        signal = data['Signal'].iloc[-1] if 'Signal' in data.columns else 0
        if signal == 1:
            sig_text, s_icon = "BUY", "🟢"
            s_bg, s_clr, s_bd = "var(--buy-bg)", "var(--buy-color)", "var(--buy-border)"
        elif signal == -1:
            sig_text, s_icon = "SELL", "🔴"
            s_bg, s_clr, s_bd = "var(--sell-bg)", "var(--sell-color)", "var(--sell-border)"
        else:
            sig_text, s_icon = "HOLD", "🟡"
            s_bg, s_clr, s_bd = "var(--neutral-bg)", "var(--neutral-color)", "var(--neutral-border)"

        st.markdown(
            f"""
            <div style="
                background: var(--bg-primary, #ffffff);
                border: 1px solid var(--border-color, #e2e8f0);
                border-radius: 8px;
                padding: 8px 4px;
                text-align: center;
            ">
                <div style="font-size: 10px; color: var(--text-secondary, #64748b); margin-bottom: 2px; font-weight: 600;">📊 SIGNAL</div>
                <div style="margin-bottom: 4px;">
                    <span style="
                        display: inline-block;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 700;
                        background-color: {t_bg};
                        color: {t_clr};
                        font-size: 10px;
                        border: 1px solid {t_bd};
                    ">{t_icon} {trend}</span>
                </div>
                <div>
                    <span style="
                        display: inline-block;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 700;
                        background-color: {s_bg};
                        color: {s_clr};
                        font-size: 10px;
                        border: 1px solid {s_bd};
                    ">{s_icon} {sig_text}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# RENDER NEWS
def render_news(news):
    st.subheader("📰 Market News")

    for item in news:
        st.markdown(
            f"""
            <div style='
                background: var(--bg-primary, #ffffff);
                border: 1px solid var(--border-color, #e2e8f0);
                border-radius: 6px;
                padding: 8px;
                margin-bottom: 8px;
            '>
                <p style='margin:0; font-size:15px; line-height:1.4;'>
                    🔹 <a href='{item['link']}' target='_blank' style='text-decoration:none; color: var(--ai-border, #6366f1);'>
                        {item['title']}
                    </a>
                </p>
                <p style='color: var(--text-muted, #94a3b8); font-size:12px; margin:4px 0 0 0;'>
                    🏢 {item['source']} • ⏱ {item['time']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# RENDER CONTACT
def render_contact():
    st.markdown("---")
    st.markdown("### 📬 Contact & Support")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
<div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">

<a href="mailto:sumitdharjaguangpou@gmail.com" style="
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 8px;
    background: rgba(22,163,74,0.1);
    color: #16a34a;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid rgba(22,163,74,0.3);
">
✉️ Gmail
</a>

<a href="https://linkedin.com/in/sumit-dhar-9a02a628b" target="_blank" style="
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 8px;
    background: rgba(99,102,241,0.1);
    color: #6366f1;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid rgba(99,102,241,0.3);
">
💼 LinkedIn
</a>

</div>
""", unsafe_allow_html=True)