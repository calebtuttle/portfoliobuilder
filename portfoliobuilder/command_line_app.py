'''
A command line app for portfoliobuilder.
'''

from portfoliobuilder.builder import Portfolio, Basket


print("Welcome to the portfoliobuilder command line application. " +
        "Enter 'help' to see commands. Enter 'q' to quit, or kill with ^c.")

help_str = '''Usage: <command>

Commands:
newportfolio
listportfolios
inspectportfolio <portfolio_name>
newbasket (<symbol0> <symbol1> <symboli>) <weighting_method> <basket_weight>
        weighting_method options: equal market_cap value
listbaskets
inspectbasket <basket_name>
addbasket <portfolio_name> <basket_name>

Enter 'help' to see commands.
Enter 'q' to quit, or kill with ^c.'''

portfolios = {} # {'portfolio_name': Portfolio object}
baskets = {} # {'basket_name': Basket object}

def newportfolio():
    portfolio = Portfolio()
    portfolio.name = f'Portfolio{len(portfolios)}'
    portfolios.append(portfolio)
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

def parse_command(command):
    if command == 'help':
        print(help_str)
    elif command == 'newportfolio':
        newportfolio()
    elif command == 'listportfolios':
        listportfolios()
    elif 'inspectportfolio' in command:
        inspectportfolio(command)
    elif 'newbasket' in command:
        newbasket(command)
    elif command == 'listbaskets':
        listbaskets()
    elif 'inspectbasket' in command:
        inspectbasket(command)
    elif 'addbasket' in command:
        addbasket(command)


# TODO: Implement buyportfolio, rebalance, savestate (which saves the portfolio to a database or something)
#       and recoverstate (which reads the saved portfolios into this session's variables) 


command = ''
while command is not 'q':
    command = input('> ')
    parse_command(command)
