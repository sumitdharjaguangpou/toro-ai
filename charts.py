# chart.py - TradingView Lightweight Charts (PRO VERSION)

import streamlit as st
import streamlit.components.v1 as components
import json
import yfinance as yf


def render_chart(symbol, levels=None, buy_signals=None, sell_signals=None):
    """
    Render professional TradingView-style chart
    """

    # =========================
    # FETCH DATA
    # =========================
    try:
        with st.spinner("📊 Loading chart..."):
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="10y", interval="1d")

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

    candles = [
        {
            "time": row["Date"].strftime("%Y-%m-%d"),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        }
        for _, row in df.iterrows()
    ]

    volumes = [
        {
            "time": row["Date"].strftime("%Y-%m-%d"),
            "value": float(row["Volume"]),
            "color": "#00ff88" if row["Close"] >= row["Open"] else "#ff1744",
        }
        for _, row in df.iterrows()
    ]

    # =========================
    # LEVELS
    # =========================
    support = levels.get("support") if levels else None
    resistance = levels.get("resistance") if levels else None
    entry = levels.get("entry") if levels else None
    target = levels.get("target") if levels else None

    # =========================
    # MARKERS (BUY/SELL)
    # =========================
    markers = []

    # BUY SIGNALS
    if buy_signals is not None and not buy_signals.empty:
        for _, row in buy_signals.iterrows():
            date = str(row["Date"])[:10]  # or row["Date"].strftime("%Y-%m-%d")
            markers.append({
                "time": date,
                "position": "belowBar",
                "color": "#00ff88",
                "shape": "arrowUp",
                "text": "BUY"
            })

    # SELL SIGNALS
    if sell_signals is not None and not sell_signals.empty:
        for _, row in sell_signals.iterrows():
            date = str(row["Date"])[:10]
            markers.append({
                "time": date,
                "position": "aboveBar",
                "color": "#ff1744",
                "shape": "arrowDown",
                "text": "SELL"
            })
    # =========================
    # HTML + JS CHART
    # =========================
    chart_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #0a0e27;
            }}
            #chart-container {{
                width: 100%;
                height: 550px;
            }}
        </style>
    </head>

    <body>
        <div id="chart-container"></div>

        <script src="https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js"></script>

        <script>
            const container = document.getElementById('chart-container');

            const chart = LightweightCharts.createChart(container, {{
                width: container.clientWidth || 900,
                height: 500,

                layout: {{
                    background: {{ color: '#0a0e27' }},
                    textColor: '#8892b0',
                }},

                grid: {{
                    vertLines: {{ color: 'rgba(0,255,255,0.08)' }},
                    horzLines: {{ color: 'rgba(0,255,255,0.08)' }},
                }},

                crosshair: {{
                    mode: LightweightCharts.CrosshairMode.Normal,
                }},

                rightPriceScale: {{
                    borderColor: 'rgba(0,255,255,0.2)',
                }},

                timeScale: {{
                    timeVisible: true,
                    secondsVisible: false,
                    borderColor: 'rgba(0,255,255,0.2)',
                }},

                handleScroll: {{
                    mouseWheel: true,
                    pressedMouseMove: true,
                }},

                handleScale: {{
                    axisPressedMouseMove: true,
                    mouseWheel: true,
                    pinch: true,
                }},
            }});

            // =========================
            // CANDLE SERIES
            // =========================
            const candleSeries = chart.addCandlestickSeries({{
                upColor: '#00ff88',
                downColor: '#ff1744',
                borderUpColor: '#00ff88',
                borderDownColor: '#ff1744',
                wickUpColor: '#00ff88',
                wickDownColor: '#ff1744',
            }});

            candleSeries.setData({json.dumps(candles)});

            // =========================
            // VOLUME SERIES
            // =========================
            const volumeSeries = chart.addHistogramSeries({{
                priceFormat: {{ type: 'volume' }},
                priceScaleId: '',
                scaleMargins: {{ top: 0.8, bottom: 0 }},
            }});

            volumeSeries.setData({json.dumps(volumes)});

            // =========================
            // MARKERS (BUY/SELL)
            // =========================
            candleSeries.setMarkers({json.dumps(markers)});
    """

    # =========================
    # PRICE LINES (CORRECTED)
    # =========================
    if support:
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {support},
            color: '#00ff88',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Dashed,
            title: 'SUPPORT'
        }});
        """

    if resistance:
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {resistance},
            color: '#ff1744',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Dashed,
            title: 'RESISTANCE'
        }});
        """

    if entry:
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {entry},
            color: '#00ffff',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Solid,
            title: 'ENTRY'
        }});
        """

    if target:
        chart_html += f"""
        candleSeries.createPriceLine({{
            price: {target},
            color: '#ffd700',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Dotted,
            title: 'TARGET'
        }});
        """

    # =========================
    # FINAL SCRIPT
    # =========================
    chart_html += """
            // Resize fix
            const resizeObserver = new ResizeObserver(() => {
                chart.applyOptions({ width: container.clientWidth });
            });

            resizeObserver.observe(container);

            chart.timeScale().fitContent();
        </script>
    </body>
    </html>
    """

    components.html(chart_html, height=500,)
