# live_data.py - Fixed version
import streamlit as st
import yfinance as yf

def live_price_fragment(stock):
    """Updates ONLY the live price"""
    try:
        ticker = yf.Ticker(stock)
        info = ticker.fast_info
        live_price = info.get("lastPrice", None)
        prev_close = info.get("previousClose", None)
        
        if live_price and prev_close:
            change = live_price - prev_close
            pct = (change / prev_close) * 100
            
            if change >= 0:
                bg = "rgba(22, 163, 74, 0.15)"
                clr = "#16a34a"
                bd = "rgba(22, 163, 74, 0.3)"
                arrow = "▲"
            else:
                bg = "rgba(220, 38, 38, 0.15)"
                clr = "#dc2626"
                bd = "rgba(220, 38, 38, 0.3)"
                arrow = "▼"
            
            html_code = f"""
            <div style="
                background: linear-gradient(135deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
                border: 1px solid rgba(0,255,255,0.2);
                border-radius: 12px;
                padding: 12px 8px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            ">
                <div style="font-size: 10px; color: #00ffff; margin-bottom: 4px; font-weight: 600; letter-spacing: 1px;">💰 LIVE PRICE</div>
                <div style="font-size: 22px; font-weight: 800; color: #ffffff; line-height: 1.1; margin-bottom: 6px;">
                    ₹{live_price:,.2f}
                </div>
                <div style="
                    display: inline-block;
                    padding: 3px 10px;
                    border-radius: 20px;
                    font-weight: 700;
                    background-color: {bg};
                    color: {clr};
                    font-size: 11px;
                    border: 1px solid {bd};
                ">
                    {arrow} ₹{abs(change):.2f} ({abs(pct):.2f}%)
                </div>
            </div>
            """
            
            st.markdown(html_code, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Live price not available")
    except Exception as e:
        st.warning(f"⚠️ Price feed unavailable")
