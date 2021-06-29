# Valuation and Quality Weighting Method
This page describes the valuation and quality ('Value-Quality,' 'value_quality') weighting method and lists the measures that are part of it.

## Overview
There are a few steps in the Valuation and Quality weighting method.

First, valuation and quality data is gathered on each stock. The valuation data measures how inexpensive the stock is. The quality data measures how good the company is, mainly, how good it is at generating earnings.

Second, each stock is given a score for each measure. That is, a stock will receive a score for its P/E ratio, one for its EV/EBITDA ratio, and so on. This score is a function of the measure for this stock relative to the total value for this measure for all stocks. For instance, if a basket contains only 2 stocks (AAPL and FB, say), and if AAPL's ROE is 3x that of FB, AAPL's ROE score will be 3x FB's ROE score.

Third, the scores for the individual measures are summed to produce two weights for each stock: a valuation weight and a quality weight. The valuation weight formula is:\
stock valuation weight = sum(all valuation scores for some stock) / sum(all valuation scores for all stocks)\
The quality weight formula is:\
stock quality weight = sum(all quality scores for some stock) / sum(all quality scores for all stocks)

Fourth, a final, single weight is generated for each stock using this formula:\
stock weight = (stock valuation weight)/2 + (stock quality weight)/2


## Valuation Measures
Listed below are the items that influence the Valuation score.

 __P/E TTM__.
Price to Earnings trailing twelve months.

__EV/EBITDA__.
Enterprise Value to Earnings Before Interest Taxes and Depreciation.

__P/FCF__.
Price to Free Cash Flow.

__EV/FCF__.
Enterprise Value to Free Cash Flow.

__P/S__.
Price to Sales.

__EV/S__.
Enterprise Value to Sales.

__P/E 5__.
(Not implemented.) Price to 5-year average earnings.

__EV/EBITDA 5__.
(Not implemented.) Price to 5-year average earnings.

__P/B__.
Price to Book value. NOTE: Give this a small weight.


## Quality Measures
Listed below are the items that influence the Quality score.

__Profit Margin__.
Average profit margin for last 5 years.

__Revenue Growth Rate__.
Annualized YoY revenue growth rate for last 5 years.

__EBITDA Growth Rate__.
Average YoY growth rate for last 10 years. This measure will be 0 if the company is not profitable.

__ROE (using net income)__.
Return on Equity where the numerator is Net Income.

__ROA (using net income)__.
Return on Assets where the numerator is Net Income.

__ROIC (using net income)__.
Return on Invested Capital where the numerator is Net Income.

__ROE (using EBITDA)__.
Return on Equity where the numerator is EBITDA.

__ROA (using EBITDA)__.
Return on Assets where the numerator is EBITDA.

__ROIC (using EBITDA)__.
Return on Invested Capital where the numerator is EBITDA.

__Current Ratio__.
Current Assets / Current Liabilities.

__Total Debt / Total Assets__.


