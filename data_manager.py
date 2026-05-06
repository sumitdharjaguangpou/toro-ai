# data_manager.py - COMPLETE VERSION

import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

DB_PATH = "stock_data.db"

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_indicators (
            symbol TEXT PRIMARY KEY,
            close REAL,
            rsi REAL,
            volume_ratio REAL,
            ensemble_score REAL,
            ensemble_action TEXT,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()

def calculate_proper_score(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="3mo", interval="1d")
        
        if data.empty or len(data) < 20:
            return None
        
        close_price = float(data['Close'].iloc[-1])
        
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_val = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else 50
        
        # Calculate returns
        if len(data) >= 6:
            returns_5d = (data['Close'].iloc[-1] / data['Close'].iloc[-6] - 1) * 100
        else:
            returns_5d = 0
        
        # Volume ratio
        volume_ma = data['Volume'].rolling(20).mean().iloc[-1]
        volume_ratio = float(data['Volume'].iloc[-1] / volume_ma) if volume_ma and volume_ma > 0 else 1
        
        # Scoring
        score = 50
        
        if rsi_val < 30:
            score += 25
        elif rsi_val < 40:
            score += 15
        elif rsi_val > 75:
            score -= 25
        elif rsi_val > 70:
            score -= 15
        
        if returns_5d > 10:
            score += 20
        elif returns_5d > 5:
            score += 12
        elif returns_5d < -10:
            score -= 20
        elif returns_5d < -5:
            score -= 12
        
        if volume_ratio > 2.0:
            score += 15
        elif volume_ratio > 1.5:
            score += 10
        
        score = max(0, min(100, score))
        
        if score >= 80:
            action = "STRONG BUY"
        elif score >= 70:
            action = "BUY"
        elif score >= 60:
            action = "WATCH"
        elif score >= 40:
            action = "NEUTRAL"
        else:
            action = "AVOID"
        
        return {
            'close': round(close_price, 2),
            'rsi': round(rsi_val, 1),
            'volume_ratio': round(volume_ratio, 2),
            'ensemble_score': score,
            'ensemble_action': action
        }
    except:
        return None

def update_all_stocks(stocks_list, max_workers=3, progress_callback=None):
    results = {}
    total = len(stocks_list)
    completed = 0
    
    for idx, symbol in enumerate(stocks_list):
        indicators = calculate_proper_score(symbol)
        if indicators:
            results[symbol] = indicators
        completed += 1
        if progress_callback:
            progress_callback(completed, total)
    
    return results

def save_to_database(results):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    for symbol, ind in results.items():
        cursor.execute('''
            INSERT OR REPLACE INTO stock_indicators 
            (symbol, close, rsi, volume_ratio, ensemble_score, ensemble_action, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (symbol, ind['close'], ind['rsi'], ind['volume_ratio'], 
              ind['ensemble_score'], ind['ensemble_action'], now))
    
    conn.commit()
    conn.close()

def load_from_database():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM stock_indicators", conn)
    conn.close()
    return df

def get_database_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM stock_indicators")
    total_stocks = cursor.fetchone()[0]
    cursor.execute("SELECT MAX(last_updated) FROM stock_indicators")
    last_updated = cursor.fetchone()[0]
    conn.close()
    return {'total_stocks': total_stocks, 'last_updated': last_updated}

def clear_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock_indicators")
    conn.commit()
    conn.close()

def should_update():
    """Check if data needs update (every 6 hours)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(last_updated) FROM stock_indicators")
    result = cursor.fetchone()[0]
    conn.close()
    
    if result is None:
        return True
    
    last_update = datetime.fromisoformat(result)
    return datetime.now() - last_update > timedelta(hours=6)
