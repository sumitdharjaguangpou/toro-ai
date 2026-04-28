# live_data.py
import streamlit as st
import yfinance as yf

@st.fragment(run_every=5)
def live_price_fragment(stock):
    """Updates ONLY the live price every 5 seconds"""
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
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 4px;
                text-align: center;
            ">
                <div style="font-size: 10px; color: #64748b; margin-bottom: 2px; font-weight: 600;">💰 LIVE</div>
                <div style="font-size: 18px; font-weight: 700; color: #0f172a; line-height: 1.1; margin-bottom: 4px;">
                    ₹{live_price:,.2f}
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
                    {arrow} ₹{abs(change):.2f} ({abs(pct):.2f}%)
                </div>
            </div>
            """
            
            st.markdown(html_code, unsafe_allow_html=True)
    except:
        pass