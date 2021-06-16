import time
import threading
import requests

# from builder import Portfolio

# portfolio = Portfolio()

# portfolio.new_basket(['AAPL'], weighting_method='equal', weight=110)
# portfolio.build_portfolio()

# r = portfolio.place_order('AAPL', 10, 'buy')
# print(r)



response = requests.get(url='https://finnhub.io/api/v1/stock/metric?symbol=AAPL&metric=all&token=bsk8trfrh5rb00eutvrg')
response = response.json()

for key in response['metric'].keys():
    print(key)

# response['metric']['ebitdPerShareTTM']