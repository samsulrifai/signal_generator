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
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
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
