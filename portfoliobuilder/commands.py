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
import sqlite3

from portfoliobuilder import utils, api_utils
from portfoliobuilder.basket_utils import Basket
from portfoliobuilder.supported_indices import supported_indices_dict


conn = sqlite3.connect('portfoliobuilder/portfoliobuilder.db')
cursor = conn.cursor()
# Ensure essential tables exist
# TODO: Change 'name' field to 'id', and make it an int
create_baskets_table = 'CREATE TABLE if not exists baskets' + \
                    ' (name text, weighting_method text,' + \
                    ' weight real, symbols text, active integer)' 
cursor.execute(create_baskets_table)


# This variable is set in run.py everytime the user enters input
user_input = ''


class BasketCommand():
    '''
    A class inherited by commands where <basket_name>
    is the first parameter.
    '''
    @staticmethod
    def get_basket_from_user_input():
        basket_name = user_input.split(' ')[1]
        cursor.execute('SELECT * FROM baskets WHERE name=?', (basket_name,))
        return cursor.fetchone()
    

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
            'newbasket (<symbol0> <symbol1> <symboli>) <weighting_method> <basket_weight>\n' + \
            '\tweighting_method options: equal market_cap value value_quality\n' + \
            'newbasketfromindex <index_symbol> <weighting_method> <basket_weight>\n' + \
            'listbaskets\n' + \
            'inspectbasket <basket_name>\n' + \
            'addsymbols <basket_name> <symbol1> <symboli>\n' + \
            'buybasket <basket_name>\n' + \
            'sellbasket <basket_name>\n' + \
            'deletebasket <basket_name>\n' + \
            'rebalance <basket_name>\n' + \
            'listindices\n\n' + \
            "Enter 'help' to see commands.\n"+ \
            "Enter 'quit' to quit, or kill with CTRL+c.")


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

    newbasket <weighting_method> <basket_weight> (<symbol0> <symbol1> <symboli>)
        weighting_method options: equal market_cap value value_quality
    '''
    @staticmethod
    def execute():
        try:
            NewBasket.input_has_enough_args()
            basket = NewBasket.create_basket()
            NewBasket.add_basket_to_db(basket)
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
        and return the resultant Basket.
        '''
        weighting_method, weight, symbols = NewBasket.get_args()
        num_baskets = cursor.execute('SELECT COUNT(*) FROM baskets')
        num_baskets = cursor.fetchone()[0]
        name = f'Basket{num_baskets}'
        return Basket(name, weighting_method, weight, symbols, False)
        
    @staticmethod
    def add_basket_to_db(basket):
        symbols_str = ' '.join(basket.symbols)
        sql_params = (basket.name, basket.weighting_method, basket.weight, symbols_str, 0)
        cursor.execute('INSERT INTO baskets VALUES (?,?,?,?,?)', sql_params)
        print(f'{basket.name} created.')


class NewBasketFromIndex():
    '''
    Namespace for the methods that execute the newbasketfromindex command

    newbasketfromindex <weighting_method> <basket_weight> <index_symbol>
    '''
    @staticmethod
    def execute():
        if not utils.has_num_args(user_input, 4):
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
        cursor.execute('SELECT * FROM baskets')
        baskets = cursor.fetchall()
        if baskets:
            for b in baskets:
                print(b[0])
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
        active = 'True' if basket[4] else 'False'
        print(f'Inspecting {basket[0]}...')
        print(f'Basket weighting method: {basket[1]}')
        print(f'Basket weight: {basket[2]}%')
        print(f'Basket is active: {active}')
        print(f'Basket constituents: {basket[3]}')


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
            print(f'No basket with the name {basket[0]}.')
            return False
        if basket[4]:
            print(f'{basket[0]} is active. Cannot add symbols.')
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
            if not api_utils.tradable(symbol):
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
        curr_symbols = basket[3].split(' ')
        all_symbols = set(curr_symbols).union(new_symbols)
        all_symbols_str = ' '.join(all_symbols)
        
        sql_params = (all_symbols_str, basket[0])
        cursor.execute('UPDATE baskets SET symbols=? WHERE name=?', sql_params)

    @staticmethod
    def get_new_symbols_not_in_basket(new_symbols, basket):
        curr_symbols = basket[3].split(' ')
        intersection = new_symbols.intersection(set(curr_symbols))
        if intersection:
            print(f'The following stocks are already in {basket[0]}', end=' ')
            print(f'and will not be added to {basket[0]}:', end=' ')
            intersection_str = ' '.join(intersection)
            print(intersection_str)
        return new_symbols - intersection

    @staticmethod
    def print_new_symbols(new_symbols):
        new_symbols_str = ' '.join(new_symbols)
        print('Adding the following symbols:', end='')
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
        if basket[4]:
            print(f'{basket[0]} is already active. Exiting.')
            return
        BuyBasket.buy(basket)
        cursor.execute('UPDATE baskets SET active=? WHERE name=?', (1,basket[0]))
        BuyBasket.print_basket_and_purchase_info(basket)

    @staticmethod
    def buy(basket):
        '''
        basket : tuple
            An entry from the baskets table in the database
        '''
        name = basket[0]
        weighting_method = basket[1]
        basket_weight = basket[2]
        symbols = basket[3].split(' ')
        Basket.buy_basket(name, weighting_method, basket_weight, symbols)
    
    @staticmethod
    def print_basket_and_purchase_info(basket):
        print(f'Orders to purchase stocks in {basket[0]} have been placed.')
        print(f'Weighting method: {basket[1]}.')
        print(f'Basket weight: {basket[2]}.')
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
            print(f'No basket with name {basket[0]}.')
            return False
        if not basket[4]:
            print(f'{basket[0]} is not active. Cannot sell.')
            return False
        return True

    @staticmethod
    def sell(basket):
        '''
        basket : tuple
            An entry from the baskets table in the database
        '''
        symbols = basket[3].split(' ')
        for symbol in symbols:
            if api_utils.close_position(symbol):
                print('Successfully placed an order to sell '\
                        f'all shares of {symbol}.', end='\r')
            else:
                print(f'Could not place an order to sell {symbol}.')
                print('Place order manually in Alpaca.')

    @staticmethod
    def update_active_for_basket_in_db(basket):
        print(f'Setting active to False for {basket[0]}.')
        print('If some orders were not placed, you must manually place them in Alpaca.')
        sql_params = (0, basket[0])
        cursor.execute('UPDATE baskets SET active=? WHERE name=?', sql_params)


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
            print(f'No basket with name {basket[0]}.')
        SellBasket.sell(basket)
        cursor.execute('DELETE FROM baskets WHERE name=(?)', (basket[0],))
        print(f'{basket[0]} deleted.')


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
            print(f'No basket with name {basket[0]}.')
            return
        acc_value = Rebalance.get_account_value()
        if acc_value <= 0:
            print('Nothing to rebalance')
            return

        weighting_method = basket[1]
        basket_weight = basket[2]
        symbols = basket[3].split(' ')
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
        print(f'{basket[0]} rebalanced. See above for stocks that might not have been rebalanced.')

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
        conn.commit()
        print('Exiting portfoliobuilder...')
        conn.close()
