from lib2to3.refactor import get_all_fix_names
from time import sleep
from binance.client import Client
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

api_key = "fZAaOG7MJ6mctNwYzmerZyEOkZO4FjYYOBGQH4m6ZdZPuXxPrlAhlMNizXcy0bab"
api_secret = "7HGiQzzcjzAhEgV2e4c0yZicJM0Bx1RGC90NNIiLXOFqoki5vMjYdPUPWf6aumnS"

client = Client(api_key, api_secret, testnet=True)

print(client)
print(client.ping())

print("Binance is connected")

style.use('ggplot')

short_window = 50
long_window = 100

# Time Frame
start = dt.datetime(2015, 1, 1)


# Loading in the data, Here its Bitcoin price

# plt.plot(price.tail(550))
# # setting 50 MA to blue color
# # # High MA color green
# plt.plot(ma_high, color="g")
# # Low MA color yellow
# plt.plot(ma_low,  color="y")
# plt.legend()
# # Showing the plot
# plt.show()

while True:
    end = dt.datetime.now()

    btcusd = web.DataReader("BTC-USD", 'yahoo', start, end)
    btcusd.reset_index(inplace=True)
    btcusd.set_index("Date", inplace=True)

    print(btcusd)

    price = btcusd[['Adj Close']]
    # Mean High for the last 50 days
    ma_high = btcusd['Close'].rolling(window=long_window, min_periods=0).mean()
    # Mean Low for last 50 days
    ma_low = btcusd['Close'].rolling(window=short_window, min_periods=0).mean()
    # 50 day Moving Average
    print(ma_low.tail())

    if ma_low.iloc[-1] > ma_high.iloc[-1]:
        params = {
            'symbol': 'BTCUSDT',
        }
        print(client.get_ticker(**params))
        buyprice = client.get_ticker(**params)['askPrice']

        print(ma_high.iloc[-1])
        print(client.get_account()['balances'][1])
        orders = client.get_all_orders(**params)
        if len(orders) < 1:
            params = {
                'symbol': 'BTCUSDT',
                'side': 'BUY',
                'type': 'LIMIT',
                'timeInForce': 'GTC',
                'quantity': 0.002,
                'price': buyprice
            }
            response = client.create_test_order(**params)
            print(response)


    sleep(20)
