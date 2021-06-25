'''
A command line app for portfoliobuilder.
Documentation for each command can be found in docs/command_line_app.md.
'''
import os
import sqlite3

from portfoliobuilder import utils, api_utils
from portfoliobuilder import command_line_utils as cmd_utils 
from portfoliobuilder.builder import Portfolio, Basket
from portfoliobuilder.command_line_builder import get_weights, buy_basket
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
sellbasket <basket_name>
deletebasket <basket_name>
rebalance <basket_name>
listindices

Enter 'help' to see commands.
Enter 'q' to quit, or kill with ^c.'''

# baskets = {} # {'basket_name': Basket object}

conn = sqlite3.connect('portfoliobuilder/portfoliobuilder.db')
cursor = conn.cursor()

# Ensure essential tables exist
# TODO: Maybe find a different way to store symbols?
create_baskets_table = 'CREATE TABLE if not exists baskets' + \
                    ' (name text, weighting_method text,' + \
                    ' weight real, symbols text, active integer)' 
cursor.execute(create_baskets_table)

def account():
    response = api_utils.get_account()
    for key in response:
        print(f'{key}: {response[key]}')

def linkaccount(command):
    ''' NOTE: Not entered into database. '''
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
        num_baskets = cursor.execute('SELECT COUNT(*) FROM baskets')
        num_baskets = cursor.fetchone()[0]
        name = f'Basket{num_baskets}'
        basket = Basket(symbols, weighting_method, basket_weight, name)
        symbols_str = ' '.join(symbols)
        sql_params = (name, weighting_method, basket_weight, symbols_str, 0)
        cursor.execute('INSERT INTO baskets VALUES (?,?,?,?,?)', sql_params)
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
    cursor.execute('SELECT * FROM baskets')
    baskets = cursor.fetchall()
    if baskets:
        for b in baskets:
            print(b[0])
    else:
        print('No baskets.')

def inspectbasket(command):
    if command.split(' ')[0] != 'inspectbasket':
        print('Invalid command.')
        return
    if not cmd_utils.has_num_args(command, 1):
        return

    basket_name = command.split(' ')[1]
    cursor.execute('SELECT name FROM baskets')
    basket_names = cursor.fetchall()
    if (basket_name,) in basket_names:
        cursor.execute('SELECT * FROM baskets WHERE name=?', (basket_name,))
        basket = cursor.fetchone()
        active = 'True' if basket[4] else 'False'
        print(f'Inspecting {basket_name}...')
        print(f'Basket weighting method: {basket[1]}')
        print(f'Basket weight: {basket[2]}%')
        print(f'Basket is active: {active}')
        print(f'Basket constituents: {basket[3]}')
    else:
        print('Invalid command. Unknown basket.')

def buybasket(command):
    if not cmd_utils.has_num_args(command, 1):
        return
    portfolio = Portfolio()
    portfolio.update_cash()
    basket_name = command.split(' ')[1]
    cursor.execute('SELECT * FROM baskets WHERE name=?', (basket_name,))
    basket = cursor.fetchone()
    if basket[4]:
        print(f'{basket_name} is already active. Exiting.')
        return
    cursor.execute('UPDATE baskets SET active=? WHERE name=?', (1,basket_name))
    weighting_method = basket[1]
    basket_weight = basket[2]
    symbols = basket[3].split(' ')
    buy_basket(basket_name, weighting_method, basket_weight, symbols)
    print(f'Orders to purchase stocks in {basket_name} have been placed.')
    print(f'Weighting method: {basket[1]}.')
    print(f'Basket weight: {basket[2]}.')
    print('Note: Some purchase orders might not have been placed.', end=' ')
    print('If no errors were printed above, all stocks were placed successfully.')

def sellbasket(command):
    if 'sellbasket' != command.split(' ')[0]:
        print('Invalid command.')
        return
    if not cmd_utils.has_num_args(command, 1):
        return
    
    basket_name = command.split(' ')[1]
    cursor.execute('SELECT * FROM baskets WHERE name=?', (basket_name,))
    basket = cursor.fetchone()
    if not basket:
        print(f'No basket with name {basket_name}.')
        return
    if not basket[4]:
        print(f'{basket_name} is not active.')
        return
    symbols = basket[3].split(' ')
    for symbol in symbols:
        if api_utils.close_position(symbol):
            print('Successfully placed an order to sell '\
                    f'all shares of {symbol}.', end='\r')
        else:
            print(f'Could not place an order to sell {symbol}.')
            print('Exiting. Try again or place orders manually in Alpaca.')
            return
    print(f'Setting active to False for {basket_name}.')
    print('If some orders were not placed, you must manually place them in Alpaca.')
    sql_params = (0, basket_name)
    cursor.execute('UPDATE baskets SET active=? WHERE name=?', sql_params)
    
def deletebasket(command):
    if 'deletebasket' != command.split(' ')[0]:
        print('Invalid command.')
        return
    if not cmd_utils.has_num_args(command, 1):
        return

    basket_name = command.split(' ')[1]
    cursor.execute('SELECT * FROM baskets WHERE name = (?)', (basket_name,))
    basket = cursor.fetchone()
    if basket:
        symbols = basket[3]
        for symbol in symbols:
            api_utils.close_position(symbol)
        cursor.execute('DELETE FROM baskets WHERE name = (?)', (basket_name,))
        print(f'{basket_name} deleted.')
    else:
        print(f'No basket with the name "{basket_name}".')

def rebalance(command):
    if 'rebalance' != command.split(' ')[0]:
        print('Invalid command.')
        return
    if not cmd_utils.has_num_args(command, 1):
        return
    
    basket_name = command.split(' ')[1]
    cursor.execute('SELECT * FROM baskets WHERE name=?', (basket_name,))
    basket = cursor.fetchone()
    if not basket:
        print(f'No basket named {basket_name}.')
        return
    weighting_method = basket[1]
    basket_weight = basket[2]
    symbols = basket[3].split(' ')
    # TODO: Turn this into a method, and move it to command_line_builder.py
    account = api_utils.get_account()
    if account:
        acc_value = float(account['equity'])
    else:
        print('Could not access account.')
        return
    weights = get_weights(weighting_method, symbols)
    for symbol in symbols:
        notional = acc_value * (basket_weight / 100) * weights[symbol]
        # TODO: Finish... buy, sell, whatever to rebalance.

def listindices():
    print('Listing indices... (Note: some might not be supported by newbasketfromindex.)')
    print('Index | Symbol')
    for symbol in supported_indices_list:
        print(f'{supported_indices_dict[symbol]}  |  {symbol}')

def exit():
    print('Saving changes...')
    conn.commit()
    print('Exiting portfoliobuilder...')
    conn.close()

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
    elif 'sellbasket' in command:
        sellbasket(command)
    elif 'deletebasket' in command:
        deletebasket(command)
    elif 'rebalance' in command:
        rebalance(command)
    elif command == 'listindices':
        listindices()
    elif command == 'q':
        exit()
    else:
        print("Invalid command. Enter 'help' to see commands.")


# TODO: Implement the ability to read a list of symbols from a file.
# TODO: Implement rebalance, savestate (which saves the portfolio to a sqlite database)
#       and recoverstate (which reads the saved portfolios into this session's variables).
#       No, simply recover the state every time a new session starts. Save it every time
#       savestate is called, and ask the user if they want to save everytime they exit
#       with 'q'.


try:
    command = ''
    while command is not 'q':
        command = input('> ')
        parse_command(command)
except KeyboardInterrupt:
    exit()
