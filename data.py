import yfinance as yf

def get_data(symbol):
    data = yf.download(symbol, period="6mo", interval="1d")
    return data