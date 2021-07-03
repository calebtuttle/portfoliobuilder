
from portfoliobuilder import api_utils, weighting


_WEIGHTING_METHODS = {'equal': weighting.Equal, 
                    'market_cap': weighting.MarketCap, 
                    'value': weighting.Value, 
                    'value_quality': weighting.ValueQuality}


def get_weights(weighting_method, symbols):
    '''
    Get the weight for each stock according to the weighting method.
    Does not account for basket_weight, only for the weight of each
    stock _within_ the basket.

    weighting_method : str
        Must be either 'market_cap', 'equal', 'value' (naively implemented), or 'value_quality'
    symbols : list of strings
        The list of stocks to purchase. All elements must be valid ticker symbols.
    
    Return a dictionary weights s.t. len(weights) == len(symbols)
    where each element in weights has the form: 
        symbol: weight_for_symbol
    and where each weight is a positive number <= 1.
    '''
    try:
        return _WEIGHTING_METHODS[weighting_method].get_weights(symbols)
    except KeyError:
        raise Exception('Invalid weighting method')


def buy_basket(basket):
    '''
    Buy a basket of stocks (designated by the symbols argument). 
    The amount of each stock to purchase is determined using
    the weighting_method and the total basket_weight.
    '''
    # Determine account value and cash available
    account = api_utils.get_account()
    if account:
        cash = float(account['cash'])
        acc_value = float(account['equity'])
    else:
        print('Could not access account. Exiting. Try again or ensure API keys are correct.')
        return
    
    weighting_method = basket.weighting_method
    basket_weight = basket.weight
    symbols = [stock.symbol for stock in basket.stocks]

    # Ensure there is enough cash to give the basket its full weight
    if (basket_weight/100) * acc_value > cash:
        print(f'Not enough cash available to purchase Basket{basket.id}. Exiting.')
        return

    # Ensure weighting_method is valid
    if weighting_method not in _WEIGHTING_METHODS:
        print('Invalid weighting_method. Exiting.')
        return

    weights = get_weights(weighting_method, symbols)

    basket_weight = basket_weight / 100
    for symbol in weights.keys():
        print(f'Placing order to buy {symbol}...', end='\r')
        notional = acc_value * basket_weight * weights[symbol]
        if not api_utils.place_order(symbol, notional, 'buy'):
            print(f'Order to buy {symbol} failed.')

