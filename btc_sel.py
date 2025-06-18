import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

# === CONFIGURABLE PARAMETERS ===
SMA_SHORT = 50
SMA_LONG = 200
RSI_PERIOD = 14
RSI_UPPER = 60
RSI_LOWER = 40
MACD_FAST = 8
MACD_SLOW = 21
MACD_SIGNAL = 5
BB_PERIOD = 20
BB_STD = 2
TP_MULTIPLIER = 1.2
CAPITAL = 10000
RISK_PCT = 0.005
BACKTEST_LOOKBACK = 20
# ==============================

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
BINANCE_BASE_URL = 'https://api.binance.com'

# Fetch candlesticks into DataFrame
def get_candles_df(symbol, interval, limit=300):
    r = requests.get(
        f'{BINANCE_BASE_URL}/api/v3/klines',
        params={'symbol': symbol, 'interval': interval, 'limit': limit}
    )
    df = pd.DataFrame(
        r.json(),
        columns=['time','open','high','low','close','volume','ct','qav','n','tbav','tqav','ignore']
    )
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
    df.set_index('time', inplace=True)
    return df

# Compute technical indicators
def compute_indicators(df):
    df['sma_short'] = df['close'].rolling(SMA_SHORT).mean()
    df['sma_long'] = df['close'].rolling(SMA_LONG).mean()
    # RSI
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    df['rsi'] = 100 - (100 / (1 + (up.ewm(span=RSI_PERIOD).mean() / down.ewm(span=RSI_PERIOD).mean())))
    # MACD
    ema_fast = df['close'].ewm(span=MACD_FAST).mean()
    ema_slow = df['close'].ewm(span=MACD_SLOW).mean()
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = df['macd'].ewm(span=MACD_SIGNAL).mean()
    # Bollinger Bands
    df['bb_mid'] = df['close'].rolling(BB_PERIOD).mean()
    df['bb_std'] = df['close'].rolling(BB_PERIOD).std()
    df['bb_upper'] = df['bb_mid'] + BB_STD * df['bb_std']
    df['bb_lower'] = df['bb_mid'] - BB_STD * df['bb_std']
    return df

# Generate detailed signal for a single timeframe
def detailed_signal(df):
    s = df.iloc[-1]
    # Trend
    trend = 'Bullish' if s['sma_short'] > s['sma_long'] else 'Bearish' if s['sma_short'] < s['sma_long'] else 'Sideways'
    # RSI state
    rsi_state = 'Neutral'
    if s['rsi'] > RSI_UPPER: rsi_state = 'Overbought'
    elif s['rsi'] < RSI_LOWER: rsi_state = 'Oversold'
    # MACD momentum
    macd_state = 'Bullish' if s['macd'] > s['macd_signal'] else 'Bearish'
    # BB position
    bb_state = 'Above Mid' if s['close'] > s['bb_mid'] else 'Below Mid'
    # Final signal logic: require majority of bullish conditions for BUY, majority bearish for SELL
    conds = [trend == 'Bullish', rsi_state == 'Neutral' or rsi_state == 'Oversold', macd_state == 'Bullish', bb_state == 'Above Mid']
    bull_count = sum(conds)
    conds_bear = [trend == 'Bearish', rsi_state == 'Neutral' or rsi_state == 'Overbought', macd_state == 'Bearish', bb_state == 'Below Mid']
    bear_count = sum(conds_bear)
    if bull_count >= 3:
        signal = 'BUY'
    elif bear_count >= 3:
        signal = 'SELL'
    else:
        signal = 'HOLD'
    # Entry, SL, TP
    entry = s['close']
    sl = s['bb_mid']
    tp = entry + (entry - sl) * TP_MULTIPLIER if signal == 'BUY' else entry - (sl - entry) * TP_MULTIPLIER if signal == 'SELL' else entry
    qty = (CAPITAL * RISK_PCT) / abs(entry - sl) if signal in ['BUY','SELL'] and entry != sl else 0
    return signal, trend, rsi_state, macd_state, bb_state, entry, sl, tp, qty

# Backtest BUY signals on primary timeframe
def backtest(df):
    signals = []
    for i in range(SMA_LONG, len(df) - BACKTEST_LOOKBACK):
        row = df.iloc[i]
        avg = df['close'].iloc[i-BACKTEST_LOOKBACK:i].mean()
        if row['close'] > avg and row['close'] > row['open']:
            signals.append((i, row['close']))
    wins = sum(1 for idx, price in signals
               if not df['close'].iloc[idx+1:idx+1+BACKTEST_LOOKBACK].empty
               and df['close'].iloc[idx+1:idx+1+BACKTEST_LOOKBACK].max() > price)
    return len(signals), wins

# Send Telegram message
def send_telegram(text):
    r = requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
                      json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
    return r

# MAIN
try:
    symbol = 'BTCUSDT'
    intervals = ['15m', '1h', '1d']
    results = {}
    for tf in intervals:
        df = compute_indicators(get_candles_df(symbol, tf))
        sig, trend, rsi_st, macd_st, bb_st, entry, sl, tp, qty = detailed_signal(df)
        total, wins = backtest(df)
        results[tf] = {
            'signal': sig,
            'trend': trend,
            'rsi': rsi_st,
            'macd': macd_st,
            'bb': bb_st,
            'entry': entry,
            'sl': sl,
            'tp': tp,
            'qty': qty,
            'win_rate': (wins/total*100) if total else 0
        }
    # Build message per timeframe
    time_str = datetime.now().strftime('%d %b %Y %H:%M')
    lines = [f"📊 {symbol} Detailed Signals (as of {time_str} WIB)", '────────────────────']
    for tf in intervals:
        r = results[tf]
        lines.extend([
            f"⏱ Timeframe: {tf}",
            f"⚡ Signal: {r['signal']}",
            f"📈 Trend: {r['trend']}",
            f"🔄 RSI: {r['rsi']}",
            f"🔥 MACD: {r['macd']}",
            f"📊 BB: {r['bb']}",
            f"🎯 Entry: {r['entry']:.2f}",
            f"🛑 SL:    {r['sl']:.2f}",
            f"🏹 TP:    {r['tp']:.2f}",
            f"📐 Qty:   {r['qty']:.4f}",
            f"📈 WinRate: {r['win_rate']:.1f}%",
            '────────────────────'
        ])
    msg = "\n".join(lines)
    res = send_telegram(msg)
    print('✅ Telegram sent' if res.status_code==200 else '❌ Telegram failed', res.status_code)
except Exception as e:
    print('❌ Error:', e)
