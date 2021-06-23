'''
A command line app for portfoliobuilder.
'''


from portfoliobuilder import utils, api_utils
from portfoliobuilder.builder import Portfolio, Basket
from portfoliobuilder.supported_indices import (supported_indices_list, 
                                                supported_indices_dict)


print("Welcome to the portfoliobuilder command line application. " +
        "Enter 'help' to see commands. Enter 'q' to quit, or kill with ^c.")

help_str = '''Usage: <command>

Commands:
newportfolio
listportfolios
inspectportfolio <portfolio_name>
newbasket (<symbol0> <symbol1> <symboli>) <weighting_method> <basket_weight>
        weighting_method options: equal market_cap value
newbasketfromindex <index_symbol> <weighting_method> <basket_weight>
listbaskets
inspectbasket <basket_name>
addbasket <portfolio_name> <basket_name>
listindices

Enter 'help' to see commands.
Enter 'q' to quit, or kill with ^c.'''

portfolios = {} # {'portfolio_name': Portfolio object}
baskets = {} # {'basket_name': Basket object}

def newportfolio():
    portfolio = Portfolio()
    portfolio.name = f'Portfolio{len(portfolios)}'
    portfolios[portfolio.name] = portfolio
    print(f'{portfolio.name} created.')

def listportfolios():
    if portfolios:
        for p_name in portfolios.keys():
            print(p_name)
    else:
        print('No portfolios.')

def inspectportfolio(command):
    invalid_cmd = command.split(' ')[0] != 'inspectportfolio'
    invalid_cmd = invalid_cmd or (len(command.split(' ')) > 2)
    invalid_cmd = invalid_cmd or (len(command.split(' ')) < 2)
    if invalid_cmd:
        print('Invalid command.')
        return

    portfolio_name = command.split(' ')[1]
    if portfolio_name in portfolios:
        portfolio = portfolios[portfolio_name]
        print(f'Inspecting {portfolio_name}...')
        print(f'Portfolio value: {portfolio.portfolio_value}')
        print(f'Portfolio cash: {portfolio.cash}')
        print(f"Portfolio's baskets: {portfolio.baskets}")
    else:
        print('Invalid command. Unknown portfolio.')

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
    invalid_cmd = command.split(' ')[0] != 'inspectbasket'
    invalid_cmd = invalid_cmd or (len(command.split(' ')) > 2)
    invalid_cmd = invalid_cmd or (len(command.split(' ')) < 2)
    if invalid_cmd:
        print('Invalid command.')
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

def addbasket(command):
    invalid_cmd = command.split(' ')[0] != 'addbasket'
    invalid_cmd = invalid_cmd or (len(command.split(' ')) > 3)
    invalid_cmd = invalid_cmd or (len(command.split(' ')) < 3)
    if invalid_cmd:
        print('Invalid command.')
        return

    portfolio_name = command.split(' ')[1]
    basket_name = command.split(' ')[2]
    if portfolio_name in portfolios:
        if basket_name in baskets:
            portfolio = portfolios[portfolio_name]
            basket = baskets[basket_name]
            total_weight = sum([b.weight for b in portfolio.baskets])
            if basket.weight + total_weight > 100:
                print(f'Invalid command. {total_weight}% of portfolio is allocated. ' + 
                        f'Trying to allocate an additional {basket.weight}% of {portfolio_name}.')
            else:
                portfolio.baskets.append(basket)
        else:
            print('Invalid command. Unknown basket.')
    else:
        print('Invalid command. Unknown portfolio.')

def listindices():
    print('Listing indices... (Note: some might not be supported by newbasketfromindex.)')
    print('Index | Symbol')
    for symbol in supported_indices_list:
        print(f'{supported_indices_dict[symbol]}  |  {symbol}')

def parse_command(command):
    if command == 'help':
        print(help_str)
    elif command == 'newportfolio':
        newportfolio()
    elif command == 'listportfolios':
        listportfolios()
    elif 'inspectportfolio ' in command:
        inspectportfolio(command)
    elif 'newbasket ' in command:
        newbasket(command)
    elif 'newbasketfromindex ' in command:
        newbasketfromindex(command)
    elif command == 'listbaskets':
        listbaskets()
    elif 'inspectbasket ' in command:
        inspectbasket(command)
    elif 'addbasket' in command:
        addbasket(command)
    elif command == 'listindices':
        listindices()
    elif command == 'q':
        print('Goodbye')
    else:
        print("Invalid command. Enter 'help' to see commands.")


# TODO: Implement the ability to read a list of symbols from a file.
# TODO: Implement buyportfolio, rebalance, savestate (which saves the portfolio to a database or something)
#       and recoverstate (which reads the saved portfolios into this session's variables).
# Maybe get rid of portfolio functionality and replace it with a single account (your Alpaca account)?


command = ''
while command is not 'q':
    command = input('> ')
    parse_command(command)
