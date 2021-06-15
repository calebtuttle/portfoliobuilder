import requests

from exceptions import InvalidTotalWeightException, BadAPICallException


endpoint = 'https://paper-api.alpaca.markets/v2/'

paper_key = 'PK1WEJMYZYRT8K4QMJ58'
paper_secret = '75ZqYASD2sK0gPuf69tXwGOIwlp6eiWprBtEjfQj'

headers = {'APCA-API-KEY-ID': paper_key, 'APCA-API-SECRET-KEY': paper_secret}

def get_account():
    url = endpoint + 'account'
    response = requests.get(url=url, headers=headers)
    return response.json()

acc = get_account()


class Portfolio():
    def __init__(self):
        self.portfolio_value = 0
        self.cash = 0
        self.baskets = []

    def new_basket(self, tickers, weighting_method='equal', weight=100):
        basket = Basket(tickers, weighting_method, weight)
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
        url = endpoint + 'account'
        response = requests.get(url=url, headers=headers)

        if 'code' in response.json().keys():
            return None

        cash = float(response.json()['cash'])
        self.cash = cash
        return cash

    def place_order(self, ticker, notional, side):
        '''
        Place a market day order to buy or sell notional amount of ticker. 

        ticker : str
            The ticker symbol of the stock
        notional : float
            How much, in dollars, of the stock to buy
        side : str
            'buy' or 'sell'

        Return the HTTP response if the order was placed successfully, 
        None otherwise.
        '''
        url = endpoint + 'orders'
        payload = {'symbol': ticker, 'notional': str(notional), 'side': side,
                   'type': 'market', 'time_in_force': 'day'}
        response = requests.post(url=url, json=payload, headers=headers)
        if 'code' in response.json().keys():
            return None
        return response.json()

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

        # TODO: Check that each ticker in each basket.tickers is valid

        # TODO: Finish the below for loop, and split it into multiple funcitons
        for basket in self.baskets:
            num_constituents = len(basket.tickers)

            if basket.weighting_method is 'equal':
                stock_weight = 1/num_constituents
                for ticker in basket.tickers:
                    notional = self.cash * basket.weight * stock_weight
                    self.place_order(ticker, notional, 'buy')
            # TODO: market_cap weighting

            # TODO: Value weighting

    def rebalance(self):
        for basket in self.baskets:
            # rebalance basket
            pass


class Basket():
    '''
    A basket is a collection of stocks. It is basically a sub-portfolio.
    It provides the user with greater granularity with respect to weighting.
    '''
    def __init__(self, tickers, weighting_method='equal', weight=100):
        '''
        tickers : list
            List of tickers to include in the basket.
        weighting_method : str
            Either 'equal', 'market_cap', or 'value'.
        weight : float
            The weight (in percent) of the basket in the whole portfolio. Default: 100%.
        '''
        self.tickers = tickers
        self.weighting_method = weighting_method
        self.weight = weight
    