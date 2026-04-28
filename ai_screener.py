# ai_screener.py
from groq import Groq
import streamlit as st
import time

# Configure Groq
GROQ_API_KEY = "GROQ_API_KEY"#api key here
client = Groq(api_key=GROQ_API_KEY)

def ai_analyze_stock(stock_name, technical_data):
    """
    Sends technical data to Groq AI (Llama 3.1) for analysis.
    Returns: BUY, SELL, or HOLD with reasoning.
    """
    prompt = f"""
    You are a professional stock analyst. Analyze this stock:

    📊 Stock: {stock_name}
    📈 RSI: {technical_data.get('RSI', 'N/A')}
    📉 MACD: {technical_data.get('MACD', 'N/A')} vs Signal: {technical_data.get('MACD_Signal', 'N/A')}
    📊 ADX: {technical_data.get('ADX', 'N/A')}
    📏 Bollinger Position: {technical_data.get('BB_Position', 'N/A')}
    📈 EMA20 vs EMA50: {technical_data.get('EMA_Trend', 'N/A')}
    📦 Volume Ratio: {technical_data.get('Volume_Ratio', 'N/A')}x average

    Based on these technical indicators, give:
    1. BUY, SELL, or HOLD
    2. Confidence (1-10)
    3. One-line reasoning

    Return in this exact format:
    SIGNAL: [BUY/SELL/HOLD]
    CONFIDENCE: [1-10]
    REASON: [one line]
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast & free on Groq
            messages=[
                {"role": "system", "content": "You are a professional stock analyst. Always respond in the exact format requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low = more consistent
            max_tokens=100,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"SIGNAL: HOLD\nCONFIDENCE: 5\nREASON: AI unavailable ({str(e)[:50]})"

def parse_ai_response(response_text):
    """Parse AI response into structured data."""
    signal = "HOLD"
    confidence = 5
    reason = "No analysis available"
    
    for line in response_text.split('\n'):
        if line.startswith("SIGNAL:"):
            signal = line.replace("SIGNAL:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                confidence = int(line.replace("CONFIDENCE:", "").strip())
            except:
                pass
        elif line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()
    
    return signal, confidence, reason

def ai_enhanced_screener(stock_symbol, stock_name, data):
    """
    Combines technical scoring with Groq AI analysis.
    Returns: ai_score, ai_signal, ai_confidence, ai_reason
    """
    # Get technical data
    latest = data.iloc[-1]
    
    technical_data = {
        'RSI': f"{latest.get('RSI', 50):.1f}",
        'MACD': f"{latest.get('MACD', 0):.3f}",
        'MACD_Signal': f"{latest.get('MACD_Signal', 0):.3f}",
        'ADX': f"{latest.get('ADX', 20):.1f}",
        'BB_Position': 'Middle',
        'EMA_Trend': 'Neutral',
        'Volume_Ratio': f"{latest.get('Volume', 0) / data['Volume'].rolling(20).mean().iloc[-1]:.1f}" if len(data) >= 20 else "1.0"
    }
    
    # Bollinger position
    if 'BB_Lower' in latest and 'BB_Upper' in latest:
        bb_lower = float(latest['BB_Lower'])
        bb_upper = float(latest['BB_Upper'])
        close = float(latest['Close'])
        if close <= bb_lower * 1.02:
            technical_data['BB_Position'] = 'Near Lower (Support)'
        elif close >= bb_upper * 0.98:
            technical_data['BB_Position'] = 'Near Upper (Resistance)'
    
    # EMA trend
    ema20 = latest.get('EMA20', 0)
    ema50 = latest.get('EMA50', 0)
    if ema20 > ema50:
        technical_data['EMA_Trend'] = 'Bullish (EMA20 > EMA50)'
    else:
        technical_data['EMA_Trend'] = 'Bearish (EMA20 < EMA50)'
    
    # Add a small delay to respect rate limits
    time.sleep(0.5)
    
    # Get AI analysis
    ai_response = ai_analyze_stock(stock_name, technical_data)
    ai_signal, ai_confidence, ai_reason = parse_ai_response(ai_response)
    
    # Convert AI signal to score
    ai_score = 0
    if ai_signal == "BUY":
        ai_score = ai_confidence / 2  # Max +5 points
    elif ai_signal == "SELL":
        ai_score = -ai_confidence / 2  # Max -5 points
    
    return ai_score, ai_signal, ai_confidence, ai_reason