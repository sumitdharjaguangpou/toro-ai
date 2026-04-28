import matplotlib.pyplot as plt
import plotly
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import pandas as pd


#PRICE CHART
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd

def plot_price_chart(data, buy, sell, timeframe="Daily"):
    """
    data : DataFrame with columns [Open, High, Low, Close, Volume] and DateTime index
    buy  : DataFrame of buy signals (same index as data)
    sell : DataFrame of sell signals (same index as data)
    timeframe : "Daily", "Weekly", "Monthly", "5 Min", "15 Min", "1 Hour"
    """

    # ==========================================
    # ⏱️ ULTRA-COMPACT TIMEFRAME + CHART TYPE
    # ==========================================
    col1, col2, col3, col4 = st.columns([0.5, 1.5, 0.5, 1.5])
    
    with col1:
        st.markdown('<p style="font-size:11px; margin:0; padding-top:8px;">⏱️</p>', unsafe_allow_html=True)
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["Daily", "Weekly", "Monthly", "5 Min", "15 Min", "1 Hour"],
            index=["Daily", "Weekly", "Monthly", "5 Min", "15 Min", "1 Hour"].index(timeframe) if timeframe in ["Daily", "Weekly", "Monthly", "5 Min", "15 Min", "1 Hour"] else 0,
            label_visibility="collapsed",
            key="timeframe_chart"
        )
    
    with col3:
        st.markdown('<p style="font-size:11px; margin:0; padding-top:8px;">📊</p>', unsafe_allow_html=True)
    
    with col4:
        chart_style = st.radio(
            "Chart Type",
            ["📉", "📈"],
            horizontal=True,
            label_visibility="collapsed",
            index=0,
            key="chart_style_radio"
        )
    
    chart_type = "📉 Candlestick" if chart_style == "📉" else "📈 Line"

    # ── Resample logic ──
    resample_map = {
        "Weekly": "W",
        "Monthly": "ME",
        "5 Min": "5min",
        "15 Min": "15min",
        "1 Hour": "1h",
    }

    if timeframe in resample_map:
        rule = resample_map[timeframe]
        data_resampled = data.resample(rule).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()

        if not buy.empty:
            buy_resampled = buy.resample(rule).agg({'Close': 'last'}).dropna()
            buy_resampled = buy_resampled[buy_resampled.index.isin(buy.index)]
        else:
            buy_resampled = pd.DataFrame(columns=['Close'])

        if not sell.empty:
            sell_resampled = sell.resample(rule).agg({'Close': 'last'}).dropna()
            sell_resampled = sell_resampled[sell_resampled.index.isin(sell.index)]
        else:
            sell_resampled = pd.DataFrame(columns=['Close'])

        data = data_resampled
        buy = buy_resampled
        sell = sell_resampled

    # Moving averages
    ma1, ma2 = 20, 50
    ma1_series = data['Close'].rolling(ma1).mean()
    ma2_series = data['Close'].rolling(ma2).mean()

    # Subplot
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.03,
    )

    # ── Row 1: Price ──
    if chart_type == "📉 Candlestick":
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="OHLC",
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350',
            showlegend=True
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Close'],
            mode='lines', name='Close',
            line=dict(color='#64b5f6', width=1.8)
        ), row=1, col=1)

    # MAs
    fig.add_trace(go.Scatter(
        x=data.index, y=ma1_series,
        mode='lines', name=f'MA{ma1}',
        line=dict(color='#ffb74d', width=1.2, dash='dot')
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data.index, y=ma2_series,
        mode='lines', name=f'MA{ma2}',
        line=dict(color='#81c784', width=1.2, dash='dot')
    ), row=1, col=1)

    # Buy / Sell signals
    if not buy.empty:
        fig.add_trace(go.Scatter(
            x=buy.index, y=buy['Close'],
            mode='markers', name='Buy',
            marker=dict(symbol='triangle-up', color='#00e676', size=12,
                        line=dict(color='black', width=1)),
            hovertemplate='BUY @ ₹%{y:.2f}<extra></extra>'
        ), row=1, col=1)

    if not sell.empty:
        fig.add_trace(go.Scatter(
            x=sell.index, y=sell['Close'],
            mode='markers', name='Sell',
            marker=dict(symbol='triangle-down', color='#ff1744', size=12,
                        line=dict(color='black', width=1)),
            hovertemplate='SELL @ ₹%{y:.2f}<extra></extra>'
        ), row=1, col=1)

    # Volume bars
    colors = ['#26a69a' if data['Close'].iloc[i] > data['Open'].iloc[i] else '#ef5350'
              for i in range(len(data))]
    fig.add_trace(go.Bar(
        x=data.index, y=data['Volume'],
        name='Volume',
        marker=dict(color=colors, opacity=0.6),
        showlegend=False
    ), row=2, col=1)

    # ── Layout (NO range selector buttons) ──
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e1e1e", font_color="#e0e0e0", font_size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0.3)"
        ),
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        dragmode="pan",
        xaxis=dict(
            rangeslider=dict(visible=False),
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False
        ),
        yaxis=dict(
            title="Price (₹)",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False,
            side="right"
        ),
        yaxis2=dict(
            title="Volume",
            showgrid=False,
            zeroline=False
        ),
        xaxis2=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.08)',
            zeroline=False
        )
    )

    # Smart dates
    fig.update_xaxes(
        tickformatstops=[
            dict(dtickrange=[None, "M1"], value="%d %b"),
            dict(dtickrange=["M1", "M6"], value="%b '%y"),
            dict(dtickrange=["M6", None], value="%b %Y"),
        ],
        ticklabelmode="period",
        tickfont=dict(color="#b0b0b0", size=10),
        row=1, col=1
    )
    fig.update_xaxes(
        tickformatstops=[
            dict(dtickrange=[None, "M1"], value="%d %b"),
            dict(dtickrange=["M1", "M6"], value="%b '%y"),
            dict(dtickrange=["M6", None], value="%b %Y"),
        ],
        ticklabelmode="period",
        tickfont=dict(color="#b0b0b0", size=9),
        row=2, col=1
    )

    # Spike lines for crosshair
    fig.update_xaxes(spikemode="across", spikethickness=1, spikedash="dot",
                     spikecolor="rgba(255,255,255,0.2)", row=1, col=1)

    # Display
    st.plotly_chart(fig, use_container_width=True)




#RSI CHART
def plot_rsi_chart(data, buy, sell):
    fig, ax = plt.subplots(figsize=(14,1))

    ax.plot(data['RSI'])
    ax.scatter(buy.index, data.loc[buy.index, "RSI"])
    ax.scatter(sell.index, data.loc[sell.index, "RSI"])

    st.pyplot(fig)


#MACD CHART
def plot_macd_chart(data):
    fig, ax = plt.subplots(figsize=(14,1))

    ax.plot(data['MACD'])
    ax.plot(data['MACD_Signal'])

    st.pyplot(fig)