# Portfolio Builder
Portfolio Builder is a tool for building a stock portfolio. It provides functions for weighting and rebalancing.

## Motivation
I want the benefit of the passive investment strategies of ETFs without the disadvantage of fees. I created this program with the goal of copying and executing those strategies for free.

## Background
As of November 2020, the exchange traded fund (ETF) market is about $5 trillion, and the mutual fund market is about $21 trillion (source: https://www.cnbc.com/2020/11/17/us-etf-market-tops-5-trillion-in-assets-as-investors-stampede-into-stocks-on-vaccine-hopes.html). The average expense ratio for a fund in 2019 was 0.45% (source: https://newsroom.morningstar.com/newsroom/news-archive/press-release-details/2020/Morningstars-Annual-Fund-Fee-Study-Finds-Investors-Saved-Nearly-6-Billion-in-Fund-Fees-in-2019/default.aspx). Thus, the institutions that collectively manage $26 trillion of assets earn over $11 billion per year in fees.

With the ability to automate trades and purchase fractional shares, an investor can copy these ETFs without paying the fees. Let's get rid of unnecessary fees.

Additionally, the size of the companies that manage these funds is concerning. I encourage anyone intrigued to see this article by Annie Lowrey: https://www.theatlantic.com/ideas/archive/2021/04/the-autopilot-economy/618497/. 

## Requirements
Python 3.7.6

An Alpaca account, a Finnhub account, and API keys for each. You can create an Alpaca account here: https://alpaca.markets; and a Finnhub account here: https://finnhub.io. 

## Installation
1. Clone this GitHub repository, and navigate to the outermost portfoliobuilder/ directory.

2. Run setup.py in the outermost portfoliobuilder/ directory:

        portfoliobuilder$ python setup.py develop

    This allows you to import portfoliobuilder.

3. Set the following environment variables:

        PORTFOLIOBUILDER_ALPACA_PAPER_KEY
        PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY
        PORTFOLIOBUILDER_FINNHUB_KEY

    These are the API keys that will allow communication with Alpaca and Finnhub. If you are using conda, you can find instructions for setting environment variables here: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables.