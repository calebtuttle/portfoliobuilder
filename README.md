# Portfolio Builder
Portfolio Builder is a tool for creating and maintaining a diversified stock portfolio.

It allows users to buy _baskets_ of stocks. The user constructs a basket which is stored on their computer. Once constructed, a basket can be purchased. A user's portfolio can consist of multiple baskets. 

This ability to quickly buy a basket of stocks gives an investor the ability to construct, with no fees, a portfolio that is as diversified as one consisting of equity-comprised ETFs, and it gives the investor more weighting strategies than ETFs provide.

Note: The Portfolio Builder documentation assumes a basic understanding of the stock market and portfolio weighting strategies. See [introductory readings](#Introductory-readings) to get a sense of the investing vocabulary used in this documentation.

## Motivation
There are two primary motivations for this project: reducing fees and reclaiming ownership of the stocks in my portfolio.

The institutions that collectively manage $26 trillion of assets earn over $11 billion per year in fees ([$26 trillion AUM](https://www.cnbc.com/2020/11/17/us-etf-market-tops-5-trillion-in-assets-as-investors-stampede-into-stocks-on-vaccine-hopes.html) x [0.45% expense ratio](https://newsroom.morningstar.com/newsroom/news-archive/press-release-details/2020/Morningstars-Annual-Fund-Fee-Study-Finds-Investors-Saved-Nearly-6-Billion-in-Fund-Fees-in-2019/default.aspx) ~= $11 billion). A portion of those fees are used to manage index funds which are entirely automated. With the ability to automate trades, purchase fractional shares, and pay zero commissions, an investor can copy these index funds without paying the fees.

Additionally, the popularity of index funds has resulted in the concentration of voting power. The top three mutual fund firms cast about 25% of the shareholder votes for companies in the S&P500. Such a high level of concentrated power is not good for competition in markets. I encourage anyone intrigued to see [this article by Annie Lowrey](https://www.theatlantic.com/ideas/archive/2021/04/the-autopilot-economy/618497/). Portfolio Builder allows an investor to purchase shares of companies directly; an investor therefore retains his or her voting power.

## Requirements
- Python 3.7.6
- API keys for the following APIs:
    - [Alpaca](https://alpaca.markets) 
    - [Finnhub](https://finnhub.io)
    - [Polygon](https://polygon.io)

See [A note on the API keys](#A-note-on-the-API-keys) to see what the API keys are used for.

## Installation
1. Clone this GitHub repository.

        git clone https://github.com/calebtuttle/portfoliobuilder.git
        
2. Navigate into the cloned directory.

        cd portfoliobuilder

3. Install dependencies. 

    Install with conda.

        conda install --file requirements.txt

    Or install pip.

        pip install -r requirements.txt

4. While still in the outermost portfoliobuilder/ directory, run setup.py.

        python setup.py develop

    This allows modules in portfoliobuilder import one another, and it allows you to import portfoliobuilder to your python modules.

5. Set the following environment variables for your: 
- Alpaca API key for paper trading
- Alpaca secret key for paper trading
- Finnhub API key 
- Polygon key

        PORTFOLIOBUILDER_ALPACA_PAPER_KEY
        PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY
        PORTFOLIOBUILDER_FINNHUB_KEY
        PORTFOLIOBUILDER_POLYGON_KEY

    There are a couple ways to set these environment variables.

    (a) You can set the environment variables with your _virtual environment_. If you are using conda, you can find instructions for setting environment variables [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables).

    (b) You can set the environment variables every time you run Portfolio Builder using the [`link` commands](docs/commands.md#linkalpaca-alpaca_api_key-alpaca_secret).

## Quickstart
The following demonstrates how to construct, inspect, and purchase a basket of stocks. 

To run Portfolio Builder, execute the run.py script within portfoliobuilder/portfoliobuilder:

    python run.py

You should be presented with a short welcome message and prompt:

    Welcome to the portfoliobuilder command line application. Enter
    'help' to see commands. Enter 'q' to quit, or kill with CTRL+C.
    > 

For this example, we will buy all the stocks in the S&P500, but instead of weighting those stocks by market cap (like the S&P500 does), we will weight them equally. First, we create a basket from an index:

    > newbasketfromindex equal 50 ^GSPC

This command says, "Construct a basket of all the stocks in the _^GSPC_ index (which is the symbol for the S&P500). When I buy this basket, I want those stocks to be weighted _equally_. And when I buy the basket, I want to allocate exactly _50%_ of my portfolio to it." After Portfolio Builder ensures all stocks in the S&P500 can be traded through Alpaca, you should get an output that looks like this:

    Basket1 created.

We can double check that the basket was created with `inspectbasket` (I'm omitting the entire list of basket constituents here).

    > inspectbasket 1
    Inspecting Basket1...
    Basket weighting method: equal
    Basket weight: 50.0%
    Basket is active: False
    Basket constituents: SBAC CVX PVH SWKS ...

Now we buy the basket:

    > buybasket Basket1
    Orders to purchase stocks in Basket1 have been placed.
    Weighting method: equal
    Basket weight: 50.0%
    Note: Some purchase orders might not have been placed. If no errors
    were printed above, all stocks were placed successfully.

If all of the above ran without errors or exceptions, you successfully purchased the ~500 stocks in the S&P500 and weighted them equally. For a full list of commands and their descriptions, see the [commands page](docs/commands.md).

## Contribute
I welcome all contributions! Feel free to report bugs, address bugs, add commands/features, and improve the documentation. See the [contributing page](contributing.md) for more info.

## A note on the API keys
All of the APIs used by Portfolio Builder are free or have a free tier. Portfolio Builder requires no API subscriptions.

What are the API keys for? The two Alpaca keys are used to trade stocks within your Alpaca account. The Alpaca API keys are the only strictly necessary ones for this application; if you do not connect to the other APIs, however, the 'equal' weighting method will be the only weighting method available. Note that each Alpaca account comes with two sub-accounts: a paper account and a live account. The paper account uses fake money to simulate buying and selling of stocks; this let's you test programmatic trading. The live account uses real money, and you can only trade within it once you've funded it. I discourage anyone from using Portfolio Builder with their live account until the app has been sufficiently tested.

The Finnhub and Polygon API keys are used to collect stock data (e.g., market capitalizations and P/E ratios). This data is used by the weighting methods other than the 'equal' weighting method.

## Introductory readings
The Portfolio Builder documentation assumes a basic familiarity with investing concepts. The following resources introduce you to the investing concepts used in the Portfolio Builder documentation. (For the purposes of this documentation, these resources are meant to be skimmed. You do not need to study these to understand the documentation.)
- [Wikipedia article on stock market indices](https://en.wikipedia.org/wiki/Stock_market_index)
- [Wikipedia article on ETFs](https://en.wikipedia.org/wiki/Exchange-traded_fund)
