# Stock Scoring Methodology
This document describes the methodology of the scoring system used by the value weighting method.

## Overview
Each stock receives a score. A stock with a higher score receives more weight. Each stock's score consists of two sub-scores, Valuation and Quality, such that the total score = (Valuation * 0.5) + (Quality * 0.5). 

The Valuation score increases as the stock's Valuation ratios decrease. For example, a stock with a P/E of 20 will likely have a higher Valuation score than a stock with a P/E of 40. The Quality score increases as measures of Quality increase. For example, a stock with consistent YoY earnings growth of 15% will likely have a higher Quality score than a stock whose earnings have consistently decreased. 


## Valuation Measures
Listed below are the items that influence the Valuation score.

#### P/E 
Price to Earnings.

### EV/EBITDA 
Enterprise Value to Earnings Before Interest Taxes and Depreciation.

### P/FCF
Price to Free Cash Flow.

### EV/FCF
Enterprise Value to Free Cash Flow.

### P/S 
Price to Sales.

### EV/S
Enterprise Value to Sales.

### P/B
Price to Book value. NOTE: Give this a small weight.


## Quality Measures
Listed below are the items that influence the Quality score.

### Profit Margin

### Revenue Growth Rate
Average YoY growth rate for last 10 years.

### Earnings Growth Rate
Average YoY growth rate for last 10 years. This measure will be 0 if the company is not profitable.

### ROE (using net income)
Return on Equity where the numerator is Net Income.

### ROA (using net income)
Return on Assets where the numerator is Net Income.

### ROIC (using net income)
Return on Invested Capital where the numerator is Net Income.

### ROE (using EBITDA)
Return on Equity where the numerator is EBITDA.

### ROA (using EBITDA)
Return on Assets where the numerator is EBITDA.

### ROIC (using EBITDA)
Return on Invested Capital where the numerator is EBITDA.

### Current Ratio
Current Assets / Current Liabilities.

### Total Debt / Total Assets


