# Weighting Methods
This page gives an overview and example of each weighting method available in Portfolio Builder.

## Equal
Weight each stock in the basket equally. 

For example, assume we have a portfolio worth $1,000, and consider the following basket.

Basket0:\
    Weighting method: equal\
    Basket weight: 50%\
    Basket constituents: FB AAPL

When we purchase Basket0, we will purchase $250 of FB and $250 of AAPL, for a total of $500.

## Market Capitalization
Weight each stock in the basket proportionally to its weight in the total market capitalization of the basket (stock weight = stock market cap / basket market cap).

For example, assume we have a portfolio worth $1,000, and consider the following basket.

Basket0:\
    Weighting method: equal\
    Basket weight: 50%\
    Basket constituents: FB AAPL

For simplicity, let's assume AAPL's market cap is $2 trillion and FB's $1 trillion. The total market cap of the basket, then, is $3 trillion. AAPL accounts for 2/3 of the basket market cap, while FB accounts for 1/3 of it. When we purchase Basket0, we will purchase $333.33 of AAPL and $166.67 of FB for a total of $500.

## Value (naive)
Weight each stock according to its EV/FCF ratio. The lower a stock's EV/FCF ratio, the greater the weight.

Here is a more formal articulation. Let n be the number of stocks in the basket. Let i iterate from 0 to n. Let k iterate from n to 0. Let v be the sum of the EV/FCF values of all stocks in the basket. We sort the stocks according to EV/FCF such that higher a EV/FCF places the stock later in the list. We generate the weight of a stock with this formula:\
    weight of stock_i = (stock_n's EV/FCF) / v

For example, assume we have a portfolio worth $1,000 and are going to buy the following basket.

Basket0:\
    Weighting method: equal\
    Basket weight: 50%\
    Basket constituents: FB AAPL

As of writing AAPL's EV/FCF is 35.74 and FB's is 34.91, so we would allocate $247.06 to AAPL and $252.94 to FB.

## Value-Quality
Weight each stock according to both its valuation and its quality. Give stocks with lower valuations and higher quality more weight, stocks with higher valuations and lower quality less weight.

This weighting method is significantly more involved than the others. For detailed information, see the docs/measures.md page.