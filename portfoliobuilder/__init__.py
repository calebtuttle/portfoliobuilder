import os


############### Alpaca constants ###############

alpaca_endpoint = 'https://paper-api.alpaca.markets/v2/'

try:
    alpaca_paper_key = os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_KEY']
    alpaca_paper_secret = os.environ['PORTFOLIOBUILDER_ALPACA_PAPER_SECRET_KEY']
except KeyError:
    alpaca_paper_key = ''
    alpaca_paper_secret = ''
    print('Link Alpaca account with linkalpaca.')

alpaca_headers = {'APCA-API-KEY-ID': alpaca_paper_key, 'APCA-API-SECRET-KEY': alpaca_paper_secret}


############### Finnhub constants ###############

finnhub_endpoint = 'https://finnhub.io/api/v1/'

try:
    finnhub_key = os.environ['PORTFOLIOBUILDER_FINNHUB_KEY']
except KeyError:
    finnhub_key = ''
    print('Link Finnhub account with linkfinnhub.')


############### Polygon constants ###############

polygon_endpoint = 'https://api.polygon.io/v2/reference/'

try:
    polygon_key = os.environ['PORTFOLIOBUILDER_POLYGON_KEY']
except KeyError:
    polygon_key = ''
    print('Link Polygon account with linkpolygon.')
