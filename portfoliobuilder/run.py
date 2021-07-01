
import sqlite3

from portfoliobuilder import commands

# TODO: change help_str: 'exit' is now the exit command, not 'q'


command_executables = {
    'inspectaccount': commands.InspectAccount,
    'linkaccount': commands.LinkAccount,
    'newbasket': commands.NewBasket,
    'newbasketfromindex': commands.NewBasketFromIndex,
    'listbaskets': commands.ListBaskets,
    'inspectbasket': commands.InspectBasket,
    'addsymbols': commands.AddSymbols,
    'buybasket': commands.BuyBasket,
    'sellbasket': commands.SellBasket,
    'deletebasket': commands.DeleteBasket,
    'rebalance': commands.Rebalance,
    'listindices': commands.ListIndices,
    'exit': commands.Exit
}


conn = sqlite3.connect('portfoliobuilder/portfoliobuilder.db')
cursor = conn.cursor()

# Ensure essential tables exist
# TODO: Change 'name' field to 'id', and make it an int
create_baskets_table = 'CREATE TABLE if not exists baskets' + \
                    ' (name text, weighting_method text,' + \
                    ' weight real, symbols text, active integer)' 
cursor.execute(create_baskets_table)

def parse_user_input(user_input):
    try:
        command = user_input[0]
        command_executables[command].execute()
    except (IndexError, KeyError):
        print('Invalid command.')

try:
    user_input = ''
    while user_input is not 'exit':
        user_input = input('> ')
        parse_user_input(user_input)
except KeyboardInterrupt:
    command_executables['exit'].execute()
