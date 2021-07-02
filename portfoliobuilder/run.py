'''
TODO: Test thoroughly. Then delete basket_functions.py and command_line_app.py.
'''

from portfoliobuilder import commands


command_executables = {
    'help': commands.Help,
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
    'exit': commands.Quit
}


def parse_user_input(user_input):
    try:
        commands.user_input = user_input
        command = user_input.split(' ')[0]
        command_executables[command].execute()
    except (IndexError, KeyError) as error:
        print(f'Invalid command. {type(error)}')

print("Welcome to the portfoliobuilder command line application. " +
        "Enter 'help' to see commands. Enter 'q' to quit, or kill with ^c.")

try:
    user_input = ''
    while True:
        user_input = input('> ')
        if user_input == 'exit':
            command_executables['exit'].execute()
            break
        parse_user_input(user_input)
except KeyboardInterrupt:
    command_executables['exit'].execute()
