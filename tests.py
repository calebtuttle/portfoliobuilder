'''
Unit tests.
'''

from portfoliobuilder import api_utils



################# api_utils Alpaca tests #################

def test_api_utils_get_account():
    acc = api_utils.get_account()
    assert acc['currency'] == 'USD'

def test_api_utils_get_asset():
    asset = api_utils.get_asset('AAPL')
    assert asset['symbol'] == 'AAPL'

# place_order() works

def test_api_utils_get_position():
    position = api_utils.get_position('AAPL')
    assert position['symbol'] == 'AAPL'
    assert  position['exchange'] == 'NASDAQ'

# close_position() works


################# api_utils Finnhub tests #################


def test_api_utils_get_profil2():
    profile = api_utils.get_profile2('AAPL')
    assert profile['country'] == 'US'
    assert profile['currency'] == 'USD'

def test_api_utils_get_metrics():
    metrics = api_utils.get_metrics('AAPL')
    assert metrics['symbol'] == 'AAPL'
    assert isinstance(metrics['metric'], dict)

def test_api_utils_get_financials_as_reported():
    fins = api_utils.get_financials_as_reported('AAPL')
    assert fins['symbol'] == 'AAPL'
    assert isinstance(fins['data'], list)

def test_api_utils_get_index_constituents():
    indx_constituents = api_utils.get_index_constituents('^GSPC')
    assert indx_constituents['symbol'] == '^GSPC'


################# api_utils Polygon tests #################

def test_api_utils_get_financials():
    fins = api_utils.get_financials('AAPL')
    assert 'status' in fins.keys()
    assert 'results' in fins.keys()
    assert len(fins.keys()) == 2




def run_tests():
    test_api_utils_get_account()
    test_api_utils_get_asset()
    test_api_utils_get_position()
    test_api_utils_get_profil2()
    test_api_utils_get_metrics()
    test_api_utils_get_financials_as_reported()
    test_api_utils_get_index_constituents()
    test_api_utils_get_financials()

    print('Tests ran successfully')

run_tests()