# Portfolio Builder
Portfolio Builder is a tool for creating and maintaining a diversified stock portfolio.

## Overview
There are two basic ideas behind Portfolio Builder: Basket-based investing is superior to stock picking, and the current options for basket-based investing are insufficient. Portfolio Builder allows an investor to easily buy a basket of stocks and gives the investor a few options with respect to weighting those stocks. This ability to quickly buy a basket of stocks gives an investor the ability to construct a portfolio that is as diversified as one consisting of ETFs, and with Portfolio Builder, there are no annual fees. 

I want the benefit of the passive investment strategies of ETFs without the disadvantage of fees. I created this app with the goal of copying and executing those strategies for free.

## Background
As of November 2020, the exchange traded fund (ETF) market is about $5 trillion, and the mutual fund market is about $21 trillion ([source](https://www.cnbc.com/2020/11/17/us-etf-market-tops-5-trillion-in-assets-as-investors-stampede-into-stocks-on-vaccine-hopes.html)). The average expense ratio for a fund in 2019 was 0.45% ([source](https://newsroom.morningstar.com/newsroom/news-archive/press-release-details/2020/Morningstars-Annual-Fund-Fee-Study-Finds-Investors-Saved-Nearly-6-Billion-in-Fund-Fees-in-2019/default.aspx)). Thus, the institutions that collectively manage $26 trillion of assets earn over $11 billion per year in fees.

With the ability to automate trades and purchase fractional shares, an investor can copy these ETFs without paying the fees.

Additionally, the size of the companies that manage these funds is concerning. I encourage anyone intrigued to see [this article by Annie Lowrey](https://www.theatlantic.com/ideas/archive/2021/04/the-autopilot-economy/618497/). 

## Requirements
Python 3.6.8

An Alpaca account, a Finnhub account, a polygon account, and API keys for each. You can create an Alpaca account [here](https://alpaca.markets), a Finnhub account [here](https://finnhub.io), and a Polygon account [here](https://polygon.io). See [A Note on the API Keys](#A-Note-on-the-API-Keys) for more info.

## Installation
1. Clone this GitHub repository, and navigate to the outermost portfoliobuilder/ directory.

2. Run setup.py in the outermost portfoliobuilder/ directory:

        portfoliobuilder$ python setup.py develop

    This allows you to import portfoliobuilder.

3. Set the following environment variables to your Alpaca API key for paper trading, your Alpaca secret key for paper trading, your Finnhub API key, and your Polygon key, respectively:

        PORTFOLIOBUILDER_ALPACA_PAPER_KEY
        PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY
        PORTFOLIOBUILDER_FINNHUB_KEY
        PORTFOLIOBUILDER_POLYGON_KEY

    If you are using conda, you can find instructions for setting environment variables [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables).

## Quickstart
The following demonstrates how to construct, inspect, and purchase a basket of stocks. 

To run Portfolio Builder, run the command_line_app script with:

    portfoliobuilder/portfoliobuilder$ python command_line_app.py

You should be presented with a short welcome message and prompt:

    Welcome to the portfoliobuilder command line application. Enter
    'help' to see commands. Enter 'q' to quit, or kill with ^c.
    > 

For this example, we will buy all the stocks in the S&P500, but instead of weighting those stocks by market cap (like the S&P500 does), we will weight them equally. First, we create a basket from an index:

    > newbasketfromindex ^GSPC equal 50

This command says, "Construct a basket of all the stocks in the _^GSPC_ index (which is the symbol for the S&P500). When I buy this basket, I want those stocks to be weighted _equally_. And when I buy the basket, I want to allocate exactly _50%_ of my portfolio to it." After Portfolio Builder ensures all stocks in the S&P500 can be traded through Alpaca, you should get an output that looks like this:

    Basket0 created.

We can double check that the basket was created with `inspectbasket` (I'm omitting the entire list of basket constituents here).

    > inspectbasket Basket0
    Inspecting Basket0...
    Basket weighting method: equal
    Basket weight: 50.0%
    Basket is active: False
    Basket constituents: SBAC CVX PVH SWKS ...

Now we buy the basket:

    > buybasket Basket0
    Orders to purchase stocks in Basket0 have been placed.
    Weighting method: equal.
    Basket weight: 50.0%.
    Note: Some purchase orders might not have been placed. If no errors
    were printed above, all stocks were placed successfully.

If all of the above ran without errors or exceptions, you successfully purchased the ~500 stocks in the S&P500 and weighted them equally. For further information, see the command line app documentation.

## A Note on the API Keys
What are the API keys for? The two Alpaca keys are used to trade stocks within your Alpaca account. The Alpaca API keys are the only strictly necessary ones for this application; if you do not connect to the other APIs, however, the 'equal' weighting method will be the only weighting method available. Note that each Alpaca account comes with two sub-accounts: a paper account and a live account. The paper account uses fake money to simulate buying and selling of stocks; this let's you test programmatic trading. The live account uses real money, and you can only trade within it once you've funded it. I discourage anyone from using Portfolio Builder with their live account until the app has been sufficiently tested.

The Finnhub and Polygon API keys are used to collect stock data (e.g., market capitalizations and P/E ratios). This data is used by the weighting methods other than the 'equal' weighting method.