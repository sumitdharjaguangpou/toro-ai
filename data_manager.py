# data_manager.py
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import streamlit as st

DB_PATH = "stock_data.db"

# ==========================================
# DATABASE SETUP
# ==========================================
def init_database():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_indicators (
            symbol TEXT PRIMARY KEY,
            close REAL,
            rsi REAL,
            macd REAL,
            macd_signal REAL,
            macd_hist REAL,
            ema20 REAL,
            ema50 REAL,
            adx REAL,
            bb_upper REAL,
            bb_lower REAL,
            bb_middle REAL,
            volume_ratio REAL,
            returns_5d REAL,
            technical_score REAL,
            ai_signal TEXT,
            ai_confidence REAL,
            ai_reason TEXT,
            support REAL,
            resistance REAL,
            atr REAL,
            last_updated TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_prices (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            PRIMARY KEY (symbol, date)
        )
    ''')
    
    conn.commit()
    conn.close()

# ==========================================
# INDICATOR CALCULATION (Single Stock)
# ==========================================
def calculate_indicators(data):
    """Calculate all indicators for a single stock"""
    if len(data) < 50:
        return None
    
    # RSI
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
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
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    data['ADX'] = dx.rolling(14).mean()
    
    # Volume
    data['Volume_MA20'] = data['Volume'].rolling(20).mean()
    data['Volume_Ratio'] = data['Volume'] / data['Volume_MA20']
    
    # Returns
    data['Returns_5D'] = data['Close'].pct_change(5) * 100
    
    # Support/Resistance
    data['Resistance'] = data['High'].rolling(20).max()
    data['Support'] = data['Low'].rolling(20).min()
    data['ATR'] = tr.rolling(14).mean()
    
    latest = data.iloc[-1]
    return {
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
        'support': float(latest['Support']),
        'resistance': float(latest['Resistance']),
        'atr': float(latest['ATR'])
    }

# ==========================================
# BATCH UPDATE (Background)
# ==========================================
def update_all_stocks(stocks_list, batch_size=50):
    """Download and store all stocks in batches"""
    total = len(stocks_list)
    results = {}
    
    for start in range(0, total, batch_size):
        batch = stocks_list[start:start + batch_size]
        
        try:
            # Batch download
            all_data = yf.download(batch, period="3mo", interval="1d", progress=False)
            
            for symbol in batch:
                try:
                    if symbol in all_data['Close'].columns:
                        data = all_data.xs(symbol, axis=1, level=1).copy()
                    else:
                        data = yf.download(symbol, period="3mo", interval="1d", progress=False)
                    
                    if data.empty or len(data) < 50:
                        continue
                    
                    indicators = calculate_indicators(data)
                    if indicators:
                        results[symbol] = indicators
                        
                except:
                    continue
                    
        except Exception as e:
            continue
    
    return results

# ==========================================
# DATABASE OPERATIONS
# ==========================================
def save_to_database(results):
    """Save indicators to SQLite"""
    conn = sqlite3.connect(DB_PATH)
    
    for symbol, ind in results.items():
        conn.execute('''
            INSERT OR REPLACE INTO stock_indicators 
            (symbol, close, rsi, macd, macd_signal, macd_hist, ema20, ema50, 
             adx, bb_upper, bb_lower, bb_middle, volume_ratio, returns_5d,
             support, resistance, atr, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            symbol, ind['close'], ind['rsi'], ind['macd'], ind['macd_signal'],
            ind['macd_hist'], ind['ema20'], ind['ema50'], ind['adx'],
            ind['bb_upper'], ind['bb_lower'], ind['bb_middle'],
            ind['volume_ratio'], ind['returns_5d'], ind['support'],
            ind['resistance'], ind['atr'], datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()

def load_from_database():
    """Load all indicators from database - INSTANT"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM stock_indicators", conn)
    conn.close()
    return df

def should_update():
    """Check if data is older than 15 minutes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(last_updated) FROM stock_indicators")
    result = cursor.fetchone()[0]
    conn.close()
    
    if result is None:
        return True
    
    last_update = datetime.fromisoformat(result)
    return datetime.now() - last_update > timedelta(minutes=15)