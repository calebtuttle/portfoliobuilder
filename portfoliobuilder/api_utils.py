import requests
import time

from portfoliobuilder import (alpaca_endpoint, alpaca_headers, 
    finnhub_endpoint, finnhub_key, polygon_endpoint, polygon_key)


################# Alpaca utility functions #################

_last_alpaca_call = 0
# _alpaca_limit = 10/3 # number of calls per second

def alpaca_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    def wrapper(*args, **kwargs):
        global _last_alpaca_call
        next_available_call = _last_alpaca_call + 0.3
        now = time.time()
        if next_available_call >= now:
            time.sleep(next_available_call - now)
        _last_alpaca_call = time.time()

        return func(*args, **kwargs)

    return wrapper

@alpaca_call
def get_account():
    url = alpaca_endpoint + 'account'
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()
    return None

@alpaca_call
def tradable(symbol):
    url = alpaca_endpoint + f'assets/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()['tradable']
    print(f'Got status code {response.status_code} in tradable() for symbol {symbol}.')
    return False
    
@alpaca_call
def fractionable_tradable(symbol):
    '''
    Return True if the asset denoted by symbol is both fractionable 
    and tradable, False otherwise.
    '''
    url = alpaca_endpoint + f'assets/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()['fractionable'] and response.json()['tradable']
    return False

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
    response = requests.post(url=url, json=payload, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()
    return None

@alpaca_call
def get_position(symbol):
    url = alpaca_endpoint + f'positions/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()
    return None

@alpaca_call
def close_position(symbol):
    url = alpaca_endpoint + f'positions/{symbol}'
    payload = {'percentage': 100}
    response = requests.delete(url=url, json=payload, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()
    return None


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

        return func(*args, **kwargs)

    return wrapper

@finnhub_call
def get_market_cap(symbol):
    url = finnhub_endpoint + 'stock/profile2'
    params = {'symbol': symbol, 'token': finnhub_key}
    response = requests.get(url=url, params=params)
    try: 
        market_cap = response.json()['marketCapitalization']
        market_cap *= 1_000_000 # Finnhub reports a multiple of a million
        return market_cap
    except KeyError:
        return None

@finnhub_call
def get_metrics(symbol):
    ''' Return the JSON response from the stock/metrics Finnhub endpoint. '''
    url = finnhub_endpoint + 'stock/metric'
    params = {'symbol': symbol, 'metric': 'all', 'token': finnhub_key}
    response = requests.get(url=url, params=params).json()
    if not response['metric'] and not response['series']:
        return None
    return response

@finnhub_call
def get_ev_to_fcf(symbol):
    ''' 
    Get current Enterprise Value / TTM Free Cash Flow. 
    
    Return EV/FCF if number is positive, None if negative.
    '''
    url = finnhub_endpoint + 'stock/metric'
    params = {'symbol': symbol, 'metric': 'all', 'token': finnhub_key}
    response = requests.get(url=url, params=params).json()
    try:
        ev_to_fcf = response['metric']['currentEv/freeCashFlowTTM']
        return ev_to_fcf
    except KeyError:
        return None

@finnhub_call
def get_financials_as_reported(symbol):
    '''
    Return the response from the Financials as Reported
    endpoint.
    '''
    url = finnhub_endpoint + 'stock/financials-reported'
    params = {'symbol': symbol, 'token': finnhub_key}
    response = requests.get(url=url, params=params)
    if response.status_code in range(200, 226):
        return response.json()
    return None

@finnhub_call
def get_index_constituents(index_symbol):
    '''
    Return a list of the stock symbols, None if unsuccessful.
    '''
    url = finnhub_endpoint + 'index/constituents'
    params = {'symbol': index_symbol, 'token': finnhub_key}
    response = requests.get(url=url, params=params).json()
    try:
        symbols = response['constituents']
        return symbols
    except KeyError:
        return None


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
