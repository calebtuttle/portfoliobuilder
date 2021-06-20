from portfoliobuilder.builder import Portfolio, Basket

def copy_portfolio(portfolio):
    ''' 
    Return a distinct instance of portfolio where all 
    attributes of the copy are identical to those of portfolio.
    '''
    portfolio_copy = Portfolio()
    portfolio_copy.name = portfolio.name
    portfolio_copy.portfolio_value = portfolio.portfolio_value
    portfolio_copy.cash = portfolio.cash
    portfolio_copy.last_cash_update = portfolio.last_cash_update
    portfolio_copy.baskets = portfolio.baskets
    return portfolio_copy
