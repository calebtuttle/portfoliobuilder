'''
A module with functions for ranking each stock in a basket.
'''
import numpy as np
import pandas as pd

from portfoliobuilder import api_utils

VALUATION_MEASURES = ['pe_ttm', 'ev_ebitda', 'p_fcf_last_year', 'ev_fcf', 'ps_ttm',
                    'ev_s', 'pb']
QUALITY_MEASURES = ['profit_margin', 'revenue_growth', 'ebitda_growth', 
        'roe_income', 'roaa_income', 'roic_income', 'roe_ebitda', 
        'roa_ebitda', 'roic_ebitda', 'current_ratio', 'assets_to_liabilities']

def get_measures(symbol):
    #TODO: For each endpoint, ensure the results are expected.
    # For example, ensure market cap is not a multiple of 1 million.
    # Finnhub endpoint
    metrics = api_utils.get_metrics(symbol)
    metrics = metrics['metric']

    # Polygon endpoint
    polygon_financials = api_utils.get_financials(symbol)['results'][0]

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

    measures_dict = {
        # Valuation measures
        'pe_ttm': pe_ttm,
        'ev_ebitda': ev_ebitda,
        'p_fcf_last_year': p_fcf_last_year,
        'ev_fcf': ev_fcf,
        'ps_ttm': ps_ttm,
        'ev_s': ev_s,
        'pb': pb,
        # Quality measures
        'profit_margin': profit_margin,
        'revenue_growth': revenue_growth,
        'ebitda_growth': ebitda_growth,
        'roe_income': roe_income,
        'roaa_income': roaa_income,
        'roic_income': roic_income,
        'roe_ebitda': roe_ebitda,
        'roa_ebitda': roa_ebitda,
        'roic_ebitda': roic_ebitda,
        'current_ratio': current_ratio,
        'assets_to_liabilities': assets_to_liabilities
    }

    measures_series = pd.Series(data=measures_dict)
    measures_series.name = symbol
    return measures_series


def rank(measures_series_list):
    '''
    measures_series_list : list
        A list of return values from get_measures().
    '''
    df = pd.concat(measures_series_list, axis=1)
    measure_type_col = ['quality' if i in QUALITY_MEASURES else 'valuation' for i in df.index]
    df['measure_type'] = measure_type_col

    # Address Nones. For valuation measures, replace with largest num
    # in row. For quality measures, replace with smallest num in row.
    valuation_max = df[df['measure_type'] == 'valuation'].max(axis=1)
    for measure in valuation_max.index:
        df.loc[measure] = df.loc[measure].fillna(valuation_max.loc[measure], inplace=False)
    quality_min = df[df['measure_type'] == 'quality'].min(axis=1)
    for measure in quality_min.index:
        df.loc[measure] = df.loc[measure].fillna(quality_min.loc[measure], inplace=False)

    # Address negative numbers by adding the absolute value of
    # the smallest number in a row to every element in the row. 
    symbols_cols = [True for i in range(len(df.columns)-1)]
    symbols_cols.append(False)
    df_no_measure_type = df.loc[:,symbols_cols].copy()
    mins = df_no_measure_type.min(axis=1)
    for measure in mins.index:
        df_no_measure_type.loc[measure] += abs(mins.loc[measure])
    # Maybe move the following line to a few steps down
    df[df_no_measure_type.columns] = df_no_measure_type

    # Generate a weight for each measure for each stock
    for measure in df_no_measure_type.index:
        measure_sum = df_no_measure_type.loc[measure].sum()
        row_name = measure + '_score'
        if df.loc[measure]['measure_type'] == 'valuation':
            df_no_measure_type.loc[row_name] = 1 - (df_no_measure_type.loc[measure] / measure_sum)
        elif df.loc[measure]['measure_type'] == 'quality':
            df_no_measure_type.loc[row_name] = df_no_measure_type.loc[measure] / measure_sum


def rank(stocks_and_measures):
    '''
    stocks_and_measures : list
        A list where each element is a return value of get_measures()
    '''
    # Rank according to valuation
    valuation_measures_lists = {
        'pe_ttm': [s['valuation_measures']['pe_ttm'] for s in stocks_and_measures.values()],
        'ev_ebitda': [s['valuation_measures']['ev_ebitda'] for s in stocks_and_measures.values()],
        'p_fcf_last_year': [s['valuation_measures']['p_fcf_last_year'] for s in stocks_and_measures.values()],
        'ev_fcf': [s['valuation_measures']['ev_fcf'] for s in stocks_and_measures.values()],
        'ps_ttm': [s['valuation_measures']['ps_ttm'] for s in stocks_and_measures.values()],
        'ev_s': [s['valuation_measures']['ev_s'] for s in stocks_and_measures.values()],
        'pb': [s['valuation_measures']['pb'] for s in stocks_and_measures.values()],
    }
    largest_dict = {}
    smallest_dict = {}
    for measure in valuation_measures_lists:
        # Handle Nones
        largest = max([i if i else 0.1 for i in valuation_measures_lists[measure]])
        valuation_measures_lists[measure] = [i if i else largest for i in valuation_measures_lists[measure]]
        smallest = min([i if i else 0.1 for i in valuation_measures_lists[measure]])
        largest_dict[measure] = largest
        smallest_dict[measure] = smallest
    valuation_measures_totals = {
        'pe_ttm': sum(valuation_measures_lists['pe_ttm']),
        'ev_ebitda': sum(valuation_measures_lists['ev_ebitda']),
        'p_fcf_last_year': sum(valuation_measures_lists['p_fcf_last_year']),
        'ev_fcf': sum(valuation_measures_lists['ev_fcf']),
        'ps_ttm': sum(valuation_measures_lists['ps_ttm']),
        'ev_s': sum(valuation_measures_lists['ev_s']),
        'pb': sum(valuation_measures_lists['pb'])
    }
    valuation_rankings = {}
    for symbol in stocks_and_measures:
        valuation_measures = stocks_and_measures[symbol]['valuation_measures']
        valuation_rankings[symbol] = {}
        for measure in valuation_measures:
            val = valuation_measures[measure]
            if not val:
                val = largest_dict[measure]
            # Add the smallest number to every value to ensure all numbers are >0
            val += abs(smallest_dict[measure])
            total = valuation_measures_totals[measure]
            valuation_rankings[symbol][measure] = val / total

    # Rank according to quality
    quality_measures_lists = {
        'profit_margin': [s['quality_measures']['profit_margin'] for s in stocks_and_measures.values()],
        'revenue_growth': [s['quality_measures']['revenue_growth'] for s in stocks_and_measures.values()],
        'ebitda_growth': [s['quality_measures']['ebitda_growth'] for s in stocks_and_measures.values()],
        'roe_income': [s['quality_measures']['roe_income'] for s in stocks_and_measures.values()],
        'roaa_income': [s['quality_measures']['roaa_income'] for s in stocks_and_measures.values()],
        'roic_income': [s['quality_measures']['roic_income'] for s in stocks_and_measures.values()],
        'roe_ebitda': [s['quality_measures']['roe_ebitda'] for s in stocks_and_measures.values()],
        'roa_ebitda': [s['quality_measures']['roa_ebitda'] for s in stocks_and_measures.values()],
        'roic_ebitda': [s['quality_measures']['roic_ebitda'] for s in stocks_and_measures.values()],
        'current_ratio': [s['quality_measures']['current_ratio'] for s in stocks_and_measures.values()],
        'assets_to_liabilities': [s['quality_measures']['assets_to_liabilities'] for s in stocks_and_measures.values()]
    }
    smallest_dict = {}
    for measure in quality_measures_lists:
        # Handle negative numbers
        smallest = min([i if i else 0.1 for i in quality_measures_lists[measure]])
        removed_nones = [i if i else smallest for i in quality_measures_lists[measure]]
        quality_measures_lists[measure] = [i+abs(smallest) for i in removed_nones]
        smallest_dict[measure] = smallest
    quality_measures_totals = {
        'profit_margin': sum(quality_measures_lists['profit_margin']),
        'revenue_growth': sum(quality_measures_lists['profit_margin']),
        'ebitda_growth': sum(quality_measures_lists['profit_margin']),
        'roe_income': sum(quality_measures_lists['profit_margin']),
        'roaa_income': sum(quality_measures_lists['profit_margin']),
        'roic_income': sum(quality_measures_lists['profit_margin']),
        'roe_ebitda': sum(quality_measures_lists['profit_margin']),
        'roa_ebitda': sum(quality_measures_lists['profit_margin']),
        'roic_ebitda': sum(quality_measures_lists['profit_margin']),
        'current_ratio': sum(quality_measures_lists['profit_margin']),
        'assets_to_liabilities': sum(quality_measures_lists['profit_margin'])
    }
    quality_rankings = {}
    for symbol in stocks_and_measures:
        quality_measures = stocks_and_measures[symbol]['quality_measures']
        quality_rankings[symbol] = {}
        for measure in quality_measures:
            val = quality_measures[measure]
            if not val:
                val = smallest_dict[measure]
            # Add the smallest number to every value to ensure all numbers are >0
            val += abs(smallest_dict[measure])
            total = quality_measures_totals[measure]
            quality_rankings[symbol][measure] = val / total
    
    return {
        'valuation_rankings': valuation_rankings,
        'quality_rankings': quality_rankings
    }






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