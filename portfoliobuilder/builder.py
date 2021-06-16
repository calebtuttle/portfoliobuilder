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

    def buy_equal_basket(self, basket):
        ''' Buy all stocks in basket, weighting them equally. '''
        num_constituents = len(basket.symbols)
        stock_weight = 1/num_constituents
        for symbol in basket.symbols:
            notional = self.cash * (basket.weight / 100) * stock_weight
            self.place_order(symbol, notional, 'buy')

    def buy_market_cap_basket(self, basket):
        ''' 
        Buy all stocks in basket, weighting them by market cap. 
        The greater the market cap, the greater the weight.
        '''
        stocks = [Stock(symbol) for symbol in basket.symbols]
        market_caps = [stock.update_market_cap() for stock in stocks]
        basket_market_cap = sum(market_caps)
        for i, symbol in enumerate(basket.symbols):
            stock_weight = market_caps[i] / basket_market_cap
            notional = self.cash * (basket.weight / 100) * stock_weight
            self.place_order(symbol, notional, 'buy')

    def buy_value_basket(self, basket):
        ''' 
        Buy all stocks in basket, weighting them by value.
        Value is determined by current Enterprise Value to
        Trailing Twelve Months Free Cash Flow. The smaller
        the EV/FCF, the greater the weight.
        '''
        stocks = [Stock(symbol) for symbol in basket.symbols]
        ev_to_fcfs = [stock.update_ev_to_fcf() for stock in stocks]
        
        # If a stock's EV/FCF is negative, give it as much
        # weight as the most expensive (highest EV/FCF) stock.
        max_ev_to_fcf = max(ev_to_fcfs)
        ev_to_fcfs = [max_ev_to_fcf if e2f is None else e2f for e2f in ev_to_fcfs]

        basket_ev_to_fcf = sum(ev_to_fcfs)
        for i, symbol in enumerate(basket.symbols):
            stock_weight = 1 - (ev_to_fcfs[i] / basket_ev_to_fcf)
            notional = self.cash * (basket.weight / 100) * stock_weight
            self.place_order(symbol, notional, 'buy')

    def buy_basket(self, basket):
        if basket.weighting_method is 'equal':
            self.buy_equal_basket(basket)
        elif basket.weighting_method is 'market_cap':
            self.buy_market_cap_basket(basket)
        elif basket.weighting_method is 'value':
            self.buy_value_basket(basket)
        else:
            raise Exception('\n\tInvalid weighting method')

    def build_portfolio(self):
        '''
        Purchase all stocks in each basket, weighting the stocks according
        to the weighting method indicated by each basket.
        '''
        # TODO: Check whether the account already has a portfolio (i.e.,
        # whether the account is holding anything other than cash).

        if not self.weights_are_valid():
            raise InvalidTotalWeightException()
        if not self.update_cash():
            print('Could not update cash. Try again or see Portfolio.update_cash()')
            raise BadAPICallException()

        for basket in self.baskets:
            self.buy_basket(basket)

    def rebalance(self):
        for basket in self.baskets:
            # rebalance basket
            pass

    def new_portfolio(self, baskets):
        ''' 
        Create a new portfolio. Create a list of baskets, and
        for each basket, choose a weight, weighting method, and
        list of stocks. 
        '''
        # TODO: Add appropriate checks.

        # TODO: Add user options.

        self.baskets = baskets
        self.build_portfolio()

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

        self.ev_to_fcf = 0 # current Enterprise Value / TTM Free Cash Flow
        self.last_ev_to_fcf_update = 0

    def update_market_cap(self):
        '''
        Return new market cap if successful.
        '''
        self.market_cap = api_utils.get_market_cap(self.symbol)
        self.last_market_cap_update = time.time()
        return self.market_cap

    def update_ev_to_fcf(self):
        '''
        Return new EBITDA per share if successful.
        '''
        self.ev_to_fcf = api_utils.get_ev_to_fcf(self.symbol)
        self.last_ev_to_fcf_update = time.time()
        return self.ev_to_fcf

        