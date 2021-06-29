'''
A module for the weighting methods.
'''
import sys

import numpy as np
import pandas as pd

from portfoliobuilder import api_utils


class Equal():
    '''
    A namespace for the equal weighting method.
    '''
    @staticmethod
    def get_weights(symbols):
        num_constituents = len(symbols)
        stock_weight = 1/num_constituents
        weights_ls = [stock_weight for _ in range(len(symbols))]
        weights = dict(zip(symbols, weights_ls))
        return weights


class MarketCap():
    '''
    A namespace for the market_cap weighting method.
    '''
    @staticmethod
    def get_weights(symbols):
        get_profile = api_utils.get_profile2
        
        market_caps = []
        for symbol in symbols:
            profile = get_profile(symbol)
            if profile:
                # Finnhub reports a multiple of a million
                market_cap = profile['marketCapitalization'] * 1000000
                market_caps.append(market_cap)
            else:
                market_caps.append(1)

        basket_market_cap = sum(market_caps)
        weights = {}
        for i, symbol in enumerate(symbols):
            stock_weight = market_caps[i] / basket_market_cap
            weights[symbol] = stock_weight
        return weights


class Value():
    '''
    A namespace for the (naive) value weighting method.
    '''
    @staticmethod
    def get_weights(symbols):
        get_metrics = api_utils.get_metrics
        
        metrics_ls = [get_metrics(symbol)['metric'] for symbol in symbols]
        ev_to_fcfs = [metrics['currentEv/freeCashFlowTTM'] for metrics in metrics_ls]
        
        # If a stock's EV/FCF is negative (i.e., None), give it as much
        # weight as the most expensive (highest EV/FCF) stock.
        max_ev_to_fcf = max(ev_to_fcfs)
        ev_to_fcfs = [e2f if e2f else max_ev_to_fcf for e2f in ev_to_fcfs]

        basket_ev_to_fcf = sum(ev_to_fcfs)
        weights = {}
        for i, symbol in enumerate(symbols):
            stock_weight = ev_to_fcfs[-i] / basket_ev_to_fcf
            weights[symbol] = stock_weight
        return weights


class ValueQuality():
    '''
    A namespace for the value_quality weighting method.
    '''
    _VALUATION_MEASURES = ['pe_ttm', 'ev_ebitda', 'p_fcf_last_year', 'ev_fcf', 'ps_ttm',
                        'ev_s', 'pb']
    _QUALITY_MEASURES = ['profit_margin', 'revenue_growth', 'ebitda_growth', 
            'roe_income', 'roaa_income', 'roic_income', 'roe_ebitda', 
            'roa_ebitda', 'roic_ebitda', 'current_ratio', 'assets_to_liabilities']

    _empty_measures_series = pd.Series(data={
            # Valuation measures
            'pe_ttm': np.nan, 'ev_ebitda': np.nan, 'p_fcf_last_year': np.nan,
            'ev_fcf': np.nan, 'ps_ttm': np.nan, 'ev_s': np.nan, 'pb': np.nan,
            # Quality measures
            'profit_margin': np.nan, 'revenue_growth': np.nan,
            'ebitda_growth': np.nan, 'roe_income': np.nan,
            'roaa_income': np.nan, 'roic_income': np.nan,
            'roe_ebitda': np.nan, 'roa_ebitda': np.nan,
            'roic_ebitda': np.nan, 'current_ratio': np.nan,
            'assets_to_liabilities': np.nan
        })

    @staticmethod
    def _get_measures(symbol):
        '''
        Get measures of valuation and quality for the given stock.
        See docs/measures.md for more info.

        symbol : str
            A stock ticker symbol (e.g., 'AAPL')

        Return a pd.Series where the indices are the measure names
        and the series name is symbol.
        '''
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

    @staticmethod
    def _get_weighting_data(measures_series_list):
        '''
        measures_series_list : list
            A list of return values from get_measures().

        Return a pd.DataFrame where each column represents a different
        stock and the last row contains the weights.
        '''
        df = pd.concat(measures_series_list, axis=1)
        measure_type_col = ['quality' if i in ValueQuality._QUALITY_MEASURES else 'valuation' for i in df.index]
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
        df_no_measure_type = df.loc[:,symbols_cols].copy() # excludes 'measure_type' column
        mins = df_no_measure_type.min(axis=1)
        for measure in mins.index:
            df_no_measure_type.loc[measure] += abs(mins.loc[measure])
        
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
        # get a single valuation score and a single quality score 
        # for each stock.
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

        # Generate a single weight for each stock
        val_row = df_no_measure_type.loc['final_valuation_score']
        quality_row = df_no_measure_type.loc['final_quality_score']
        df_no_measure_type.loc['weight'] = (val_row/2) + (quality_row/2)

        return df_no_measure_type
    
    @staticmethod
    def get_weights(symbols):
        '''
        Given a list of stock symbols, generate a weight for each
        stock such that the total weights add up to 1 (100%).
        NOTE: If an error occurs during the API calls, the stock
        will be given a weight of 0; this is unlike the behavior
        of the other weighting methods.

        Return a dict matching the specifications of builder.get_weights()
        '''
        measures_series_list = []
        failed_symbols = []
        for symbol in symbols:
            print(f'Getting measures for {symbol}...', end='\r')
            try:
                measures = ValueQuality._get_measures(symbol)
                measures_series_list.append(measures)
            except (IndexError, KeyError) as e:
                sys.stdout.write("\033[K")
                print(f'{type(e)} for {symbol}')
                failed_symbols.append(symbol)
            sys.stdout.write("\033[K")
        
        print('Getting weights...', end='\r')
        data = ValueQuality._get_weighting_data(measures_series_list)
        sys.stdout.write("\033[K")
        weights = data.loc['weight'].to_dict()

        for symbol in failed_symbols:
            weights[symbol] = 0
        return weights
