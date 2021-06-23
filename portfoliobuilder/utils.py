import sys

from portfoliobuilder.builder import Portfolio, Basket
from portfoliobuilder import api_utils

def copy_portfolio(portfolio):
    ''' 
    Return a distinct instance of portfolio where all 
    attributes of the copy are identical to those of portfolio.
    '''
    portfolio_copy = Portfolio()
    portfolio_copy.name = portfolio.name
    portfolio_copy.portfolio_value = portfolio.portfolio_value
    portfolio_copy.cash = portfolio.cash
    portfolio_copy.last_cash_update = portfolio.last_cash_update
    portfolio_copy.baskets = portfolio.baskets
    return portfolio_copy


################# Functions that use api_utils #################

def tradable_symbols_from(symbols):
    ''' 
    Return the given list of symbols less the ones that aren't tradable. 
    '''
    tradable_symbols = []
    for symbol in symbols:
        print(f'Determining whether {symbol} is tradable...', end=f'\r')
        is_tradable = api_utils.tradable(symbol)
        if is_tradable:
            tradable_symbols.append(symbol)
    sys.stdout.write("\033[K")
    return tradable_symbols