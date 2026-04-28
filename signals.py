import pandas as pd


def calculate_signal_score(data):
    """
    Returns raw score using all 7 indicators
    Positive = Bullish, Negative = Bearish
    """
    if len(data) < 50:
        return 0
    
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    score = 0
    
    # 1. RSI (Relaxed thresholds)
    rsi = latest.get('RSI', 50)
    if rsi < 35:
        score += 3
    elif rsi < 45:
        score += 2
    elif rsi < 50:
        score += 1
    elif rsi > 65:
        score -= 3
    elif rsi > 55:
        score -= 2
    elif rsi > 50:
        score -= 1
    
    # 2. MACD
    if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
        macd = latest['MACD']
        signal_line = latest['MACD_Signal']
        prev_macd = prev['MACD']
        prev_signal = prev['MACD_Signal']
        
        if macd > signal_line:
            score += 2
            if prev_macd <= prev_signal:
                score += 1
        else:
            score -= 2
            if prev_macd >= prev_signal:
                score -= 1
    
    # 3. EMA Crossover
    ema20 = latest.get('EMA20', latest['Close'])
    ema50 = latest.get('EMA50', latest['Close'])
    prev_ema20 = prev.get('EMA20', prev['Close'])
    prev_ema50 = prev.get('EMA50', prev['Close'])
    
    if ema20 > ema50:
        score += 2
        if prev_ema20 <= prev_ema50:
            score += 1
    else:
        score -= 2
    
    # 4. Price vs EMA20
    close = latest['Close']
    if close > ema20:
        score += 1
        if close > ema20 * 1.02:
            score += 1
    else:
        score -= 1
        if close < ema20 * 0.98:
            score -= 1
    
    # 5. Bollinger Bands
    if 'BB_Lower' in data.columns and 'BB_Upper' in data.columns:
        bb_lower = latest['BB_Lower']
        bb_upper = latest['BB_Upper']
        
        if close <= bb_lower * 1.01:
            score += 3
        elif close >= bb_upper * 0.99:
            score -= 3
    
    # 6. ADX
    adx = latest.get('ADX', 20)
    if adx > 25:
        if score > 0:
            score += 2
        elif score < 0:
            score -= 2
    elif adx > 20:
        if score > 0:
            score += 1
        elif score < 0:
            score -= 1
    
    # 7. Volume Confirmation
    if 'Volume' in data.columns:
        avg_vol = data['Volume'].rolling(20).mean().iloc[-1]
        current_vol = latest['Volume']
        if pd.notna(avg_vol) and avg_vol > 0:
            vol_ratio = current_vol / avg_vol
            if vol_ratio > 1.5:
                if score > 0:
                    score += 2
                elif score < 0:
                    score -= 2
            elif vol_ratio > 1.2:
                if score > 0:
                    score += 1
                elif score < 0:
                    score -= 1
    
    return score


def getsignal(data):
    """Uses enhanced scoring but returns simple -1, 0, 1"""
    score = calculate_signal_score(data)
    
    if score >= 3:
        return 1
    elif score <= -3:
        return -1
    else:
        return 0