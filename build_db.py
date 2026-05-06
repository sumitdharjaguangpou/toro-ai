# build_db.py - FIXED VERSION

import sqlite3
import yfinance as yf
import time
from datetime import datetime

DB_PATH = "stock_data.db"

# List of good Indian stocks (removed duplicates)
STOCKS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'AXISBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS',
    'HCLTECH.NS', 'WIPRO.NS', 'SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS',
    'MARUTI.NS', 'TATAMOTORS.NS', 'TITAN.NS', 'ASIANPAINT.NS', 'NESTLE.NS',
    'POWERGRID.NS', 'NTPC.NS', 'ONGC.NS', 'COALINDIA.NS', 'BAJFINANCE.NS',
    'HDFC.NS', 'BAJAJFINSV.NS', 'TECHM.NS', 'ULTRACEMCO.NS', 'ADANIPORTS.NS',
    'JSWSTEEL.NS', 'GRASIM.NS', 'DIVISLAB.NS', 'BRITANNIA.NS', 'APOLLOHOSP.NS',
    'HEROMOTOCO.NS', 'EICHERMOT.NS', 'BAJAJ-AUTO.NS', 'SHREECEM.NS', 'UPL.NS'
]


print("=" * 50)
print("BUILDING DATABASE")
print("=" * 50)

# Clear and recreate database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS stock_indicators')
cursor.execute('''
    CREATE TABLE stock_indicators (
        symbol TEXT PRIMARY KEY,
        close REAL,
        rsi REAL,
        adx REAL,
        volume_ratio REAL,
        ensemble_score REAL,
        ensemble_action TEXT,
        last_updated TEXT
    )
''')
conn.commit()
print("✅ Database created")

results = []

for symbol in STOCKS:
    try:
        print(f"Processing {symbol}...", end=" ")
        
        # Download data
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="3mo", interval="1d")
        
        if data.empty or len(data) < 20:
            print("❌ No data")
            continue
        
        # Get current price
        price = data['Close'].iloc[-1]
        
        # Simple RSI calculation
        closes = data['Close'].values
        gains = []
        losses = []
        
        for i in range(1, len(closes)):
            diff = closes[i] - closes[i-1]
            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))
        
        if len(gains) >= 14:
            avg_gain = sum(gains[-14:]) / 14
            avg_loss = sum(losses[-14:]) / 14
            if avg_loss > 0:
                rsi = 100 - (100 / (1 + avg_gain / avg_loss))
            else:
                rsi = 70
        else:
            rsi = 50
        
        # Score based on RSI
        if rsi < 35:
            score = 85
            action = "STRONG BUY"
        elif rsi < 45:
            score = 70
            action = "BUY"
        elif rsi > 75:
            score = 30
            action = "SELL"
        elif rsi > 65:
            score = 45
            action = "NEUTRAL"
        else:
            score = 55
            action = "WATCH"
        
        # Save to database
        cursor.execute('''
            INSERT OR REPLACE INTO stock_indicators 
            (symbol, close, rsi, adx, volume_ratio, ensemble_score, ensemble_action, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (symbol, float(price), round(rsi, 1), 25, 1.0, score, action, datetime.now().isoformat()))
        
        results.append(symbol)
        print(f"✅ Price: {price:.2f}, RSI: {rsi:.1f}, Score: {score}, {action}")
        
        time.sleep(0.2)
        
    except Exception as e:
        print(f"❌ Error: {e}")

conn.commit()
conn.close()

print(f"\n✅ Saved {len(results)} stocks to database")
print("\nStocks in database:")
for r in results:
    print(f"  - {r}")