'''
A module with functions for scoring a basket of stocks.
'''

from portfoliobuilder import api_utils

class Scorer():
    def __init__(self):
        pass

    def score(self):
        pass



def get_measures(symbol):
    #TODO: For each endpoint, ensure the results are expected.
    # For example, ensure market cap is not a multiple of 1 million.
    # Finnhub endpoint
    metrics = api_utils.get_metrics(symbol)
    metrics = metrics['metric']

    # Polygon endpoint
    polygon_financials = api_utils.get_financials(symbol)

    market_cap = metrics['marketCapitalization']
    ev = polygon_financials['enterpriseValue']

    pe_ttm = metrics['peBasicExclExtraTTM']

    # EV/EBITDA last year
    ev_ebitda = polygon_financials[0]['enterpriseValueOverEBITDA']

    # P/FCF last year
    fcf_last_year = polygon_financials[0]['freeCashFlow']
    p_fcf_last_year = market_cap / fcf_last_year

    ev_fcf = metrics['currentEv/freeCashFlowTTM']

    ps = metrics['psTTM']

    # EV/S

    # P/E 5

    # EV/EBITDA 5

    # P/B
    pb = metrics['pbQuarterly']

    profit_margin = metrics['netProfitMargin5Y']

    revenue_growth = metrics['revenueGrowth5Y']

    ebitda_growth = metrics['ebitdaCagr5Y']

    roe_income = metrics['roeTTM']

    # ROA using net income

    roic_income = metrics['roiTTM']

    # ROE using EBITDA

    # ROA using EBITDA

    # ROIC using EBITDA

    current_ratio = metrics['currentRatioQuarterly']

    # Total Debt / Total Assets


def rank(symbols):
    pass


'''
psuedo code for score()

for each Valuation measure: 
    rank stocks according to the measure
(each rank will be between 0 and 1)
for each stock:
    valuation score = sum of all valuation measure rankings
    (i.e., p/e rank + p/s rank + p/b rank, etc.)

for each quality measure:
    rank stocks according to the measure
for each stock:
    quality score = sum of all quality measure rankings

for each stock:
    score = (valuation score * 0.5) + (quality score * 0.5)

'''