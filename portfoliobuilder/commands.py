'''
This module implements the commands for the command line app.

To create a command:
- Create a class with the name of the command.
- Add an 'execute()' method to the class that executes the command.
- Add the command keyword and the class to the command_executables
    dictionary in run.py.
- Update the help string in the Help class to include the command.
'''
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from portfoliobuilder import utils, api_utils, basket_utils
from portfoliobuilder.models import Base, Basket, Stock
from portfoliobuilder.supported_indices import supported_indices_dict


def setup_db():
    global engine, session
    engine = create_engine('sqlite:////home/caleb/Desktop/myprograms' +\
                                    '/portfoliobuilder/sqlalchemy.db',
                                        echo=False, future=True)
    session = Session(engine)
    Base.metadata.create_all(bind=engine) # Create tables



# This variable is set in run.py everytime the user enters input
user_input = ''


class BasketCommand():
    '''
    A class inherited by commands where <basket_id>
    is the first parameter.
    '''
    @staticmethod
    def get_basket_from_user_input():
        try:
            basket_id = int(user_input.split(' ')[1])
            return session.get(Basket, basket_id)
        except ValueError:
            return

class Help():
    '''
    Namespace for functions that execute the help command.
    '''
    @staticmethod
    def execute():
        print('Usage: <command>\n\n' + \
            'Commands:\n' + \
            'inspectaccount\n' + \
            'linkaccount <alpaca_api_key> <alpaca_secret>\n' + \
            'newbasket <weighting_method> <basket_weight> (<symbol0> <symbol1> <symboli>)\n' + \
            '\tweighting_method options: equal market_cap value value_quality\n' + \
            'newbasketfromindex <weighting_method> <basket_weight> <index_symbol>\n' + \
            'listbaskets\n' + \
            'inspectbasket <basket_id>\n' + \
            'addsymbols <basket_id> <symbol1> <symboli>\n' + \
            'buybasket <basket_id>\n' + \
            'sellbasket <basket_id>\n' + \
            'deletebasket <basket_id>\n' + \
            'rebalance <basket_id>\n' + \
            'listindices\n\n' + \
            "Enter 'help' to see commands.\n"+ \
            "Enter 'quit' to quit, or kill with CTRL+C.")


class InspectAccount():
    '''
    Namespace for the methods that execute the inspectaccount command.
    '''
    @staticmethod
    def execute():
        response = api_utils.get_account()
        if response:
            for key in response:
                print(f'{key}: {response[key]}')
        else:
            print('Could not get account information.')


class LinkAccount():
    '''
    Namespace for the methods that execute the linkaccount command.
    '''
    @staticmethod
    def execute():
        if not LinkAccount.input_is_valid():
            return
        LinkAccount.set_environment_variables()
        LinkAccount.check_account_connected()

    @staticmethod
    def input_is_valid():
        '''
        Return a bool indicating whether the input is valid.
        '''
        return utils.has_num_args(user_input, 2)

    @staticmethod
    def set_environment_variables():
        key, secret = user_input.split(' ')[1:3]
        os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_KEY'] = key
        os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY'] = secret

    @staticmethod
    def check_account_connected():
        acc = api_utils.get_account()
        if acc:
            print(f'Linked to account with id: {acc["id"]}.')
        else:
            print('Could not link account.') 


class NewBasket():
    '''
    Namespace for the methods that execute the newbasket command.
    '''
    @staticmethod
    def execute():
        try:
            NewBasket.input_has_enough_args()
            NewBasket.create_basket()
        except IndexError:
            print("Invalid command. Enter 'help' to see usage.")
        except AssertionError:
            print('Assertion error. Ensure parameters are valid.')

    @staticmethod
    def input_has_enough_args():
        '''
        Ensure the user provides at least 3 arguments 
        (a symbol is considered an argument).
        '''
        assert len(user_input.split(' ')) >= 3

    @staticmethod
    def print_untradable_symbols(untradable):
        print('Some symbols are not tradable.', end=' ')
        print('The basket will be created without the following symbols: ', end=' ')
        for symbol in untradable:
            print(symbol, end=' ')

    @staticmethod
    def get_symbols():
        symbols = user_input.split('(')[1].split(')')[0].split(' ')
        tradable_symbols = utils.tradable_symbols_from(symbols)
        if symbols != tradable_symbols:
            untradable = set(symbols) - set(tradable_symbols)
            NewBasket.print_untradable_symbols(untradable)
        return tradable_symbols

    @staticmethod
    def get_args():
        weighting_method = user_input.split(' ')[1]
        basket_weight = float(user_input.split(' ')[2])
        symbols = NewBasket.get_symbols()
        return [weighting_method, basket_weight, symbols]

    @staticmethod
    def create_basket():
        '''
        Parse user_input for args for creating a Basket,
        create the resultant Basket, and add it to the db.
        '''
        weighting_method, weight, symbols = NewBasket.get_args()
        basket = Basket(active=False, weighting_method=weighting_method, 
                                        weight=weight, stocks=[])
        NewBasket.add_symbols_to_basket(symbols, basket)
        session.add(basket)
        session.flush()
        print(f'Basket{basket.id} created.')
    
    @staticmethod
    def add_symbols_to_basket(symbols, basket):
        for symbol in symbols:
            stock = Stock(symbol=symbol)
            basket.stocks.append(stock)


class NewBasketFromIndex():
    '''
    Namespace for the methods that execute the newbasketfromindex command

    newbasketfromindex <weighting_method> <basket_weight> <index_symbol>
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 3):
            return
        symbols = NewBasketFromIndex.get_symbols_in_index()
        NewBasketFromIndex.replace_index_with_symbols_in_user_input(symbols)
        NewBasket.execute()

    @staticmethod
    def get_symbols_in_index():
        split_input = user_input.split(' ')
        index = split_input[3]
        response = api_utils.get_index_constituents(index)
        return response['constituents']

    @staticmethod
    def replace_index_with_symbols_in_user_input(symbols):
        ''' Modify user_input so that NewBasket.execute() can be called. '''
        symbols = '(' + ' '.join(symbols) + ')'
        global user_input
        user_input = user_input.split(' ')
        user_input[3] = symbols
        user_input = ' '.join(user_input)


class ListBaskets():
    '''
    Namespace for the methods that execute the listbaskets command.
    '''
    @staticmethod
    def execute():
        baskets = session.query(Basket)
        if baskets:
            for b in baskets:
                print(f'Basket{b.id}')
        else:
            print('No baskets.')


class InspectBasket(BasketCommand):
    '''
    Namespace for the methods that execute the inspectbasket command.
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 1):
            return
        basket = InspectBasket.get_basket_from_user_input()
        if basket:
            InspectBasket.print_basket_info(basket)
        else:
            print('Invalid command. Unknown basket.')

    @staticmethod
    def print_basket_info(basket):
        '''
        basket : tuple
            An entry in the baskets table in the database
        '''
        active = 'True' if basket.active else 'False'
        symbols = [stock.symbol for stock in basket.stocks]
        symbols = ' '.join(symbols)
        print(f'Inspecting Basket{basket.id}...')
        print(f'Basket weighting method: {basket.weighting_method}')
        print(f'Basket weight: {basket.weight}%')
        print(f'Basket is active: {active}')
        print(f'Basket constituents: {symbols}')


class AddSymbols(BasketCommand):
    '''
    Namespace for the methods that execute the addsymbols command.
    '''
    @staticmethod
    def execute():
        basket = AddSymbols.get_basket_from_user_input()
        if not AddSymbols.basket_is_modifiable(basket):
            return
        new_symbols = AddSymbols.get_symbols_from_user_input()
        AddSymbols.add_new_symbols_not_in_basket(new_symbols, basket)

    @staticmethod
    def basket_is_modifiable(basket):
        if not basket:
            print(f'No basket with id {id}.')
            return False
        if basket.active:
            print(f'Basket{basket.id} is active. Cannot add symbols.')
            return False
        return True
    
    @staticmethod
    def get_symbols_from_user_input():
        '''
        Return a set of the tradable symbols from the symbols
        passed as arguments in user_input.
        '''
        new_symbols = user_input.split(' ')[2:]
        untradable_new_symbols = []
        for symbol in new_symbols:
            print(f'Determining whether {symbol} is tradable...', end='\r')
            asset = api_utils.get_asset(symbol)    
            sys.stdout.write("\033[K")
            if asset:
                if asset['tradable']:
                    continue
            print(f'{symbol} appears to not be tradable.')
            untradable_new_symbols.append(symbol)
        return set(new_symbols) - set(untradable_new_symbols)

    @staticmethod
    def add_new_symbols_not_in_basket(new_symbols, basket):
        '''
        new_symbols : set
            Set of tradable symbols designated by user_input
        basket : tuple
            An entry in the basket table in the database
        '''
        new_symbols = AddSymbols.get_new_symbols_not_in_basket(new_symbols, basket)
        AddSymbols.print_new_symbols(new_symbols)
        
        for symbol in new_symbols:
            stock = Stock(symbol=symbol)
            basket.stocks.append(stock)
        session.flush()

    @staticmethod
    def get_new_symbols_not_in_basket(new_symbols, basket):
        curr_symbols = [stock.symbol for stock in basket.stocks]
        curr_symbols = ' '.join(curr_symbols)
        intersection = new_symbols.intersection(set(curr_symbols))
        if intersection:
            print(f'The following stocks are already in Basket{basket.id}', end=' ')
            print(f'and will not be added to Basket{basket.id}:', end=' ')
            intersection_str = ' '.join(intersection)
            print(intersection_str)
        return new_symbols - intersection

    @staticmethod
    def print_new_symbols(new_symbols):
        new_symbols_str = ' '.join(new_symbols)
        print('Adding the following symbols: ', end='')
        print(new_symbols_str)


class BuyBasket(BasketCommand):
    '''
    Namespace for the methods that execute the buybasket command.
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 1):
            return
            
        basket = BuyBasket.get_basket_from_user_input()
        if basket.active:
            print(f'{basket[0]} is already active. Exiting.')
            return
        basket_utils.buy_basket(basket)
        BuyBasket.print_basket_and_purchase_info(basket)
        basket.active = True
        session.flush()

    @staticmethod
    def print_basket_and_purchase_info(basket):
        print(f'Orders to purchase stocks in Basket{basket.id} have been placed.')
        print(f'Weighting method: {basket.weighting_method}')
        print(f'Basket weight: {basket.weight}')
        print('Note: Some purchase orders might not have been placed.', end=' ')
        print('If no errors were printed above, all orders were placed successfully.')


class SellBasket(BasketCommand):
    '''
    Namespace for the methods that execute the sellbasket command.
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 1):
            return
        basket = SellBasket.get_basket_from_user_input()
        if not SellBasket.basket_is_modifiable(basket):
            return
        SellBasket.sell(basket)
        SellBasket.update_active_for_basket_in_db(basket)
        
    @staticmethod
    def basket_is_modifiable(basket):
        if not basket:
            print(f'No basket with id {basket.id}.')
            return False
        if not basket.active:
            print(f'Basket{basket.id} is not active. Cannot sell.')
            return False
        return True

    @staticmethod
    def sell(basket):
        '''
        basket : tuple
            An entry from the baskets table in the database
        '''
        symbols = [stock.symbol for stock in basket.stocks]
        for symbol in symbols:
            if api_utils.close_position(symbol):
                print('Successfully placed an order to sell '\
                        f'all shares of {symbol}.', end='\r')
                sys.stdout.write('\033[K')
            else:
                print(f'Could not place an order to sell {symbol}.', end=' ')
                print(f'Ensure your account has a position in {symbol}.', end=' ')
                print(f'If you have a position in {symbol}, you', end=' ')
                print('must place your order manually in Alpaca.')

    @staticmethod
    def update_active_for_basket_in_db(basket):
        print(f'Setting active to False for Basket{basket.id}.')
        print('If some orders were not placed, you must manually place them in Alpaca.')
        basket.active = False
        session.flush()


class DeleteBasket(BasketCommand):
    '''
    Namespace for the methods that execute the deletebasket command.
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 1):
            return
        basket = DeleteBasket.get_basket_from_user_input()
        if not basket:
            print(f'No basket with id {basket.id}.')
            return
        if basket.active:
            SellBasket.sell(basket)
        session.delete(basket)
        session.flush()


class Rebalance(BasketCommand):
    '''
    Namespace for the methods that execute the rebalance command.
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 1):
            return
        basket = Rebalance.get_basket_from_user_input()
        if not basket:
            print(f'No basket with id {basket.id}.')
            return
        acc_value = Rebalance.get_account_value()
        if acc_value <= 0:
            print('Nothing to rebalance')
            return

        weighting_method = basket.weighting_method
        basket_weight = basket.weight
        symbols = [stock.symbol for stock in basket.stocks]
        weights = Basket.get_weights(weighting_method, symbols)

        for symbol in symbols:
            curr_position = api_utils.get_position(symbol)
            if curr_position:
                print(f'Rebalancing {symbol}...', end='\r')
                goal_market_val = acc_value * (basket_weight / 100) * weights[symbol]
                curr_market_val = curr_position['market_value']
                Rebalance.rebalance(symbol, goal_market_val, curr_market_val)
                sys.stdout.write("\033[K")
            else:
                print(f'Could not rebalance {symbol}.')
        print(f'Basket{basket.id} rebalanced. See above for stocks that might not have been rebalanced.')

    @staticmethod
    def get_account_value():
        account = api_utils.get_account()
        if account:
            return float(account['equity'])
        else:
            print('Could not access account.')
            return 0

    @staticmethod
    def rebalance(symbol, goal_market_val, curr_market_val):
        '''
        Sell or buy symbol so that the account holds
        $goal_market_val instead of $curr_market_val of
        symbol.
        '''
        if goal_market_val < curr_market_val:
            notional = curr_market_val - goal_market_val
            if not api_utils.place_order(symbol, notional, 'sell'):
                print(f'Could not rebalance {symbol}')
        elif goal_market_val > curr_market_val:
            notional = goal_market_val - curr_market_val
            if not api_utils.place_order(symbol, notional, 'buy'):
                print(f'Could not rebalance {symbol}')


class ListIndices():
    '''
    Namespace for methods that execute the listindices command.
    '''
    @staticmethod
    def execute():
        print('Listing indices... (Note: some might not be supported by newbasketfromindex.)')
        print('Index | Symbol')
        for symbol in supported_indices_dict:
            print(f'{supported_indices_dict[symbol]}  |  {symbol}')


class Quit():
    '''
    Namespace for the methods that execute the quit command.
    '''
    @staticmethod
    def execute():
        print('Saving changes...')
        session.commit()
        print('Exiting portfoliobuilder...')
        session.close()
