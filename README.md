# BTCUSDT Multi-Timeframe Trading Signal Bot

This repository contains a Python script to generate trading signals for BTC/USDT based on multiple technical indicators across three timeframes (15m, 1h, 1d). It also performs a simple backtest to calculate win rate, and can send formatted reports via Telegram.

## Features

* **Multi-Timeframe Confirmation** (15m, 1h, 1d)
* **Technical Indicators**:

  * Simple Moving Averages (SMA Short & Long)
  * Relative Strength Index (RSI)
  * Moving Average Convergence Divergence (MACD)
  * Bollinger Bands (BB)
* **Signal Logic**: BUY, SELL or HOLD based on majority of indicator conditions
* **Simple Backtest**: Calculates historical win rate for BUY signals
* **Telegram Integration**: Sends formatted signal reports to a Telegram chat
* **Configurable Parameters**: Periods, thresholds, risk management, lookback

## Requirements

* Python 3.8+
* pip
* A Telegram bot token and chat ID

## Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/samsulrifai/signal_generator.git
   cd signal_generator
   ```
2. **Create & activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. **Install required libraries**

   ```bash
   pip install requests pandas numpy python-dotenv
   ```

## Configuration

1. **Create a `.env` file** in the project root:

   ```dotenv
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   ```
2. **(Optional) Adjust parameters** in the script:

   * SMA\_SHORT, SMA\_LONG
   * RSI\_PERIOD, RSI\_UPPER, RSI\_LOWER
   * MACD\_FAST, MACD\_SLOW, MACD\_SIGNAL
   * BB\_PERIOD, BB\_STD
   * TP\_MULTIPLIER, CAPITAL, RISK\_PCT, BACKTEST\_LOOKBACK

### Parameter Selection Guidelines

Choosing optimal parameter values is key to signal reliability. Here’s how to determine yours:

1. **Historical Backtesting**
   Run systematic backtests over different parameter combinations (a grid search) to find settings that yield high win rates and acceptable drawdowns.

   * Vary SMA periods (e.g. 20–200) and compare performance.
   * Test RSI bounds (e.g. \[30–70], \[40–60]) to balance sensitivity vs. noise.

2. **Market Regime Consideration**

   * In trending markets, longer SMAs (100–300) reduce whipsaw.
   * In range-bound markets, tighter BB\_STD (1–1.5) and shorter SMAs (20–50) capture reversals.

3. **Risk Appetite & Timeframe**

   * Higher timeframes (1h, 1d) tolerate wider SL/TP; lower timeframes (15m) need tighter stops.
   * Adjust `RISK_PCT` (e.g. 0.5–2%) based on portfolio size and risk tolerance.

4. **Adaptive Optimization**

   * Periodically re-optimize parameters (weekly or monthly) to adapt to volatility shifts.
   * Use walk-forward analysis: optimize on a training window, test on the next out-of-sample period.

5. **Validation**

   * Always test on fresh (unseen) data to avoid overfitting.
   * Monitor live performance and compare to backtested metrics to validate stability.

With these guidelines, you can tailor the bot to your trading style and the BTC/USDT market conditions.

## Usage

Run the main script to fetch data from Binance, compute indicators, backtest, and send the signal via Telegram:

```bash
python btc_sel.py
```

On success, you will see in console:

```
✅ Telegram sent 200
```

And receive a message in your Telegram chat with structured signals per timeframe.

## File Structure

* `btc_sel.py` : Main bot script
* `README.md`  : This documentation file
* `.env`       : Environment variables (not committed)

## License

This project is licensed under the MIT License.
