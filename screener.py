# screener.py
import yfinance as yf
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from data_manager import init_database, should_update, update_all_stocks, save_to_database, load_from_database  

def calculate_levels(data):
    """Calculate entry, exit, target, stoploss, support, resistance"""
    latest = data.iloc[-1]
    close = float(latest['Close'])
    
    # Support & Resistance (20-period high/low)
    resistance = float(data['High'].rolling(20).max().iloc[-1])
    support = float(data['Low'].rolling(20).min().iloc[-1])
    
    # ATR for stoploss calculation
    high = data['High']
    low = data['Low']
    tr1 = high - low
    tr2 = (high - data['Close'].shift()).abs()
    tr3 = (low - data['Close'].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = float(tr.rolling(14).mean().iloc[-1])
    
    # Entry = Current price
    entry = close
    
    # Target = Based on resistance + ATR (minimum 2:1 reward:risk)
    target_from_atr = entry + (2 * atr)
    target = min(resistance * 1.01, target_from_atr)
    if target <= entry:
        target = entry + (2 * atr)
    
    # Stop Loss = Tight ATR-based
    stoploss = entry - (1 * atr)
    if stoploss < support:
        stoploss = support * 1.005
    
    # Recalculate risk-reward
    risk = entry - stoploss
    reward = target - entry
    
    # Ensure minimum 1:1.5 risk-reward
    if reward / risk < 1.5 and risk > 0:
        target = entry + (1.5 * risk)
    
    return {
        'entry': entry,
        'target': round(target, 2),
        'stoploss': round(stoploss, 2),
        'support': round(support, 2),
        'resistance': round(resistance, 2),
        'atr': round(atr, 2)
    }

#============================================
#---- RUN SCREENER (With Database Cache) ----
#============================================
def run_screener(stocks_dict):
    """Run smart screener - reads from DB if fresh, downloads if old."""
    results = []
    
    init_database()
    
    stocks_list = list(stocks_dict.values())
    total_stocks = len(stocks_list)
    
    if should_update():
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.markdown("🐂 **TORO AI scanning the market universe...**")
        
        try:
            all_data = yf.download(stocks_list, period="3mo", interval="1d", progress=False)
            batch_success = True
        except:
            all_data = None
            batch_success = False
        
        db_results = {}
        
        for i, s in enumerate(stocks_list):
            progress_ratio = (i + 1) / total_stocks
            progress_percent = int(progress_ratio * 100)
            progress_bar.progress(progress_ratio)
            status_text.markdown(f"📡 **Downloading & Analyzing:** `{progress_percent}%`")
            
            try:
                if batch_success and s in all_data['Close'].columns:
                    data = all_data.xs(s, axis=1, level=1).copy()
                else:
                    data = yf.download(s, period="3mo", interval="1d", progress=False)
                
                if data.empty or len(data) < 50:
                    continue
                
                # Calculate all indicators
                delta = data['Close'].diff()
                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)
                avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
                avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
                rs = avg_gain / avg_loss
                data['RSI'] = 100 - (100 / (1 + rs))
                
                data['EMA_12'] = data['Close'].ewm(span=12).mean()
                data['EMA_26'] = data['Close'].ewm(span=26).mean()
                data['MACD'] = data['EMA_12'] - data['EMA_26']
                data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
                data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']
                
                data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
                data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
                
                data['BB_Middle'] = data['Close'].rolling(20).mean()
                std = data['Close'].rolling(20).std()
                data['BB_Upper'] = data['BB_Middle'] + (2 * std)
                data['BB_Lower'] = data['BB_Middle'] - (2 * std)
                
                high = data['High']
                low = data['Low']
                close = data['Close']
                plus_dm = high.diff().where((high.diff() > low.diff()) & (high.diff() > 0), 0)
                minus_dm = low.diff().where((low.diff() > high.diff()) & (low.diff() > 0), 0)
                tr1 = high - low
                tr2 = (high - close.shift()).abs()
                tr3 = (low - close.shift()).abs()
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                atr_val = tr.rolling(14).mean()
                plus_di = 100 * (plus_dm.rolling(14).mean() / atr_val)
                minus_di = 100 * (minus_dm.rolling(14).mean() / atr_val)
                dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
                data['ADX'] = dx.rolling(14).mean()
                
                data['Volume_MA20'] = data['Volume'].rolling(20).mean()
                data['Volume_Ratio'] = data['Volume'] / data['Volume_MA20']
                data['Returns_5D'] = data['Close'].pct_change(5) * 100
                
                resistance = float(data['High'].rolling(20).max().iloc[-1])
                support = float(data['Low'].rolling(20).min().iloc[-1])
                atr_final = float(atr_val.iloc[-1])
                
                latest = data.iloc[-1]
                
                db_results[s] = {
                    'close': float(latest['Close']),
                    'rsi': float(latest['RSI']),
                    'macd': float(latest['MACD']),
                    'macd_signal': float(latest['MACD_Signal']),
                    'macd_hist': float(latest['MACD_Hist']),
                    'ema20': float(latest['EMA20']),
                    'ema50': float(latest['EMA50']),
                    'adx': float(latest['ADX']),
                    'bb_upper': float(latest['BB_Upper']),
                    'bb_lower': float(latest['BB_Lower']),
                    'bb_middle': float(latest['BB_Middle']),
                    'volume_ratio': float(latest['Volume_Ratio']),
                    'returns_5d': float(latest['Returns_5D']),
                    'support': support,
                    'resistance': resistance,
                    'atr': atr_final
                }
            except:
                continue
        
        progress_bar.progress(1.0)
        status_text.markdown("💾 **Saving to database...**")
        save_to_database(db_results)
        progress_bar.empty()
        status_text.empty()
    
    status_text = st.empty()
    status_text.markdown("⚡ **Loading from quantum database...**")
    
    df = load_from_database()
    
    if df.empty:
        status_text.empty()
        st.error("⚠️ No data in database. Please run again.")
        return []
    
    for _, row in df.iterrows():
        try:
            score = 0
            details = []
            
            rsi = row['rsi']
            if rsi < 30:
                score += 3
                details.append(f"RSI Oversold ({rsi:.0f})")
            elif rsi < 40:
                score += 2
            elif rsi < 50:
                score += 1
            elif rsi > 70:
                score -= 3
            elif rsi > 60:
                score -= 2
            
            macd = row['macd']
            macd_signal = row['macd_signal']
            macd_hist = row['macd_hist']
            
            if macd > macd_signal:
                score += 2
                if macd_hist > 0:
                    score += 1
            else:
                score -= 2
            
            ema20 = row['ema20']
            ema50 = row['ema50']
            close_price = row['close']
            
            if ema20 > ema50:
                score += 2
                if close_price > ema20:
                    score += 1
            else:
                score -= 2
            
            bb_lower = row['bb_lower']
            bb_upper = row['bb_upper']
            
            if close_price <= bb_lower * 1.02:
                score += 3
            elif close_price >= bb_upper * 0.98:
                score -= 3
            
            adx = row['adx']
            if adx > 30:
                if score > 0:
                    score += 2
                elif score < 0:
                    score -= 2
            elif adx > 25:
                if score > 0:
                    score += 1
                elif score < 0:
                    score -= 1
            
            vol_ratio = row['volume_ratio']
            if vol_ratio > 2.0:
                if score > 0:
                    score += 2
            elif vol_ratio > 1.5:
                if score > 0:
                    score += 1
            
            if score >= 10:
                label = "🔥🔥 STRONG BUY"
                color = "#00ff88"
                bg_gradient = "linear-gradient(135deg, rgba(0,255,136,0.15), rgba(0,255,136,0.05))"
            elif score >= 7:
                label = "🔥 BUY"
                color = "#00e676"
                bg_gradient = "linear-gradient(135deg, rgba(0,230,118,0.12), rgba(0,230,118,0.03))"
            elif score >= 4:
                label = "📈 WATCH (BULLISH)"
                color = "#69f0ae"
                bg_gradient = "linear-gradient(135deg, rgba(105,240,174,0.1), rgba(105,240,174,0.02))"
            elif score <= -10:
                label = "❄️❄️ STRONG SELL"
                color = "#ff1744"
                bg_gradient = "linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.05))"
            elif score <= -7:
                label = "❄️ SELL"
                color = "#d50000"
                bg_gradient = "linear-gradient(135deg, rgba(213,0,0,0.12), rgba(213,0,0,0.03))"
            elif score <= -4:
                label = "📉 WATCH (BEARISH)"
                color = "#ff5252"
                bg_gradient = "linear-gradient(135deg, rgba(255,82,82,0.1), rgba(255,82,82,0.02))"
            else:
                label = "➖ NEUTRAL"
                color = "#94a3b8"
                bg_gradient = "linear-gradient(135deg, rgba(148,163,184,0.08), rgba(148,163,184,0.02))"
            
            results.append({
                'symbol': row['symbol'],
                'score': score,
                'label': label,
                'color': color,
                'bg_gradient': bg_gradient,
                'rsi': rsi,
                'adx': adx,
                'close': close_price,
                'vol_ratio': vol_ratio,
                'returns_5d': row['returns_5d'],
                'details': details,
                'support': row['support'],
                'resistance': row['resistance'],
                'atr': row['atr'],
                'ai_signal': 'N/A',
                'ai_confidence': 0,
                'ai_reason': 'Run screener after data refresh for AI analysis'
            })
        except:
            continue
    
    status_text.empty()
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    # 🤖 Run AI on top 5 stocks
    for r in results[:5]:
        try:
            from ai_screener import ai_enhanced_screener
            stock_symbol = r['symbol']
            stock_name = stock_symbol.replace(".NS", "").replace(".BO", "")
            
            data = yf.download(stock_symbol, period="3mo", interval="1d", progress=False)
            if not data.empty:
                data.columns = data.columns.get_level_values(0)
                ai_score, ai_signal, ai_confidence, ai_reason = ai_enhanced_screener(
                    stock_symbol, stock_name, data
                )
                r['ai_signal'] = ai_signal
                r['ai_confidence'] = ai_confidence
                r['ai_reason'] = ai_reason
                r['score'] += ai_score
        except:
            pass
    
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return results

#---DISPLAY SCREENER (FUTURISTIC)--
def display_screener_results(results):
    """Display screener results in Streamlit with futuristic styling"""
    if not results:
        st.warning("⚠️ No stocks found.")
        return
    
    # Add futuristic CSS
    st.markdown("""
    <style>
    /* Futuristic screener styling */
    .screener-card {
        background: linear-gradient(135deg, rgba(10, 20, 40, 0.95), rgba(5, 10, 20, 0.98));
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .screener-card:hover {
        border-color: rgba(0, 255, 255, 0.8);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .neon-text {
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    .metric-box {
        background: rgba(0, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        border-color: rgba(255, 0, 255, 0.5);
        background: rgba(255, 0, 255, 0.05);
    }
    
    .ai-insight {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(255, 0, 255, 0.05));
        border-left: 3px solid #00ffff;
        border-radius: 10px;
        padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Best opportunity card
    best = results[0]
    
    try:
        data = yf.download(best['symbol'], period="3mo", interval="1d", progress=False)
        if not data.empty:
            data.columns = data.columns.get_level_values(0)
            levels = calculate_levels(data)
        else:
            levels = None
    except:
        levels = None
    
    st.markdown("### 🏆 **BEST OPPORTUNITY**")
    
    if levels:
        risk = levels['entry'] - levels['stoploss']
        reward = levels['target'] - levels['entry']
        rr_ratio = reward / risk if risk > 0 else 0
        
        components.html(
        f"""
        <div style="
            background: {best.get('bg_gradient', 'linear-gradient(135deg, rgba(0,255,255,0.05), rgba(255,0,255,0.05))')};
            border: 2px solid {best['color']};
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            font-family: 'Courier New', monospace;
        ">
            <div style="
                font-size: 24px;
                font-weight: 800;
                color: {best['color']};
                margin-bottom: 8px;
                text-shadow: 0 0 15px {best['color']};
                letter-spacing: 1px;
            ">
                🎯 {best['symbol']}
            </div>
            
            <div style="
                font-size: 18px;
                font-weight: 700;
                color: {best['color']};
                margin-bottom: 12px;
                letter-spacing: 2px;
            ">
                {best['label']}
            </div>

            <div style="
                font-size: 11px;
                color: #00ffff;
                margin-bottom: 15px;
                opacity: 0.8;
                letter-spacing: 1px;
            ">
                ⚡ SCORE: {best['score']:.0f} &nbsp;|&nbsp; 📊 RSI: {best['rsi']:.0f} &nbsp;|&nbsp; 📈 ADX: {best['adx']:.0f}
            </div>

            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 12px;
                margin-bottom: 15px;
            ">
                <div style="background:rgba(0,255,136,0.1);padding:10px;border-radius:12px;text-align:center;border:1px solid rgba(0,255,136,0.3);">
                    <div style="font-size:9px;color:#00ffff;letter-spacing:1px;">🎯 ENTRY</div>
                    <div style="font-size:18px;font-weight:800;color:#00ff88;">
                        ₹{levels['entry']:.2f}
                    </div>
                </div>

                <div style="background:rgba(0,255,255,0.1);padding:10px;border-radius:12px;text-align:center;border:1px solid rgba(0,255,255,0.3);">
                    <div style="font-size:9px;color:#00ffff;letter-spacing:1px;">🏁 TARGET</div>
                    <div style="font-size:18px;font-weight:800;color:#00ffff;">
                        ₹{levels['target']:.2f}
                    </div>
                </div>

                <div style="background:rgba(255,23,68,0.1);padding:10px;border-radius:12px;text-align:center;border:1px solid rgba(255,23,68,0.3);">
                    <div style="font-size:9px;color:#ff1744;letter-spacing:1px;">🛑 STOP LOSS</div>
                    <div style="font-size:18px;font-weight:800;color:#ff1744;">
                        ₹{levels['stoploss']:.2f}
                    </div>
                </div>
            </div>

            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 12px;
                margin-bottom: 15px;
            ">
                <div style="background:rgba(148,163,184,0.1);padding:8px;border-radius:10px;text-align:center;">
                    <div style="font-size:8px;color:#00ffff;">📈 RESISTANCE</div>
                    <div style="font-size:13px;font-weight:600;color:#94a3b8;">
                        ₹{levels['resistance']:.2f}
                    </div>
                </div>

                <div style="background:rgba(148,163,184,0.1);padding:8px;border-radius:10px;text-align:center;">
                    <div style="font-size:8px;color:#00ffff;">📉 SUPPORT</div>
                    <div style="font-size:13px;font-weight:600;color:#94a3b8;">
                        ₹{levels['support']:.2f}
                    </div>
                </div>

                <div style="background:rgba(255,215,0,0.1);padding:8px;border-radius:10px;text-align:center;">
                    <div style="font-size:8px;color:#ffd700;">⚖️ R:R RATIO</div>
                    <div style="font-size:13px;font-weight:600;color:#ffd700;">
                        1:{rr_ratio:.1f}
                    </div>
                </div>
            </div>

            <div style="
                background: linear-gradient(135deg, rgba(0,255,255,0.08), rgba(255,0,255,0.08));
                padding: 12px;
                border-radius: 12px;
                border-left: 3px solid #00ffff;
            ">
                <div style="
                    font-size: 10px;
                    color: #00ffff;
                    font-weight: 700;
                    margin-bottom: 6px;
                    letter-spacing: 2px;
                ">
                    🤖 AI QUANTUM ANALYSIS
                </div>
                <div style="
                    font-size: 12px;
                    color: #e2e8f0;
                    line-height: 1.5;
                ">
                    {best.get('ai_reason', 'Analysis not available')}
                </div>
            </div>
        </div>
        """,
        height=410,
        scrolling=False
        )
    else:
        st.markdown(f"""
        <div style="
            background: {best.get('bg_gradient', 'linear-gradient(135deg, rgba(0,255,255,0.05), rgba(255,0,255,0.05))')};
            border: 2px solid {best['color']};
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <div style="font-size: 24px; font-weight: 800; color: {best['color']}; margin-bottom: 8px;">
                🎯 {best['symbol']}
            </div>
            <div style="font-size: 16px; font-weight: 700; color: {best['color']}; margin-bottom: 8px;">
                {best['label']}
            </div>
            <div style="font-size: 12px; color: #00ffff;">
                Score: {best['score']:.0f} | RSI: {best['rsi']:.0f} | ADX: {best['adx']:.0f} | Price: ₹{best['close']:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Results Table with styling
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 **QUANTUM SCREENING RESULTS**")
    
    table_data = []
    for r in results[:10]:
        table_data.append({
            'Stock': r['symbol'],
            'Signal': r['label'],
            'Score': r['score'],
            'RSI': f"{r['rsi']:.0f}",
            'ADX': f"{r['adx']:.0f}",
            'Price': f"₹{r['close']:.2f}",
            'Volume': f"{r['vol_ratio']:.1f}x",
            'AI': f"{r.get('ai_signal', 'N/A')} ({r.get('ai_confidence', 0)}/10)"
        })
    
    df_results = pd.DataFrame(table_data)
    st.dataframe(df_results, use_container_width=True, hide_index=True)
    
    # Summary Metrics with futuristic styling
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📈 **MARKET SUMMARY**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 11px; color: #00ff88; letter-spacing: 1px;">🟢 STRONG BUY</div>
            <div style="font-size: 28px; font-weight: 800; color: #00ff88;">{sum(1 for r in results if r['score'] >= 7)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 11px; color: #ff1744; letter-spacing: 1px;">🔴 STRONG SELL</div>
            <div style="font-size: 28px; font-weight: 800; color: #ff1744;">{sum(1 for r in results if r['score'] <= -7)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 11px; color: #69f0ae; letter-spacing: 1px;">🟡 WATCH LIST</div>
            <div style="font-size: 28px; font-weight: 800; color: #69f0ae;">{sum(1 for r in results if 4 <= r['score'] <= 6)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_score = sum(r['score'] for r in results)/len(results)
        arrow = "📈" if avg_score > 0 else "📉"
        color = "#00ff88" if avg_score > 0 else "#ff1744"
        st.markdown(f"""
        <div class="metric-box">
            <div style="font-size: 11px; color: #00ffff; letter-spacing: 1px;">⚡ AVG SCORE</div>
            <div style="font-size: 28px; font-weight: 800; color: {color};">{arrow} {avg_score:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
