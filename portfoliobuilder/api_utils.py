import requests
import time

from portfoliobuilder import alpaca_endpoint, alpaca_headers, finnhub_endpoint, finnhub_key


# TODO: Test all of these methods


################# Alpaca utility functions #################

_last_alpaca_call = 0
# _alpaca_limit = 10/3 # number of calls per second

def alpaca_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    global _last_alpaca_call
    nex_available_call = _last_alpaca_call + 0.3
    now = time.time()
    if nex_available_call >= now:
        time.sleep(nex_available_call - now)
    _last_alpaca_call = time.time()

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@alpaca_call
def get_account():
    url = alpaca_endpoint + 'account'
    response = requests.get(url=url, headers=alpaca_headers)
    return response.json()

@alpaca_call
def fractionable_tradable(symbol):
    '''
    Return True if the asset denoted by symbol is both fractionable 
    and tradable, False otherwise.
    '''
    url = alpaca_endpoint + f'assets/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    response = response.json()
    if response['fractionable'] and response['tradable']:
        return True
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
    response = response.json()
    if 'code' in response.keys():
        return None
    return response


################# Finnhub utility functions #################

_last_finnhub_call = 0
# _finnhub_limit = 30 # number of calls per second

def finnhub_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    global _last_finnhub_call
    nex_available_call = _last_finnhub_call + 0.0333334
    now = time.time()
    if nex_available_call >= now:
        time.sleep(nex_available_call - now)
    _last_finnhub_call = time.time()

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@finnhub_call
def get_market_cap(symbol):
    url = finnhub_endpoint + 'stock/profile2'
    params = {'symbol': symbol, 'token': finnhub_key}
    response = requests.get(url=url, params=params)
    market_cap = response.json()['marketCapitalization']
    market_cap *= 1_000_000 # Finnhub reports a multiple of a million
    return market_cap

@finnhub_call
def get_ebitda_ps(symbol):
    ''' Get TTM EBITDA per share. '''
    url = finnhub_endpoint + 'metric'
    params = {'symbol': symbol, 'metric': 'all', 'token': finnhub_key}
    response = requests.get(url=url, params=params)
    response = response.json()
    return response['metric']['ebitdPerShareTTM']
    