
############### Alpaca constants ###############

alpaca_endpoint = 'https://paper-api.alpaca.markets/v2/'

alpaca_paper_key = input('Enter Alpaca paper API key: ')
alpaca_paper_secret = input('Enter Alpaca paper secret: ')

# alpaca_paper_key = 'None'  # Uncomment for testing
# alpaca_paper_secret = 'None'  # Uncomment for testing

alpaca_headers = {'APCA-API-KEY-ID': alpaca_paper_key, 'APCA-API-SECRET-KEY': alpaca_paper_secret}


############### Finnhub constants ###############

finnhub_endpoint = 'https://finnhub.io/api/v1/'

finnhub_key = input('Enter Finnhub API key: ')

# finnhub_key = 'None'  # Uncomment for testing