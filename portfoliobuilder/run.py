
from portfoliobuilder import commands


command_executables = {
    'help': commands.Help,
    'inspectaccount': commands.InspectAccount,
    'linkalpaca': commands.LinkAlpaca,
    'linkfinnhub': commands.LinkFinnhub,
    'linkpolygon': commands.LinkPolygon,
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
    'quit': commands.Quit
}


def parse_user_input(user_input):
    try:
        commands.user_input = user_input
        command = user_input.split(' ')[0]
        command_executables[command].execute()
    except (IndexError, KeyError) as error:
        print(f'Invalid command. {type(error)}')


print("Welcome to the portfoliobuilder command line application. Enter " +
    "'help' to see commands. Enter 'quit' to quit, or kill with CTRL+C.")

commands.setup_db()

try:
    user_input = ''
    while True:
        user_input = input('> ')
        if user_input == 'quit':
            command_executables['quit'].execute()
            break
        parse_user_input(user_input)
except KeyboardInterrupt:
    command_executables['quit'].execute()
