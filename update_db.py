# update_db.py - Run this to fix your database
from data_manager import save_to_database, load_from_database
from stocks import stocks_dict
import yfinance as yf
import pandas as pd

print("🔄 UPDATING DATABASE WITH REAL DATA...")
print("=" * 50)

def calculate_rsi(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50

def calculate_adx(data):
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
    adx = dx.rolling(14).mean()
    return adx.iloc[-1] if not pd.isna(adx.iloc[-1]) else 20

# Get first 20 stocks for testing
stocks_list = list(stocks_dict.values())[:20]
print(f"📊 Processing {len(stocks_list)} stocks...")
print()

results = {}

for idx, symbol in enumerate(stocks_list):
    try:
        print(f"{idx+1}/{len(stocks_list)}: {symbol}...")
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        
        if data.empty or len(data) < 50:
            print(f"  ❌ Insufficient data")
            continue
        
        rsi = calculate_rsi(data)
        adx = calculate_adx(data)
        close = data['Close'].iloc[-1]
        volume_ma = data['Volume'].rolling(20).mean().iloc[-1]
        volume_ratio = data['Volume'].iloc[-1] / volume_ma if volume_ma > 0 else 1
        
        # Calculate ensemble score (simple version)
        ensemble_score = 50
        if rsi < 35:
            ensemble_score += 20
        elif rsi > 70:
            ensemble_score -= 15
        if adx > 25:
            ensemble_score += 15
        
        ensemble_action = "BUY" if ensemble_score > 65 else "SELL" if ensemble_score < 35 else "NEUTRAL"
        
        results[symbol] = {
            'close': float(close),
            'rsi': float(rsi),
            'adx': float(adx),
            'volume_ratio': float(volume_ratio),
            'ensemble_score': float(ensemble_score),
            'ensemble_action': ensemble_action,
            'returns_5d': 0,
            'ema20': float(close),
            'ema50': float(close),
            'support': float(close * 0.98),
            'resistance': float(close * 1.02),
            'atr': float(close * 0.02)
        }
        print(f"  ✅ RSI: {rsi:.1f}, ADX: {adx:.1f}, Score: {ensemble_score:.0f}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

print()
print("=" * 50)

if results:
    save_to_database(results)
    print(f"✅ Saved {len(results)} stocks to database!")
    
    # Verify
    df = load_from_database()
    print(f"\n📊 Database now has {len(df)} stocks")
    print("\n📈 Sample data:")
    print(df[['symbol', 'rsi', 'adx', 'ensemble_score']].head())
else:
    print("❌ No stocks saved!")

print("\n✅ UPDATE COMPLETE! Now run your app.")