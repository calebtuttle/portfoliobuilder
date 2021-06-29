import requests
import time

from portfoliobuilder import (alpaca_endpoint, alpaca_headers, 
    finnhub_endpoint, finnhub_key, polygon_endpoint, polygon_key)


################# Alpaca utility functions #################

_last_alpaca_call = 0
# _alpaca_limit = 10/3 # number of calls per second

def alpaca_call(func):
    '''
    Method to ensure the API call rate limit isn't reached and
    to return None in the event that the call fails.
    '''
    def wrapper(*args, **kwargs):
        global _last_alpaca_call
        next_available_call = _last_alpaca_call + 0.3
        now = time.time()
        if next_available_call >= now:
            time.sleep(next_available_call - now)
        _last_alpaca_call = time.time()

        response = func(*args, **kwargs)
        if response.status_code in range(200, 226):
            return response.json()
        return None

    return wrapper

@alpaca_call
def get_account():
    url = alpaca_endpoint + 'account'
    return requests.get(url=url, headers=alpaca_headers)

@alpaca_call
def get_asset(symbol):
    url = alpaca_endpoint + f'assets/{symbol}'
    return requests.get(url=url, headers=alpaca_headers)

@alpaca_call
def place_order(symbol, notional, side):
    '''
    Place a market day order to buy or sell notional amount of symbol. 

    symbol : str
        The ticker symbol of the stock
    notional : float
        How much, in dollars, of the stock to buy
    side : str
        'buy' or 'sell'

    Return the HTTP response if the order was placed successfully, 
    None otherwise.
    '''
    url = alpaca_endpoint + 'orders'
    payload = {'symbol': symbol, 'notional': str(notional), 'side': side,
                'type': 'market', 'time_in_force': 'day'}
    return requests.post(url=url, json=payload, headers=alpaca_headers)

@alpaca_call
def get_position(symbol):
    url = alpaca_endpoint + f'positions/{symbol}'
    return requests.get(url=url, headers=alpaca_headers)

@alpaca_call
def get_positions():
    url = alpaca_endpoint + f'positions'
    return requests.get(url=url, headers=alpaca_headers)

@alpaca_call
def close_position(symbol):
    url = alpaca_endpoint + f'positions/{symbol}'
    payload = {'percentage': 100}
    return requests.delete(url=url, json=payload, headers=alpaca_headers)


################# Finnhub utility functions #################

_last_finnhub_call = 0
# _finnhub_limit = 1 # number of calls per second

def finnhub_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    def wrapper(*args, **kwargs):
        global _last_finnhub_call
        next_available_call = _last_finnhub_call + 1
        now = time.time()
        if next_available_call >= now:
            time.sleep(next_available_call - now)
        _last_finnhub_call = time.time()

        response = func(*args, **kwargs)
        if response.status_code in range(200, 226):
            return response.json()
        return None

    return wrapper

@finnhub_call
def get_profile2(symbol):
    url = finnhub_endpoint + 'stock/profile2'
    params = {'symbol': symbol, 'token': finnhub_key}
    return requests.get(url=url, params=params)

@finnhub_call
def get_metrics(symbol):
    ''' Return the JSON response from the stock/metrics Finnhub endpoint. '''
    url = finnhub_endpoint + 'stock/metric'
    params = {'symbol': symbol, 'metric': 'all', 'token': finnhub_key}
    return requests.get(url=url, params=params)

@finnhub_call
def get_financials_as_reported(symbol):
    '''
    Return the response from the Financials as Reported
    endpoint.
    '''
    url = finnhub_endpoint + 'stock/financials-reported'
    params = {'symbol': symbol, 'token': finnhub_key}
    return requests.get(url=url, params=params)

@finnhub_call
def get_index_constituents(index_symbol):
    '''
    Return a list of the stock symbols, None if unsuccessful.
    '''
    url = finnhub_endpoint + 'index/constituents'
    params = {'symbol': index_symbol, 'token': finnhub_key}
    return requests.get(url=url, params=params).json()


################# Polygon utility functions #################

_last_polygon_call = 0
# _polygon_limit = 0.084 # number of calls per second

def polygon_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    def wrapper(*args, **kwargs):
        global _last_polygon_call
        next_available_call = _last_polygon_call + 12
        now = time.time()
        if next_available_call >= now:
            time.sleep(next_available_call - now)
        _last_polygon_call = time.time()

        return func(*args, **kwargs)

    return wrapper

@polygon_call
def get_financials(symbol):
    # TODO: Test that this method returns data for the expected years
    url = polygon_endpoint + f'financials/{symbol}'
    params = {'limit': 10, 'type': 'Y', 
                'sort':'-reportPeriod', 
                'apiKey': polygon_key}
    response = requests.get(url, params=params)
    return response.json()
