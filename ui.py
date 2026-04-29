import streamlit as st
import yfinance as yf
import pandas as pd
import time
from difflib import get_close_matches
from watchlist import add_to_watchlist
from live_data import live_price_fragment


st.set_page_config(
    page_title="TORO AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    except Exception as e:
     print(e)
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


#==================
# RENDER HEADER
#==================
def render_header():
    st.markdown("""
    <style>
                
    :root {
    --buy-bg: rgba(34,197,94,0.12);
    --buy-color: #16a34a;
    --buy-border: rgba(34,197,94,0.28);

    --sell-bg: rgba(239,68,68,0.12);
    --sell-color: #dc2626;
    --sell-border: rgba(239,68,68,0.28);

    --neutral-bg: rgba(245,158,11,0.12);
    --neutral-color: #d97706;
    --neutral-border: rgba(245,158,11,0.28);
}
                

    /* ===================================== */
    /* CLEAN AUTO LIGHT + DARK THEME SUPPORT */
    /* ===================================== */

    /* Streamlit native theme support */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Global spacing fix */
    .block-container {
        padding-top: 2.2rem !important;
        padding-bottom: 1rem !important;
    }

    /* Remove top white strip */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    /* Remove toolbar spacing issue */
    div[data-testid="stToolbar"] {
        top: 0.5rem;
        right: 1rem;
    }

    /* Header text */
    .header-text h1 {
        font-size: 22px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        color: inherit !important;
    }

    .header-text p {
        font-size: 11px !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0.75;
        color: inherit !important;
    }

    /* Divider */
    .divider {
        margin-top: 8px;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(150,150,150,0.25);
    }

    /* Search input width */
    div[data-testid="stTextInput"] {
        max-width: 320px !important;
    }

    @media (max-width: 768px) {
        .header-text h1 {
            font-size: 18px !important;
        }

        div[data-testid="stTextInput"] {
            max-width: 100% !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    # Better logo/title alignment
    col_img, col_text = st.columns([0.06, 0.94], gap="small")

    with col_img:
        st.image("toro_ai_logo.png", width=85)

    with col_text:
        st.markdown("""
        <div class="header-text">
            <h1>TORO AI</h1>
            <p>AI Stock Intelligence</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


# =========================
# RENDER SEARCH
# =========================
def render_search_section(stocks_dict):
    left_col, right_col = st.columns([4, 6])

    with left_col:
        # =========================
        # FUTURISTIC CSS STYLING
        # =========================
        st.markdown(
            """
            <style>
                /* Container styling */
                [data-testid="column"] {
                    background: linear-gradient(135deg, rgba(10, 20, 40, 0.95) 0%, rgba(5, 10, 20, 0.98) 100%);
                    border-radius: 20px;
                    padding: 20px;
                    border: 1px solid rgba(0, 255, 255, 0.2);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                }

                /* Search label styling */
                .search-label {
                    font-size: 14px;
                    font-weight: 700;
                    letter-spacing: 2px;
                    margin-bottom: 12px;
                    background: linear-gradient(135deg, #00ffff, #ff00ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    text-transform: uppercase;
                }

                /* Search input field */
                div[data-testid="stTextInput"] {
                    width: 100% !important;
                    margin-bottom: 20px;
                }

                div[data-testid="stTextInput"] input {
                    background: rgba(0, 20, 40, 0.8) !important;
                    border: 2px solid rgba(0, 255, 255, 0.3) !important;
                    border-radius: 12px !important;
                    color: #00ffff !important;
                    font-size: 15px !important;
                    padding: 12px 15px !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 0 10px rgba(0, 255, 255, 0.1) !important;
                }

                div[data-testid="stTextInput"] input:focus {
                    border-color: #ff00ff !important;
                    box-shadow: 0 0 20px rgba(255, 0, 255, 0.3) !important;
                    outline: none !important;
                }

                div[data-testid="stTextInput"] input::placeholder {
                    color: rgba(0, 255, 255, 0.5) !important;
                    font-size: 13px !important;
                }

                /* Caption styling */
                .stCaption {
                    color: #00ffff !important;
                    font-size: 12px !important;
                    letter-spacing: 0.5px !important;
                }

                /* Warning message styling */
                .stAlert {
                    background: rgba(255, 100, 0, 0.1) !important;
                    border: 1px solid #ff6600 !important;
                    border-radius: 10px !important;
                    color: #ffaa00 !important;
                }

                /* Futuristic Button Styling */
                div.stButton > button {
                    background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1)) !important;
                    border: 1px solid rgba(0, 255, 255, 0.5) !important;
                    border-radius: 12px !important;
                    color: #00ffff !important;
                    font-weight: 600 !important;
                    font-size: 14px !important;
                    padding: 10px 20px !important;
                    transition: all 0.3s ease !important;
                    letter-spacing: 1px !important;
                    backdrop-filter: blur(10px) !important;
                }

                div.stButton > button:hover {
                    transform: translateY(-2px) !important;
                    border-color: #ff00ff !important;
                    box-shadow: 0 0 25px rgba(255, 0, 255, 0.4) !important;
                    color: #ffffff !important;
                }

                /* Suggestion buttons styling */
                div.stButton > button[key^="suggestion_"] {
                    background: linear-gradient(135deg, rgba(0, 50, 80, 0.8), rgba(80, 0, 120, 0.8)) !important;
                    border: 1px solid rgba(0, 255, 255, 0.4) !important;
                    justify-content: space-between !important;
                    text-align: left !important;
                    font-weight: 600 !important;
                }

                div.stButton > button[key^="suggestion_"]:hover {
                    background: linear-gradient(135deg, rgba(0, 100, 150, 0.9), rgba(150, 0, 200, 0.9)) !important;
                    border-color: #ff00ff !important;
                }

                /* AI Screener Button - Special Futuristic */
                div.stButton > button[key="ai_screener_btn"] {
                    background: linear-gradient(135deg, #000428, #004e92) !important;
                    background-size: 200% 200% !important;
                    border: 2px solid rgba(0, 255, 255, 0.8) !important;
                    color: #00ffff !important;
                    font-size: 14px !important;
                    font-weight: 800 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 2px !important;
                    animation: gradientShift 3s ease infinite, pulse 2s ease-in-out infinite !important;
                    margin-top: 20px !important;
                    position: relative !important;
                    overflow: hidden !important;
                }

                @keyframes gradientShift {
                    0%, 100% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                }

                @keyframes pulse {
                    0%, 100% {
                        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
                        border-color: rgba(0, 255, 255, 0.8);
                    }
                    50% {
                        box-shadow: 0 0 40px rgba(0, 255, 255, 0.6), 0 0 20px rgba(255, 0, 255, 0.3);
                        border-color: #ff00ff;
                    }
                }

                div.stButton > button[key="ai_screener_btn"]::before {
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 0;
                    height: 0;
                    border-radius: 50%;
                    background: radial-gradient(circle, rgba(0,255,255,0.3), rgba(255,0,255,0));
                    transform: translate(-50%, -50%);
                    transition: width 0.6s, height 0.6s;
                }

                div.stButton > button[key="ai_screener_btn"]:hover::before {
                    width: 300px;
                    height: 300px;
                }

                /* Toast notifications styling */
                .stToast {
                    background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
                    border: 1px solid #00ffff !important;
                    border-radius: 12px !important;
                    color: #00ffff !important;
                }

                /* Divider styling */
                .custom-divider {
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #00ffff, #ff00ff, transparent);
                    margin: 20px 0;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Search Header with futuristic glow
        st.markdown(
            """
            <div class="search-label">
                ⚡ NEURAL SEARCH INTERFACE ⚡
            </div>
            <div class="custom-divider"></div>
            """,
            unsafe_allow_html=True
        )

        # =========================
        # SEARCH INPUT
        # =========================
        search = st.text_input(
            "",
            placeholder="🔍 ENTER STOCK SYMBOL...",
            label_visibility="collapsed",
            key="search_input"
        ).upper().strip()

        stock = ""
        matches = []

        if search:
            # Exact match
            if search in stocks_dict:
                matches = [search]

            # Starts with
            elif any(name.startswith(search) for name in stocks_dict.keys()):
                matches = [
                    name for name in stocks_dict.keys()
                    if name.startswith(search)
                ][:5]

            # Contains
            elif any(search in name for name in stocks_dict.keys()):
                matches = [
                    name for name in stocks_dict.keys()
                    if search in name
                ][:5]

            # Fuzzy match
            else:
                matches = get_close_matches(
                    search,
                    list(stocks_dict.keys()),
                    n=5,
                    cutoff=0.7
                )

            if matches:
                st.markdown(
                    """
                    <div style="color: #00ffff; font-size: 12px; margin: 10px 0 5px 0; letter-spacing: 1px;">
                        ━━━ AI SUGGESTIONS ━━━
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Display suggestion buttons
                for i, match in enumerate(matches[:3]):  # Show top 3 suggestions
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        if st.button(
                            f"📊 {match}",
                            key=f"suggestion_{i}",
                            use_container_width=True,
                            help=f"Select {match}"
                        ):
                            stock = stocks_dict[match]
                            st.session_state.selected_stock = stock
                            st.session_state.selected_symbol = match
                            st.toast(f"🎯 {match} selected!", icon="✅")
                    
                    with col2:
                        if st.button(
                            "⭐",
                            key=f"watchlist_{i}",
                            help=f"Add {match} to watchlist"
                        ):
                            if add_to_watchlist(stocks_dict[match], match):
                                st.toast(f"⭐ {match} added to watchlist!", icon="✨")
                            else:
                                st.toast(f"⚠️ {match} already in watchlist!", icon="📌")

                if matches and not stock:
                    # Auto-select the first match
                    stock = stocks_dict[matches[0]]
                    
                if stock:
                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1));
                            border-left: 4px solid #00ffff;
                            border-radius: 8px;
                            padding: 10px;
                            margin: 10px 0;
                        ">
                            <span style="color: #00ffff; font-size: 12px;">🎯 ACTIVE STOCK:</span>
                            <span style="color: #ffffff; font-weight: bold; margin-left: 10px;">{matches[0]}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                stock = search if ".NS" in search else search + ".NS"
                st.warning(f"🔍 No match found. Using fallback: {stock}")

        else:
            st.markdown(
                """
                <div style="
                    background: rgba(0, 255, 255, 0.05);
                    border-radius: 10px;
                    padding: 15px;
                    text-align: center;
                    margin: 10px 0;
                ">
                    <span style="color: rgba(0, 255, 255, 0.7); font-size: 13px;">
                        💡 Begin typing a stock symbol to activate neural search...
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

        # =========================
        # AI SMART SCREENER BUTTON
        # =========================
        screener_clicked = st.button(
            "🤖 AI QUANTUM SCREENER ⚡",
            key="ai_screener_btn",
            use_container_width=True,
            help="Activate Advanced AI-Powered Stock Screening"
        )

    with right_col:
        # You can add additional content here
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
