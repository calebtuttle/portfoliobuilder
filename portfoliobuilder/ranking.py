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

    Return a pd.DataFrame where each column represents a different
    stock and the last row contains the weights.
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

    # Generate a score for each measure for each stock
    valuation_score_rows = []
    quality_score_rows = []
    for measure in df_no_measure_type.index:
        measure_sum = df_no_measure_type.loc[measure].sum()
        row_name = measure + '_score'
        if df.loc[measure]['measure_type'] == 'valuation':
            df_no_measure_type.loc[row_name] = 1 - (df_no_measure_type.loc[measure] / measure_sum)
            valuation_score_rows.append(row_name)
        elif df.loc[measure]['measure_type'] == 'quality':
            df_no_measure_type.loc[row_name] = df_no_measure_type.loc[measure] / measure_sum
            quality_score_rows.append(row_name)

    # Aggregate valuation measures and quality measures to
    # get a valuation score and quality score for each stock.
    final_valuation_score_row = {}
    for col in df_no_measure_type.columns:
        final_valuation_score = df_no_measure_type.loc[valuation_score_rows][col].sum()
        final_valuation_score_row[col] = final_valuation_score
    final_valuation_score_row = pd.Series(final_valuation_score_row)
    final_quality_score_row = {}
    for col in df_no_measure_type.columns:
        final_quality_score = df_no_measure_type.loc[quality_score_rows][col].sum()
        final_quality_score_row[col] = final_quality_score
    final_quality_score_row = pd.Series(final_quality_score_row)
    df_no_measure_type.loc['final_valuation_score'] = final_valuation_score_row / final_valuation_score_row.sum()
    df_no_measure_type.loc['final_quality_score'] = final_quality_score_row / final_quality_score_row.sum()

    # Generate a final, single weight for each stock
    val_row = df_no_measure_type.loc['final_valuation_score']
    quality_row = df_no_measure_type.loc['final_quality_score']
    df_no_measure_type.loc['weight'] = (val_row/2) + (quality_row/2)

    return df_no_measure_type
    

