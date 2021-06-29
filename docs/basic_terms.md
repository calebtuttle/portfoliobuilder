# Basic Terms
This page clarifies the basic terms used by Portfolio Builder.

### Basket
A basket is simply a collection of stocks (it also includes weighting information). It is an abstraction unique to Portfolio Builder; by this I mean, neither Alpaca nor any other broker will give you the option to buy a Basket of stocks. A Basket is not a product. It is a data structure.

You might read in the documentation something like, "Let's _create_ a basket of stocks." When you create a basket, you are simply recording information on your harddrive. Portfolio Builder uses this information when you eventually _buy_ a basket.

What does it mean to "buy a basket"? When you buy a basket, you purchase all the stocks listed in the basket. The weighting information in the basket is used to determine _how much_ of each stock to buy. 

### Weighting Method
A basket's weighting method is used to determine the weight of each stock in a basket when the basket is purchased. This is an important part of Portfolio Builder because it allows for the duplication of ETF strategies with minimal effort. See the [Weighting Methods](docs/weighting_methods.md) page for more detail.

### Basket Weight
The basket weight answers the question: How much of my portfolio will I allocate to this basket? This allows for efficient portfolio management. For example, an investor might allocate 60% of their portfolio to S&P500 stocks, 10% to Dow Jones Industrial Average stocks, and 30% to tech stocks. The basket weight attribute allows an investor to execute such strategies without wasting time with a calculator and a spreadsheet.
