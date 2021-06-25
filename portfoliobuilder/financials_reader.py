'''
This module provides functions to help read the response
from the Financials as Reported Finnhub endpoint.
'''

import sys

from portfoliobuilder import api_utils
import portfoliobuilder


# TODO: Plan for implementing this module: Iterate over each
#       method with different symbols. If a method's return value
#       is unexpected, update the method to address the need of the
#       symbol that caused the problem. By doing this, each method
#       might grow indefinitely, but hopefully all cases will be 
#       covered after a few symbols are tested.


REVENUE_CONCEPTS = ['SalesRevenueNet', 'Revenues',

    'TotalRevenuesAndOtherIncome', 'SalesRevenueGoodsNet',
    'RegulatedAndUnregulatedOperatingRevenue',
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'RevenueFromContractWithCustomerIncludingAssessedTax']

'''
REVENUE_CONCEPTS notes:
- 'ElectricUtilityRevenue' is revenue for AES
- 'SalesRevenueServicesGross' is revenue for CCL
- No single total revenue item for MTB
- No revenue field for some of WU's income statements
- 'HealthCareOrganizationPatientServiceRevenue' is revenue for HCA
- 'SalesRevenueServicesNet' is revenue for ROL and RHI
- 'RevenueMineralSales' is revenue for NEM
- No single revenue field for HBAN
- 'RefiningAndMarketingRevenue' is revenue for VLO
'''

REVENUE_LABELS = ['sales', 'net sales', 'revenue', 'revenues',
    'revenues:', 'total revenue', 'total revenues', 
    'total net revenues', 'revenue from operations']


def _find_revenue(income_statement, symbol):
    '''
    Given an income statement, use Finnhub's 'concept' and
    'label' items to return the total revenue from the 
    income statement.

    income_statement : list of dictionaries
        An income statement formatted like those from the
        Financials as Reported Finnhub endpoint
    '''
    if isinstance(income_statement, list):
        for item in income_statement:
            if item['concept'] in REVENUE_CONCEPTS:
                return item['value']

        # Try '{symbol}:{concept}'
        lower_symbol = symbol.lower()
        for item in income_statement:
            for concept in REVENUE_CONCEPTS:
                sym_concept = f'{lower_symbol}:{concept}'
                if item['concept'] == sym_concept:
                    return item['value']
        
        # Try using the labels instead of concepts
        for item in income_statement:
            if item['label'].lower() in REVENUE_LABELS:
                return item['value']

    elif isinstance(income_statement, dict):
        for key in income_statement:
            if key in REVENUE_CONCEPTS:
                return income_statement[key]

    return None

def get_revenues(symbol):
    '''
    Return a list of the annual revenue for the stock, sorted
    such that the most recent annual revenue is first in the list
    and the oldest last in the list.
    '''
    response = api_utils.get_financials_as_reported(symbol)
    data = response['data']
    # Ensure we get only one report per year
    new_data = []
    years_covered = []
    for item in data:
        if item['year'] not in years_covered:
            new_data.append(item)
            years_covered.append(item['year'])
    
    income_statements = [item['report']['ic'] for item in new_data]
    revenues = [_find_revenue(stmnt, symbol) for stmnt in income_statements]
    return revenues

