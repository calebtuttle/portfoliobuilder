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
                stocks = [Stock(symbol) for symbol in basket.symbols]
                market_caps = [stock.update_market_cap() for stock in stocks]
                basket_market_cap = sum(market_caps)
                for i, symbol in enumerate(basket.symbols):
                    stock_weight = market_caps[i] / basket_market_cap
                    notional = self.cash * basket.weight * stock_weight
                    self.place_order(symbol, notional, 'buy')

            # TODO: Value weighting
            if basket.weighting_method is 'value':
                stocks = [Stock(symbol) for symbol in basket.symbols]
                ebitdas = [stock.update_ebitda_ps for stock in stocks]

                # We do this to prevent a single ebitda from having a weight greater than 100%, 
                # something that would happen if enough negative ebitdas are present; and to 
                # give less weight to stocks with negative ebitda.
                largest_ebitda = max(ebitdas)
                ebitdas = [largest_ebitda if e <= 0 else e for e in ebitdas]
                
                basket_ebitda = sum(ebitdas)
                for i, symbol in enumerate(basket.symbols):
                    stock_weight = 1 - (ebitdas[i] / basket_ebitda)
                    notional = self.cash * basket.weight * stock_weight
                    self.place_order(symbol, notional, 'buy')

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

        self.ebitda_ps = 0 # TTM EBITDA per share
        self.last_ebitda_ps_update = 0

    def update_market_cap(self):
        '''
        Return new market cap if successful.
        '''
        self.market_cap = api_utils.get_market_cap(self.symbol)
        self.last_market_cap_update = time.time()
        return self.market_cap

    def update_ebitda_ps(self):
        '''
        Return new EBITDA per share if successful.
        '''
        self.ebitda_ps = api_utils.get_ebitda_ps(self.symbol)
        self.last_ebitda_ps_update = time.time()
        return self.ebitda_ps