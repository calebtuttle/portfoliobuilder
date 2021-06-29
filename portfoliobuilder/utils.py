import sys

from portfoliobuilder import api_utils


def has_num_args(command, num_args):
    '''
    Note: Pass entire command to this function, not just arguments.
    Return True if command has exactly num_args arguments, False otherwise.
    '''
    split_command = command.split(' ')
    if len(split_command) == (num_args + 1):
        return True
    print('Invalid command. Incorrect number of arguments.')
    return False


################# Functions that use api_utils #################

def tradable_symbols_from(symbols):
    ''' 
    Return the given list of symbols less the ones that aren't tradable. 
    '''
    tradable_symbols = []
    for symbol in symbols:
        print(f'Determining whether {symbol} is tradable...', end=f'\r')
        is_tradable = api_utils.get_asset(symbol)['tradable']
        if is_tradable:
            tradable_symbols.append(symbol)
    sys.stdout.write("\033[K")
    return tradable_symbols