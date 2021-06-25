'''
builder.py reimplemented to suite the command line app.
'''

from portfoliobuilder import api_utils


def get_weights(weighting_method, symbols):
    '''
    Get the weight for each stock according to the weighting method.
    Does not account for basket_weight, only for the weight of each
    stock _within_ the basket.

    weighting_method : str
        Must be either 'market_cap', 'equal', or 'value' (value isn't robust yet)
    symbols : list of strings
        The list of stocks to purchase. All elements must be valid ticker symbols.
    
    Return a dictionary weights s.t. len(weights) == len(symbols)
    where each element in weights has the form: 
        symbol: weight_for_symbol
    and where each weight is a positive number <= 1.
    '''
    if weighting_method == 'equal':
        num_constituents = len(symbols)
        stock_weight = 1/num_constituents
        weights_ls = [stock_weight for _ in range(len(symbols))]
        weights = dict(zip(symbols, weights_ls))
        return weights
    
    elif weighting_method == 'market_cap':
        get_market_cap = api_utils.get_market_cap
        market_caps = [get_market_cap(symbol) for symbol in symbols]
        basket_market_cap = sum(market_caps)
        weights = {}
        for i, symbol in enumerate(symbols):
            stock_weight = market_caps[i] / basket_market_cap
            weights[symbol] = stock_weight
        return weights

    elif weighting_method == 'value':
        get_ev_to_fcf = api_utils.get_ev_to_fcf
        ev_to_fcfs = [get_ev_to_fcf(symbol) for symbol in symbols]
        
        # If a stock's EV/FCF is negative, give it as much
        # weight as the most expensive (highest EV/FCF) stock.
        max_ev_to_fcf = max(ev_to_fcfs)
        ev_to_fcfs = [max_ev_to_fcf if e2f is None else e2f for e2f in ev_to_fcfs]

        basket_ev_to_fcf = sum(ev_to_fcfs)
        weights = {}
        for i, symbol in enumerate(symbols):
            stock_weight = 1 - (ev_to_fcfs[i] / basket_ev_to_fcf)
            weights[symbol] = stock_weight
        return weights

def buy_basket(basket_name, weighting_method, basket_weight, symbols):
    '''
    Buy a basket of stocks (designated by the symbols argument). 
    The amount of each stock to purchase is determined using
    the weighting_method and the total basket_weight.

    basket_name : str
        The name of the basket
    weighting_method : str
        Must be either 'market_cap', 'equal', or 'value' (value isn't robust yet)
    basket_weight : float
        The weight of the basket within the user's account. Designated as a number
        n such that 0 > n <= 100.
    symbols : list of strings
        The list of stocks to purchase. All elements must be valid ticker symbols.
    '''
    # Determine account value and cash available
    account = api_utils.get_account()
    if account:
        cash = float(account['cash'])
        acc_value = float(account['equity'])
    else:
        print('Could not access account. Exiting. Try again or ensure API keys are correct.')
        return
    
    # Ensure there is enough cash to give the basket its full weight
    if (basket_weight/100) * acc_value > cash:
        print(f'Not enough cash available to purchase {basket_name}. Exiting.')
        return

    # Ensure weighting_method is valid
    if weighting_method not in ['equal', 'market_cap', 'value']:
        print('Invalid weighting_method. Exiting.')
        return

    weights = get_weights(weighting_method, symbols)

    # Equal weighting
    # TODO: Turn this into a function
    if weighting_method == 'equal':
        ''' Buy all stocks in basket, weighting them equally. '''
        for symbol in symbols:
            print(f'Placing order to buy {symbol}...', end='\r')
            notional = acc_value * (basket_weight / 100) * weights[symbol]
            if not api_utils.place_order(symbol, notional, 'buy'):
                print(f'Order to buy {symbol} failed.')

    # Market cap weighting
    # TODO: Turn this into a function
    elif weighting_method == 'market_cap':
        ''' 
        Buy all stocks in basket, weighting them by market cap. 
        The greater the market cap, the greater the weight.
        '''
        for i, symbol in enumerate(symbols):
            print(f'Placing order to buy {symbol}...', end='\r')
            notional = acc_value * (basket_weight / 100) * weights[symbol]
            if not api_utils.place_order(symbol, notional, 'buy'):
                print(f'Order to buy {symbol} failed.')

    # Value weighting
    # TODO: Turn this into a function
    # TODO: Make this method more robust
    elif weighting_method == 'value':
        ''' 
        Buy all stocks in basket, weighting them by value.
        Value is determined by current Enterprise Value to
        Trailing Twelve Months Free Cash Flow. The smaller
        the EV/FCF, the greater the weight.
        '''
        for i, symbol in enumerate(symbols):
            print(f'Placing order to buy {symbol}...', end='\r')
            notional = acc_value * (basket_weight / 100) * weights[symbol]
            if not api_utils.place_order(symbol, notional, 'buy'):
                print(f'Order to buy {symbol} failed.')

