# Portfolio Builder
Portfolio Builder is a tool for building a stock portfolio. It provides functions for weighting and rebalancing.

## Motivation
Many exchange traded funds (ETFs) are low-cost, but some charge non-negligable annual fees (fees above, say, 0.1%). While trying to build a diversified portfolio, I've encountered some ETFs which implement investment strategies that I feel are superior, but these ETFs often come with higher fees. 

(For example, an ETF with the ticker "RSP" provides exposure to S&P500 constituents, but instead of weighting the stocks by market capitalization (like the S&P500 does), it weights all constiteunts equally, giving more exposure to undervalued stocks and less to overvalued ones; unfortunately, its expense ratio is 0.2%, about 7 times Vanguard's VOO ETF which tracks the S&P500.)

I want the benefit of the investment strategies of higher-cost ETFs without the disadvantage of larger fees. So I created this program to copy and execute those strategies for free.

https://github.com/calebtuttle/portfoliobuilder.git