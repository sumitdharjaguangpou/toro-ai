# chart.py - Mobile-Friendly TradingView Chart (Fixed + Optimized)

import streamlit as st
import streamlit.components.v1 as components
import json
import yfinance as yf
import pandas as pd
import numpy as np
import html


# ==========================================
# CACHE DATA
# ==========================================
@st.cache_data(ttl=3600)
def fetch_chart_data(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period="5y", interval="1d")


# ==========================================
# MAIN CHART FUNCTION
# ==========================================
def render_chart(symbol, levels=None, buy_signals=None, sell_signals=None):
    """
    Render professional TradingView-style chart - Mobile Friendly
    """

    # =========================
    # FETCH DATA
    # =========================
    try:
        with st.spinner("📊 Loading chart..."):
            df = fetch_chart_data(symbol)

        if df.empty:
            st.warning(f"No data available for {symbol}")
            return

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    # =========================
    # PREPARE DATA
    # =========================
    df = df.reset_index()

    date_col = "Date" if "Date" in df.columns else "Datetime"

    df["TimeStr"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")

    records = df.to_dict("records")

    candles = [
        {
            "time": r["TimeStr"],
            "open": float(r["Open"]),
            "high": float(r["High"]),
            "low": float(r["Low"]),
            "close": float(r["Close"]),
        }
        for r in records
    ]

    volumes = [
        {
            "time": r["TimeStr"],
            "value": float(r["Volume"]),
            "color": (
                "rgba(0, 255, 136, 0.4)"
                if r["Close"] >= r["Open"]
                else "rgba(255, 23, 68, 0.4)"
            ),
        }
        for r in records
    ]

    # =========================
    # METRICS
    # =========================
    current_price = df["Close"].iloc[-1]

    if len(df) > 1:
        price_change = df["Close"].iloc[-1] - df["Close"].iloc[-2]
        price_change_pct = (price_change / df["Close"].iloc[-2]) * 100
    else:
        price_change = 0
        price_change_pct = 0

    # =========================
    # LEVELS
    # =========================
    support = levels.get("stoploss") if levels else np.nan
    resistance = levels.get("target") if levels else np.nan
    entry = levels.get("entry") if levels else np.nan

    support_display = (
        f"₹{support:.2f}" if pd.notna(support) else "N/A"
    )

    resistance_display = (
        f"₹{resistance:.2f}" if pd.notna(resistance) else "N/A"
    )

    entry_display = (
        f"₹{entry:.2f}" if pd.notna(entry) else "N/A"
    )

    # =========================
    # MARKERS
    # =========================
    markers = []
    seen_dates = set()

    # BUY SIGNALS
    if buy_signals is not None and not buy_signals.empty:
        for idx, _ in buy_signals.iterrows():

            date = pd.to_datetime(idx).strftime("%Y-%m-%d")

            if date not in seen_dates:
                markers.append({
                    "time": date,
                    "position": "belowBar",
                    "color": "#00ff88",
                    "shape": "arrowUp",
                    "text": "BUY",
                    "size": 1
                })

                seen_dates.add(date)

    # SELL SIGNALS
    if sell_signals is not None and not sell_signals.empty:
        for idx, _ in sell_signals.iterrows():

            date = pd.to_datetime(idx).strftime("%Y-%m-%d")

            if date not in seen_dates:
                markers.append({
                    "time": date,
                    "position": "aboveBar",
                    "color": "#ff1744",
                    "shape": "arrowDown",
                    "text": "SELL",
                    "size": 1
                })

                seen_dates.add(date)

    # =========================
    # COLORS
    # =========================
    if price_change >= 0:
        price_color = "#00ff88"
        change_symbol = "▲"
        change_color = "#00ff88"
    else:
        price_color = "#ff1744"
        change_symbol = "▼"
        change_color = "#ff1744"

    # =========================
    # SAFE SYMBOL
    # =========================
    safe_symbol = html.escape(
        symbol.replace(".NS", "").replace(".BO", "")
    )

    # =========================
    # HTML
    # =========================
    chart_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width,
              initial-scale=1.0,
              user-scalable=no">

        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: #0a0e27;
                font-family: -apple-system,
                             BlinkMacSystemFont,
                             'Segoe UI',
                             Roboto,
                             'Helvetica Neue',
                             Arial,
                             sans-serif;
                -webkit-tap-highlight-color: transparent;
            }}

            .chart-container-wrapper {{
                background: linear-gradient(
                    135deg,
                    #0a0e27,
                    #0c1030
                );

                border-radius: 16px;
                border: 1px solid rgba(0, 255, 255, 0.2);
                padding: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            }}

            .chart-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(0,255,255,0.15);
                flex-wrap: wrap;
                gap: 8px;
            }}

            .symbol-info {{
                display: flex;
                align-items: baseline;
                gap: 8px;
                flex-wrap: wrap;
            }}

            .symbol-name {{
                font-size: 18px;
                font-weight: 700;
                color: #ffffff;
                letter-spacing: 0.5px;
            }}

            .exchange {{
                font-size: 9px;
                color: #64748b;
                background: rgba(100,116,139,0.2);
                padding: 2px 6px;
                border-radius: 10px;
            }}

            .price-info {{
                display: flex;
                align-items: baseline;
                gap: 8px;
                flex-wrap: wrap;
            }}

            .current-price {{
                font-size: 22px;
                font-weight: 700;
                color: {price_color};
                letter-spacing: 0.5px;
            }}

            .price-change {{
                font-size: 11px;
                font-weight: 600;
                color: {change_color};
            }}

            .price-change-percent {{
                font-size: 11px;
                font-weight: 600;
                color: {change_color};
            }}

            .timeframe-selector {{
                display: flex;
                gap: 4px;
                background: rgba(10,20,40,0.6);
                padding: 3px 6px;
                border-radius: 16px;
                border: 1px solid rgba(0,255,255,0.15);
                flex-wrap: wrap;
            }}

            .timeframe-btn {{
                font-size: 9px;
                font-weight: 600;
                padding: 3px 8px;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
                color: #8892b0;
                background: transparent;
                border: none;
                -webkit-tap-highlight-color: transparent;
            }}

            .timeframe-btn.active {{
                background: rgba(0,255,255,0.15);
                color: #00ffff;
                border: 1px solid rgba(0,255,255,0.3);
            }}

            .timeframe-btn:hover {{
                background: rgba(0,255,255,0.08);
                color: #00e5ff;
            }}

            #chart-container {{
                width: 100%;
                height: 400px;
                border-radius: 12px;
                touch-action: manipulation;
            }}

            .chart-footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
                padding-top: 8px;
                border-top: 1px solid rgba(0,255,255,0.1);
                font-size: 9px;
                color: #64748b;
                flex-wrap: wrap;
                gap: 6px;
            }}

            .level-indicators {{
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }}

            .level {{
                display: flex;
                align-items: center;
                gap: 4px;
            }}

            .level-color {{
                width: 10px;
                height: 10px;
                border-radius: 2px;
            }}

            .level-label {{
                font-size: 9px;
                color: #8892b0;
            }}

            .level-value {{
                font-size: 9px;
                font-weight: 600;
                color: #ffffff;
            }}

            @media (max-width: 768px) {{
                .chart-container-wrapper {{
                    padding: 10px;
                }}

                .symbol-name {{
                    font-size: 14px;
                }}

                .current-price {{
                    font-size: 18px;
                }}

                .price-change,
                .price-change-percent {{
                    font-size: 10px;
                }}

                #chart-container {{
                    height: 320px;
                }}

                .timeframe-btn {{
                    font-size: 8px;
                    padding: 2px 6px;
                }}

                .level-label,
                .level-value {{
                    font-size: 8px;
                }}

                .chart-footer {{
                    font-size: 7px;
                }}
            }}

            @media (max-width: 480px) {{
                .chart-container-wrapper {{
                    padding: 8px;
                }}

                .symbol-name {{
                    font-size: 12px;
                }}

                .current-price {{
                    font-size: 16px;
                }}

                #chart-container {{
                    height: 280px;
                }}

                .timeframe-selector {{
                    gap: 2px;
                }}

                .timeframe-btn {{
                    font-size: 7px;
                    padding: 2px 5px;
                }}
            }}
        </style>
    </head>

    <body>

        <div class="chart-container-wrapper">

            <div class="chart-header">

                <div class="symbol-info">

                    <span class="symbol-name">
                        {safe_symbol}
                    </span>

                    <span class="exchange">
                        NSE
                    </span>

                    <div class="price-info">

                        <span class="current-price">
                            ₹{current_price:.2f}
                        </span>

                        <span class="price-change">
                            {change_symbol} ₹{abs(price_change):.2f}
                        </span>

                        <span class="price-change-percent">
                            {change_symbol} {abs(price_change_pct):.2f}%
                        </span>

                    </div>
                </div>

                <div class="timeframe-selector">
                    <button class="timeframe-btn"
                            data-timeframe="1M">1M</button>

                    <button class="timeframe-btn"
                            data-timeframe="3M">3M</button>

                    <button class="timeframe-btn"
                            data-timeframe="6M">6M</button>

                    <button class="timeframe-btn active"
                            data-timeframe="1Y">1Y</button>

                    <button class="timeframe-btn"
                            data-timeframe="2Y">2Y</button>

                    <button class="timeframe-btn"
                            data-timeframe="ALL">ALL</button>
                </div>

            </div>

            <div id="chart-container"></div>

            <div class="chart-footer">

                <div class="level-indicators">

                    <div class="level">
                        <div class="level-color"
                             style="background:#00ff88;">
                        </div>

                        <span class="level-label">
                            SUPPORT
                        </span>

                        <span class="level-value">
                            {support_display}
                        </span>
                    </div>

                    <div class="level">
                        <div class="level-color"
                             style="background:#ff1744;">
                        </div>

                        <span class="level-label">
                            RESISTANCE
                        </span>

                        <span class="level-value">
                            {resistance_display}
                        </span>
                    </div>

                    <div class="level">
                        <div class="level-color"
                             style="background:#00ffff;">
                        </div>

                        <span class="level-label">
                            ENTRY
                        </span>

                        <span class="level-value">
                            {entry_display}
                        </span>
                    </div>

                </div>

                <div>
                    👆 Drag | ✌️ Pinch | 👆 Double-tap
                </div>

            </div>

        </div>

        <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>

        <script>

            const container =
                document.getElementById('chart-container');

            if (typeof LightweightCharts === 'undefined') {{

                container.innerHTML =
                    '<div style="color:white;padding:20px;">Chart library failed to load.</div>';

            }} else {{

                const fullCandles =
                    {json.dumps(candles)};

                const fullVolumes =
                    {json.dumps(volumes)};

                const markers =
                    {json.dumps(markers)};

                const chart =
                    LightweightCharts.createChart(container, {{

                    width: container.clientWidth,
                    height: container.clientHeight,

                    layout: {{
                        background: {{ color: 'transparent' }},
                        textColor: '#8892b0',
                        fontSize: 10,
                    }},

                    grid: {{
                        vertLines: {{
                            color: 'rgba(0,255,255,0.06)'
                        }},
                        horzLines: {{
                            color: 'rgba(0,255,255,0.06)'
                        }},
                    }},

                    crosshair: {{
                        mode:
                            LightweightCharts.CrosshairMode.Normal,
                    }},

                    rightPriceScale: {{
                        borderColor:
                            'rgba(0,255,255,0.2)',

                        scaleMargins: {{
                            top: 0.05,
                            bottom: 0.2
                        }},
                    }},

                    timeScale: {{
                        timeVisible: true,
                        secondsVisible: false,
                        borderColor:
                            'rgba(0,255,255,0.2)',
                    }},

                    handleScroll: {{
                        mouseWheel: true,
                        pressedMouseMove: true,
                        horzTouchDrag: true,
                        vertTouchDrag: true,
                    }},

                    handleScale: {{
                        mouseWheel: true,
                        pinch: true,
                    }}

                }});

                // =========================
                // SERIES
                // =========================
                const candleSeries =
                    chart.addCandlestickSeries({{

                    upColor: '#00ff88',
                    downColor: '#ff1744',
                    borderUpColor: '#00ff88',
                    borderDownColor: '#ff1744',
                    wickUpColor: '#00ff88',
                    wickDownColor: '#ff1744',

                }});

                const volumeSeries =
                    chart.addHistogramSeries({{

                    priceFormat: {{
                        type: 'volume'
                    }},

                    priceScaleId: '',

                    scaleMargins: {{
                        top: 0.8,
                        bottom: 0
                    }}

                }});

                // =========================
                // FILTER FUNCTION
                // =========================
                function filterData(data, timeframe) {{

                    if (timeframe === 'ALL')
                        return data;

                    const lastDate =
                        new Date(
                            data[data.length - 1].time
                        );

                    let cutoff;

                    const DAY =
                        24 * 60 * 60 * 1000;

                    switch(timeframe) {{

                        case '1M':
                            cutoff =
                                new Date(
                                    lastDate.getTime()
                                    - 30 * DAY
                                );
                            break;

                        case '3M':
                            cutoff =
                                new Date(
                                    lastDate.getTime()
                                    - 90 * DAY
                                );
                            break;

                        case '6M':
                            cutoff =
                                new Date(
                                    lastDate.getTime()
                                    - 180 * DAY
                                );
                            break;

                        case '1Y':
                            cutoff =
                                new Date(
                                    lastDate.getTime()
                                    - 365 * DAY
                                );
                            break;

                        case '2Y':
                            cutoff =
                                new Date(
                                    lastDate.getTime()
                                    - 730 * DAY
                                );
                            break;

                        default:
                            return data;
                    }}

                    return data.filter(
                        d => new Date(d.time) >= cutoff
                    );
                }}

                // =========================
                // SET TIMEFRAME
                // =========================
                function setTimeframe(tf) {{

                    const candleData =
                        filterData(fullCandles, tf);

                    const volumeData =
                        filterData(fullVolumes, tf);

                    candleSeries.setData(candleData);
                    volumeSeries.setData(volumeData);

                    candleSeries.setMarkers(markers);

                    chart.timeScale().fitContent();
                }}

                // =========================
                // INITIAL DATA
                // =========================
                setTimeframe('1Y');

    """

    # =========================
    # PRICE LINES
    # =========================
    if pd.notna(support):
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {support},
            color: '#00ff88',
            lineWidth: 2,
            lineStyle: 2,
            axisLabelVisible: true,
            title: ''
        }});
        """

    if pd.notna(resistance):
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {resistance},
            color: '#ff1744',
            lineWidth: 2,
            lineStyle: 2,
            axisLabelVisible: true,
            title: ''
        }});
        """

    if pd.notna(entry):
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {entry},
            color: '#00ffff',
            lineWidth: 2,
            lineStyle: 0,
            axisLabelVisible: true,
            title: ''
        }});
        """

    # =========================
    # FINAL JS
    # =========================
    chart_html += """
                // =========================
                // BUTTONS
                // =========================
                document.querySelectorAll('.timeframe-btn')
                    .forEach(btn => {

                    btn.addEventListener('click', () => {

                        document.querySelectorAll(
                            '.timeframe-btn'
                        ).forEach(
                            b => b.classList.remove('active')
                        );

                        btn.classList.add('active');

                        const tf =
                            btn.getAttribute(
                                'data-timeframe'
                            );

                        setTimeframe(tf);

                    });

                });

                // =========================
                // RESIZE
                // =========================
                const resizeObserver =
                    new ResizeObserver(() => {

                    chart.applyOptions({
                        width: container.clientWidth
                    });

                    chart.timeScale().fitContent();

                });

                resizeObserver.observe(container);

                window.addEventListener(
                    'beforeunload',
                    () => resizeObserver.disconnect()
                );

            }

        </script>

    </body>
    </html>
    """

    # =========================
    # RENDER
    # =========================
    components.html(
        chart_html,
        height=520,
        scrolling=False
    )
