import pandas as pd

def apply_strategy(data):
    data["MA200"] = data["Close"].rolling(200).mean()
    data["RSI"] = compute_rsi(data["Close"])

    latest = data.iloc[-1]

    if latest["Close"] > latest["MA200"] and latest["RSI"] < 35:
        return "BUY"
    elif latest["RSI"] > 65:
        return "SELL"
    else:
        return "HOLD"


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))