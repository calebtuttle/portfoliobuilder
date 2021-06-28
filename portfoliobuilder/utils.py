import sys

from portfoliobuilder import api_utils


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