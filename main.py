from data import get_data
from strategy import apply_strategy

stocks = ["MCD", "HSY", "TSN"]

for stock in stocks:
    data = get_data(stock)
    signal = apply_strategy(data)
    print(f"{stock}: {signal}")