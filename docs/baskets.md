# Baskets
The central construct in Portfolio Builder is the _basket_. Users create baskets, buy baskets, sell baskets, inspect baskets, and modify baskets. 

What is a basket? A basket is a data structure that contains both a collection of stock symbols and information regarding how to weight those stocks in a portfolio. There are three core components of a basket:
- [Constituents](#constituents).
- [Weighting method](#weighting-method).
- [The basket's weight](#basket-weight).

### Constituents
A basket's constituents are the stocks within the basket. When a user "buys a basket," they are buying the basket's constituents. When they "sell a basket," they are selling the basket's constituents. And so on. When creating a basket, a user can specify the basket's constituents; they can also copy the constituents of a stock index, such as the S&P500.

### Weighting Method
A basket's weighting method answers the question, _how much_ of each stock in this basket should I buy? The weighting method is used to determine the weight of each stock in a basket when the basket is purchased and rebalanced. This is an important part of Portfolio Builder because it allows for the duplication of index fund strategies with minimal effort. See the [Weighting Methods](docs/weighting_methods.md) page for more detail.

### Basket Weight
The basket weight answers the question: How much of my portfolio will I allocate to this basket? This allows for efficient portfolio management. For example, an investor might allocate 60% of their portfolio to S&P500 stocks and 40% to Dow Jones Industrial Average stocks by purchasing two baskets, one with a weight of 60% and the other with a weight of 40%. The basket weight attribute allows an investor to execute such strategies without wasting time with a calculator and a spreadsheet.
