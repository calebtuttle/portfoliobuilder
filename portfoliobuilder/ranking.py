'''
A module with functions for ranking each stock in a basket.
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
    polygon_financials = api_utils.get_financials(symbol)['results'][0]

    # print(polygon_financials) # TODO: Delete this line

    market_cap = metrics['marketCapitalization']
    ev = polygon_financials['enterpriseValue']
    ebitda = polygon_financials['earningsBeforeInterestTaxesDepreciationAmortizationUSD']
    assets = polygon_financials['assets']
    sales = polygon_financials['revenuesUSD']

    pe_ttm = metrics['peBasicExclExtraTTM']

    # EV/EBITDA last year
    ev_ebitda = polygon_financials['enterpriseValueOverEBITDA']

    # P/FCF last year
    fcf_last_year = polygon_financials['freeCashFlow']
    p_fcf_last_year = market_cap / fcf_last_year

    ev_fcf = metrics['currentEv/freeCashFlowTTM']

    ps_ttm = metrics['psTTM']

    ev_s = ev / sales

    # P/E 5

    # EV/EBITDA 5

    # P/B
    pb = metrics['pbQuarterly']

    profit_margin = metrics['netProfitMargin5Y']

    revenue_growth = metrics['revenueGrowth5Y']

    ebitda_growth = metrics['ebitdaCagr5Y']

    roe_income = metrics['roeTTM']

    roaa_income = polygon_financials['returnOnAverageAssets']

    roic_income = polygon_financials['returnOnInvestedCapital']

    # ROE using EBITDA
    equity = polygon_financials['averageEquity']
    roe_ebitda = ebitda / equity 

    # ROA using EBITDA
    roa_ebitda = ebitda / assets

    # ROIC using EBITDA
    invested_capital = polygon_financials['investedCapitalAverage']
    roic_ebitda = ebitda / invested_capital

    current_ratio = metrics['currentRatioQuarterly']

    # Assets / Liabilities
    liabilities = polygon_financials['totalLiabilities']
    assets_to_liabilities = assets / liabilities

    return {
        'valuation_measures':
        {'pe_ttm': pe_ttm,
        'ev_ebitda': ev_ebitda,
        'p_fcf_last_year': p_fcf_last_year,
        'ev_fcf': ev_fcf,
        'ps_ttm': ps_ttm,
        'ev_s': ev_s,
        'pb': pb},
        'quality_measures':
        {'profit_margin': profit_margin,
        'revenue_growth': revenue_growth,
        'ebitda_growth': ebitda_growth,
        'roe_income': roe_income,
        'roaa_income': roaa_income,
        'roic_income': roic_income,
        'roe_ebitda': roe_ebitda,
        'roa_ebitda': roa_ebitda,
        'roic_ebitda': roic_ebitda,
        'current_ratio': current_ratio,
        'assets_to_liabilities': assets_to_liabilities}
    }



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