import alpaca_trade_api as tradeapi
import pandas as pd
import datetime
import time

# =========================
# CONFIG
# =========================
API_KEY = "PKFBMKVCHXQGXJT4MCA7GZWPHZ"
SECRET_KEY = "FC1DV4iCza5r16Vkxz6UHmJapNCfVYMtxVMp1owMM93"
BASE_URL = "https://paper-api.alpaca.markets"

STARTING_BALANCE = 1_000_000

# Stocks (tickers)
stocks = {
    "MCD": {"name": "McDonald's", "owned": 50},
    "HSY": {"name": "Hershey", "owned": 100},
    "TSN": {"name": "Tyson", "owned": 50},
   
}

TRADE_AMOUNT = 10  # buy/sell 7 shares each time

# =========================
# CONNECT TO ALPACA
# =========================
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# =========================
# GET WEEKLY AVERAGE
# =========================
def get_weekly_average(symbol):
    bars = api.get_bars(symbol, tradeapi.TimeFrame.Day, limit=7).df
    return bars['close'].mean()

# =========================
# GET CURRENT PRICE
# =========================
def get_current_price(symbol):
    trade = api.get_latest_trade(symbol)
    return trade.price

# =========================
# GET CURRENT POSITION
# =========================
def get_position(symbol):
    try:
        position = api.get_position(symbol)
        return int(position.qty)
    except:
        return 0

# =========================
# TRADE LOGIC
# =========================
def trade_stock(symbol):
    try:
        current_price = get_current_price(symbol)
        weekly_avg = get_weekly_average(symbol)
        owned = get_position(symbol)

        print("\n======================")
        print(f"{stocks[symbol]['name']} ({symbol})")
        print(f"Current Price: {current_price}")
        print(f"Weekly Avg: {weekly_avg}")
        print(f"Shares Owned: {owned}")

        # BUY CONDITION
        if current_price < weekly_avg:
            print("BUY SIGNAL → Buying 10 shares")
            api.submit_order(
                symbol=symbol,
                qty=TRADE_AMOUNT,
                side='buy',
                type='market',
                time_in_force='gtc'
            )

        # SELL CONDITION
        elif current_price > weekly_avg:
            if owned >= TRADE_AMOUNT:
                print("SELL SIGNAL → Selling 10 shares")
                api.submit_order(
                    symbol=symbol,
                    qty=TRADE_AMOUNT,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
            else:
                print("SELL SIGNAL but not enough shares")

        else:
            print("HOLD")

    except Exception as e:
        print(f"Error with {symbol}: {e}")

# =========================
# RUN ONE FULL CYCLE
# =========================
def run_trading_cycle():
    print("\n====================================")
    print(f"RUNNING TRADING CYCLE: {datetime.datetime.now()}")
    print("====================================")

    for symbol in stocks:
        trade_stock(symbol)

# =========================
# LOOP (EVERY 3 DAYS)
# =========================
def main():
    while True:
        run_trading_cycle()
       # print("\nWaiting 3 days...\n")
# =========================
# START PROGRAM
# =========================
if __name__ == "__main__":
    main()