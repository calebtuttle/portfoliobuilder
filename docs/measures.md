# Valuation and Quality Measures
This page describes the valuation and quality measures that are part of the 'value_quality' weighting method.

## Overview
Each stock receives a score. A stock with a higher score receives more weight. A score only has meaning in relation to other stocks in the same basket. Each stock's score consists of two sub-scores, Valuation and Quality, such that the total score = (Valuation * 0.5) + (Quality * 0.5). 

The Valuation score increases as the stock's Valuation ratios decrease. For example, a stock with a P/E of 20 will likely have a higher Valuation score than a stock with a P/E of 40. The Quality score increases as measures of Quality increase. For example, a stock with consistent YoY earnings growth of 15% will likely have a higher Quality score than a stock whose earnings have consistently decreased. 



TODO: Discuss methodology--how you get a single weight from all these measures.



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


