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
    target_from_atr = entry + (2 * atr)  # 2x ATR for target
    target = min(resistance * 1.01, target_from_atr)  # Slightly above resistance or ATR-based
    if target <= entry:
        target = entry + (2 * atr)  # Fallback
    
    # Stop Loss = Tight ATR-based (not support which is too far)
    stoploss = entry - (1 * atr)  # 1x ATR below entry for tighter stop
    if stoploss < support:
        stoploss = support * 1.005  # Slightly below support if it's close
    
    # Recalculate risk-reward
    risk = entry - stoploss
    reward = target - entry
    
    # Ensure minimum 1:1.5 risk-reward
    if reward / risk < 1.5 and risk > 0:
        # Adjust target to achieve at least 1:1.5
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
    """
    Run smart screener - reads from DB if fresh, downloads if old.
    Returns: sorted results list
    """
    results = []
    
    init_database()
    
    stocks_list = list(stocks_dict.values())
    total_stocks = len(stocks_list)
    
    # ==========================================
    # CHECK IF DATABASE NEEDS UPDATE
    # ==========================================
    if should_update():
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.markdown("🐂 TORO AI scanning the market universe...")
        
        # ⚡ Batch download all stocks
        try:
            all_data = yf.download(stocks_list, period="3mo", interval="1d", progress=False)
            batch_success = True
        except:
            all_data = None
            batch_success = False
        
        # Store results for database
        db_results = {}
        
        for i, s in enumerate(stocks_list):
            progress_ratio = (i + 1) / total_stocks
            progress_percent = int(progress_ratio * 100)
            progress_bar.progress(progress_ratio)
            status_text.markdown(f"📡 Downloading & Analyzing: {progress_percent}%")
            
            try:
                # Get data from batch or fallback
                if batch_success and s in all_data['Close'].columns:
                    data = all_data.xs(s, axis=1, level=1).copy()
                else:
                    data = yf.download(s, period="3mo", interval="1d", progress=False)
                
                if data.empty or len(data) < 50:
                    continue
                
                # --- Calculate ALL indicators (same as before) ---
                # RSI
                delta = data['Close'].diff()
                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)
                avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
                avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
                rs = avg_gain / avg_loss
                data['RSI'] = 100 - (100 / (1 + rs))
                
                # MACD
                data['EMA_12'] = data['Close'].ewm(span=12).mean()
                data['EMA_26'] = data['Close'].ewm(span=26).mean()
                data['MACD'] = data['EMA_12'] - data['EMA_26']
                data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
                data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']
                
                # EMA
                data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
                data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
                
                # Bollinger Bands
                data['BB_Middle'] = data['Close'].rolling(20).mean()
                std = data['Close'].rolling(20).std()
                data['BB_Upper'] = data['BB_Middle'] + (2 * std)
                data['BB_Lower'] = data['BB_Middle'] - (2 * std)
                
                # ADX
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
                
                # Volume
                data['Volume_MA20'] = data['Volume'].rolling(20).mean()
                data['Volume_Ratio'] = data['Volume'] / data['Volume_MA20']
                
                # Price Change
                data['Returns_5D'] = data['Close'].pct_change(5) * 100
                
                # Support/Resistance
                resistance = float(data['High'].rolling(20).max().iloc[-1])
                support = float(data['Low'].rolling(20).min().iloc[-1])
                atr_final = float(atr_val.iloc[-1])
                
                latest = data.iloc[-1]
                
                # ✅ SAVE to database
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
        
        # Save all to database
        progress_bar.progress(1.0)
        status_text.markdown("💾 Saving to database...")
        save_to_database(db_results)
        
        progress_bar.empty()
        status_text.empty()
    
    # ==========================================
    # ⚡ LOAD FROM DATABASE (INSTANT!)
    # ==========================================
    status_text = st.empty()
    status_text.markdown("⚡ Loading from database...")
    
    df = load_from_database()
    
    if df.empty:
        status_text.empty()
        st.error("No data in database. Please run again.")
        return []
    
    # Score each stock from database
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
                label = "🔥🔥 Strong Buy"
                color = "#00e676"
            elif score >= 7:
                label = "🔥 Buy"
                color = "#00c853"
            elif score >= 4:
                label = "📈 Watch (Bullish)"
                color = "#69f0ae"
            elif score <= -10:
                label = "❄️❄️ Strong Sell"
                color = "#ff1744"
            elif score <= -7:
                label = "❄️ Sell"
                color = "#d50000"
            elif score <= -4:
                label = "📉 Watch (Bearish)"
                color = "#ff5252"
            else:
                label = "➖ Neutral"
                color = "#94a3b8"
            
            results.append({
                'symbol': row['symbol'],
                'score': score,
                'label': label,
                'color': color,
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

    # 🤖 Run AI on top 5 stocks even from cache
    for r in results[:5]:
        try:
            from ai_screener import ai_enhanced_screener
            stock_symbol = r['symbol']
            stock_name = stock_symbol.replace(".NS", "").replace(".BO", "")
            
            # Quick fetch for AI analysis only
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
    
    # Re-sort after AI adjustment
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return results



#---DISPLAY SCREENER--
def display_screener_results(results):
    """Display screener results in Streamlit"""
    if not results:
        st.warning("⚠️ No stocks found.")
        return
    
    # Best opportunity
    best = results[0]
    
    # Calculate levels for the best stock
    try:
        data = yf.download(best['symbol'], period="3mo", interval="1d", progress=False)
        if not data.empty:
            data.columns = data.columns.get_level_values(0)
            levels = calculate_levels(data)
        else:
            levels = None
    except:
        levels = None
    
        st.markdown("<div style='margin-bottom:-10px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🏆 Best Opportunity")
    
    if levels:
        # Calculate risk-reward ratio
        risk = levels['entry'] - levels['stoploss']
        reward = levels['target'] - levels['entry']
        rr_ratio = reward / risk if risk > 0 else 0
        
        components.html(
    f"""
    <div style="
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border: 2px solid {best['color']};
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        font-family: Arial;
    ">

        <div style="
            font-size: 22px;
            font-weight: 700;
            color: {best['color']};
            margin-bottom: 4px;
        ">
            {best['symbol']} → {best['label']}
        </div>

        <div style="
            font-size: 12px;
            color: #64748b;
            margin-bottom: 10px;
        ">
            Score: {best['score']:.0f} |
            RSI: {best['rsi']:.0f} |
            ADX: {best['adx']:.0f}
        </div>

        <div style="
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 10px;
        ">
            <div style="background:#ecfdf5;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:9px;color:#64748b;">🎯 ENTRY</div>
                <div style="font-size:15px;font-weight:700;color:#16a34a;">
                    ₹{levels['entry']:.2f}
                </div>
            </div>

            <div style="background:#ecfdf5;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:9px;color:#64748b;">🏁 TARGET</div>
                <div style="font-size:15px;font-weight:700;color:#16a34a;">
                    ₹{levels['target']:.2f}
                </div>
            </div>

            <div style="background:#fef2f2;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:9px;color:#64748b;">🛑 STOP LOSS</div>
                <div style="font-size:15px;font-weight:700;color:#dc2626;">
                    ₹{levels['stoploss']:.2f}
                </div>
            </div>
        </div>

        <div style="
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 10px;
        ">
            <div style="background:#f8fafc;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:8px;color:#94a3b8;">📈 RESISTANCE</div>
                <div style="font-size:12px;font-weight:600;">
                    ₹{levels['resistance']:.2f}
                </div>
            </div>

            <div style="background:#f8fafc;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:8px;color:#94a3b8;">📉 SUPPORT</div>
                <div style="font-size:12px;font-weight:600;">
                    ₹{levels['support']:.2f}
                </div>
            </div>

            <div style="background:#f8fafc;padding:8px;border-radius:8px;text-align:center;">
                <div style="font-size:8px;color:#94a3b8;">⚖️ R:R RATIO</div>
                <div style="font-size:12px;font-weight:600;">
                    1:{rr_ratio:.1f}
                </div>
            </div>
        </div>

        <div style="
            background:#eef2ff;
            padding:10px;
            border-radius:8px;
            border-left:3px solid #6366f1;
        ">
            <div style="
                font-size:10px;
                color:#6366f1;
                font-weight:600;
                margin-bottom:3px;
            ">
                🤖 AI ANALYSIS
            </div>

            <div style="
                font-size:11px;
                color:#334155;
                line-height:1.4;
            ">
                {best.get('ai_reason', 'Analysis not available')}
            </div>
        </div>

    </div>
    """,
    height=280,
    scrolling=False
)

    else:
        # Fallback if levels calculation fails
        st.markdown(
            f"""
            <div style="
                background: #f8fafc;
                border: 2px solid {best['color']};
                border-radius: 14px;
                padding: 20px;
                margin-bottom: 16px;
            ">
                <div style="font-size: 24px; font-weight: 700; color: {best['color']}; margin-bottom: 8px;">
                    {best['symbol']} → {best['label']}
                </div>
                <div style="font-size: 14px; color: #64748b;">
                    Score: {best['score']:.0f} | RSI: {best['rsi']:.0f} | ADX: {best['adx']:.0f} | Close: ₹{best['close']:.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Top 10 table
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:-10px; margin-bottom:4px;'>📊 Top Results</h4>", unsafe_allow_html=True)
    
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
    
    # Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🟢 Buy", sum(1 for r in results if r['score'] >= 4))
    with col2:
        st.metric("🔴 Sell", sum(1 for r in results if r['score'] <= -4))
    with col3:
        st.metric("🟡 Neutral", sum(1 for r in results if -3 <= r['score'] <= 3))
    with col4:
        st.metric("📊 Avg Score", f"{sum(r['score'] for r in results)/len(results):.1f}")