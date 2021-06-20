import os


############### Alpaca constants ###############

alpaca_endpoint = 'https://paper-api.alpaca.markets/v2/'

alpaca_paper_key = os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_KEY']
alpaca_paper_secret = os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY']

alpaca_headers = {'APCA-API-KEY-ID': alpaca_paper_key, 'APCA-API-SECRET-KEY': alpaca_paper_secret}


############### Finnhub constants ###############

finnhub_endpoint = 'https://finnhub.io/api/v1/'

finnhub_key = os.environ['PORTFOLIOBUILDER_FINNHUB_KEY']
