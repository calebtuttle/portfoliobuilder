'''
A command line app for portfoliobuilder.
'''
import os

from portfoliobuilder import utils, api_utils
from portfoliobuilder import command_line_utils as cmd_utils 
from portfoliobuilder.builder import Portfolio, Basket
from portfoliobuilder.supported_indices import (supported_indices_list, 
                                                supported_indices_dict)


print("Welcome to the portfoliobuilder command line application. " +
        "Enter 'help' to see commands. Enter 'q' to quit, or kill with ^c.")

help_str = '''Usage: <command>

Commands:
account
linkaccount <alpaca_api_key> <alpaca_secret> 
newbasket (<symbol0> <symbol1> <symboli>) <weighting_method> <basket_weight>
        weighting_method options: equal market_cap value
newbasketfromindex <index_symbol> <weighting_method> <basket_weight>
listbaskets
inspectbasket <basket_name>
buybasket <basket_name>
listindices

Enter 'help' to see commands.
Enter 'q' to quit, or kill with ^c.'''

baskets = {} # {'basket_name': Basket object}

def account():
    response = api_utils.get_account()
    for key in response:
        print(f'{key}: {response[key]}')

def linkaccount(command):
    if not cmd_utils.has_num_args(command, 2):
        return
    os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_KEY'] = command.split(' ')[1]
    os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY'] = command.split(' ')[2]
    # Test that the account was actually connected
    acc = api_utils.get_account()
    if acc:
        print(f'Linked to account with id: {acc["id"]}.')

def newbasket(command):
    try:
        symbols = command.split('(')[1].split(')')[0].split(' ')
        tradable_symbols = utils.tradable_symbols_from(symbols)
        if symbols != tradable_symbols:
            untradable = set(symbols) - set(tradable_symbols)
            print('The following symbols appear to not be tradable:', end=' ')
            for symbol in untradable:
                print(symbol, end=' ')
            ansr = input("\nWould you like to create this basket without these symbols (enter 'y' or 'n')? ")
            if ansr != 'y':
                print('Basket canceled.')
                return
        weighting_method = command.split(') ')[1].split(' ')[0]
        basket_weight = int(command.split(') ')[1].split(' ')[1])
        name = f'Basket{len(baskets)}'
        basket = Basket(symbols, weighting_method, basket_weight, name)
        baskets[name] = basket
        print(f'{name} created.')
    except IndexError:
        print("Invalid command. Enter 'help' to see usage.")
    except AssertionError:
        print('Assertion error. Ensure parameters are valid.')

def newbasketfromindex(command):
    ''' Create a new basket, using the symbols in the specified index. '''
    try:
        split_command = command.split(' ')
        index = split_command[1]
        symbols = api_utils.get_index_constituents(index)
        symbols = '(' + ' '.join(symbols) + ')'
        split_command[1] = symbols
        new_command = ' '.join(split_command)
        newbasket(new_command)
    except IndexError:
        print('Invalid command.')

def listbaskets():
    if baskets:
        for b in baskets:
            print(b)
    else:
        print('No baskets.')

def inspectbasket(command):
    if command.split(' ')[0] != 'inspectbasket':
        print('Invalid command.')
        return
    if not cmd_utils.has_num_args(command, 1):
        return

    basket_name = command.split(' ')[1]
    if basket_name in baskets:
        basket = baskets[basket_name]
        print(f'Inspecting {basket_name}...')
        print(f'Basket weight: {basket.weight}%')
        print(f'Basket weighting method: {basket.weighting_method}')
        print(f'Basket constituents: {basket.symbols}')
    else:
        print('Invalid command. Unknown basket.')

def buybasket(command):
    if not cmd_utils.has_num_args(command, 1):
        return
    portfolio = Portfolio()
    portfolio.update_cash()
    basket_name = command.split(' ')[1]
    basket = baskets[basket_name]
    portfolio.buy_basket(basket)
    print(f'Orders to purchase stocks in {basket_name} have been purchased.')
    print(f'Weighting method: {basket.weighting_method}.')
    print(f'Basket weight: {basket.weight}.')
    print('Note: Some purchase orders might have failed.')
    print('If no errors were printed, all stocks were purchased.')

def listindices():
    print('Listing indices... (Note: some might not be supported by newbasketfromindex.)')
    print('Index | Symbol')
    for symbol in supported_indices_list:
        print(f'{supported_indices_dict[symbol]}  |  {symbol}')

def parse_command(command):
    if command == 'help':
        print(help_str)
    elif command == 'account':
        account()
    elif 'linkaccount' in command:
        linkaccount(command)
    elif 'newbasket ' in command:
        newbasket(command)
    elif 'newbasketfromindex ' in command:
        newbasketfromindex(command)
    elif command == 'listbaskets':
        listbaskets()
    elif 'inspectbasket ' in command:
        inspectbasket(command)
    elif 'buybasket' in command:
        buybasket(command)
    elif command == 'listindices':
        listindices()
    elif command == 'q':
        print('Goodbye')
    else:
        print("Invalid command. Enter 'help' to see commands.")


# TODO: Implement the ability to read a list of symbols from a file.
# TODO: Implement buyportfolio, rebalance, savestate (which saves the portfolio to a database or something)
#       and recoverstate (which reads the saved portfolios into this session's variables).
# TODO: Implement connection with your Alpaca account


command = ''
while command is not 'q':
    command = input('> ')
    parse_command(command)
