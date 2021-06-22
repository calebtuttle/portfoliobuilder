import requests
import time

from portfoliobuilder import alpaca_endpoint, alpaca_headers, finnhub_endpoint, finnhub_key


################# Alpaca utility functions #################

_last_alpaca_call = 0
# _alpaca_limit = 10/3 # number of calls per second

def alpaca_call(func):
    '''
    Method to ensure the API call rate limit isn't reached.
    '''
    def wrapper(*args, **kwargs):
        global _last_alpaca_call
        next_available_call = _last_alpaca_call + 0.3 # constant should be 0.3, right?
        now = time.time()
        if next_available_call >= now:
            time.sleep(next_available_call - now)
        _last_alpaca_call = time.time()
        # print(f'Aplaca call at {_last_alpaca_call}s') #TODO: Delete this line

        return func(*args, **kwargs)

    return wrapper

@alpaca_call
def get_account():
    url = alpaca_endpoint + 'account'
    response = requests.get(url=url, headers=alpaca_headers)
    return response.json()

@alpaca_call
def tradable(symbol):
    url = alpaca_endpoint + f'assets/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()['tradable']
    print(f'Got status code {response.status_code} in tradable() for symbol {symbol}. Trying again.')
    response = requests.get(url=url, headers=alpaca_headers)
    if response.status_code in range(200, 226):
        return response.json()['tradable']
    print(f'Second attempt in tradable() for symbol {symbol} failed.')
    return False
    
@alpaca_call
def fractionable_tradable(symbol):
    '''
    Return True if the asset denoted by symbol is both fractionable 
    and tradable, False otherwise.
    '''
    url = alpaca_endpoint + f'assets/{symbol}'
    response = requests.get(url=url, headers=alpaca_headers)
    response = response.json()
    try:
        if response['fractionable'] and response['tradable']:
            return True
    except KeyError:
        pass
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
    def wrapper(*args, **kwargs):
        global _last_finnhub_call
        next_available_call = _last_finnhub_call + 0.0333334
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
