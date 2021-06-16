import time

from portfoliobuilder import api_utils
from portfoliobuilder.exceptions import InvalidTotalWeightException, BadAPICallException


class Portfolio():
    def __init__(self):
        self.portfolio_value = 0
        self.cash = 0
        self.last_cash_update = 0
        self.baskets = []

    def new_basket(self, symbols, weighting_method='equal', weight=100):
        basket = Basket(symbols, weighting_method, weight)
        self.baskets.append(basket)

    def weights_are_valid(self):
        total_weight = 0
        for basket in self.baskets:
            total_weight += basket.weight
        if total_weight > 100 or total_weight < 0:
            return False
        return True

    def update_cash(self):
        '''
        Update self.cash to reflect the amount in the account. 

        Return cash amount if API call was succesful, None otherwise.
        '''
        account = api_utils.get_account()
        
        if 'code' in account.keys():
            return None

        cash = float(account['cash'])
        self.cash = cash
        self.last_cash_update = time.time()
        return cash

    def symbols_to_stocks(self, symbols):
        '''
        Generate a list of Stock objects from a list of ticker symbols.

        Return a list of Stock objects.
        '''
        stocks = []
        for symbol in symbols:
            stock = Stock(symbol)
            stock.update_market_cap()
            stocks.append(stock)
        return stocks
            

    def build_portfolio(self):
        '''                     
        Purchase all stocks in each basket, weighting the stocks according
        to the weighting method indicated by each basket.
        '''
        if not self.weights_are_valid():
            raise InvalidTotalWeightException()
        
        if not self.update_cash():
            print('Could not update cash. Try again or see Portfolio.update_cash()')
            raise BadAPICallException()

        # TODO: Finish the below for loop, and split it into multiple funcitons
        for basket in self.baskets:
            num_constituents = len(basket.symbols)

            # TODO: Turn this into a function
            if basket.weighting_method is 'equal':
                stock_weight = 1/num_constituents
                for symbol in basket.symbols:
                    notional = self.cash * basket.weight * stock_weight
                    self.place_order(symbol, notional, 'buy')

            # TODO: Turn this into a function
            if basket.weighting_method is 'market_cap':
                stocks = self.symbols_to_stocks(basket.symbols)
                basket_market_cap = sum([stock.market_cap for stock in stocks])
                for i, symbol in enumerate(basket.symbols):
                    stock_weight = stocks[i].market_cap / basket_market_cap
                    notional = self.cash * basket.weight * stock_weight

            # TODO: Value weighting

    def rebalance(self):
        for basket in self.baskets:
            # rebalance basket
            pass

    def execute(self):
        '''
        Execute this portfolio. This method will run until this portfolio is liquidated
        or replaced by another portfolio. This method handles all rebalancing.
        '''
        self.build_portfolio()
        pass


class Basket():
    '''
    A basket is a collection of stocks. It is basically a sub-portfolio.
    It provides the user with greater granularity with respect to weighting.
    '''
    def __init__(self, symbols, weighting_method='equal', weight=100):
        '''
        symbols : list
            List of stocks' ticker symbols. 
        weighting_method : str
            Either 'equal', 'market_cap', or 'value'.
        weight : float
            The weight (in percent) of the basket in the whole portfolio. Default: 100%.
        '''
        self.symbols = symbols
        self.weighting_method = weighting_method
        self.weight = weight

        assert weight > 0 and weight <= 100
        assert weighting_method in ['equal', 'market_cap', 'value']
        assert self.symbols_are_valid()

    def symbols_are_valid(self):
        '''
        A valid symbol is one denoting an asset that is both fractionable 
        and tradable.

        Return True if all symbols in self.symbols are valid, False otherwise.
        '''
        are_valid = []
        for symbol in self.symbols:
            valid = api_utils.fractionable_tradable(symbol)
            are_valid.append(valid)
        if all(are_valid):
            return True
        return False
    

class Stock():
    def __init__(self, symbol):
        self.symbol = symbol
        self.market_cap = 0
        self.last_market_cap_update = 0

    def update_market_cap(self):
        '''
        Return new market cap if successful.
        '''
        self.market_cap = api_utils.get_market_cap(self.symbol)
        self.last_market_cap_update = time.time()
        return self.market_cap

