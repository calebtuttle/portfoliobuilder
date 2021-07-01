'''
NOTE: This module and run.py are being written as a refactor of command_line_app.py.
NOTE: Most of the classes here make use of the cursor and user_input
variables from the run.py module.
'''
import os
import sqlite3

from portfoliobuilder import utils, api_utils
from portfoliobuilder.run import cursor, user_input
from portfoliobuilder.basket import Basket
from portfoliobuilder.basket_functions import get_weights, buy_basket
from portfoliobuilder.supported_indices import (supported_indices_list, 
                                                supported_indices_dict)




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

