'''
Unit tests.
'''

from portfoliobuilder import api_utils


def test_api_utils_get_account():
    acc = api_utils.get_account()
    print(acc)
    
def test_api_utils_fractionable_tradable():
    f_and_t_true = api_utils.fractionable_tradable('AAPL')
    f_and_t_false = api_utils.fractionable_tradable('NOTASYMBOL')
    assert f_and_t_true
    assert not f_and_t_false

# api_utils.place_order works

def test_api_utils_get_market_cap():
    market_cap_aapl = api_utils.get_market_cap('AAPL')
    market_cap_fake_stock = api_utils.get_market_cap('NOTASYMBOL')
    
    assert isinstance(market_cap_aapl, float)
    assert isinstance(market_cap_fake_stock, None)

def test_api_utils_get_metrics():
    metrics_aapl = api_utils.get_metrics('AAPL')
    metrics_fake_stock = api_utils.get_metrics('NOTASYMBOL')

    assert isinstance(metrics_aapl, dict)
    assert metrics_fake_stock is None

def test_api_utils_get_ev_to_fcf():
    ev_to_fcf_aapl = api_utils.get_ev_to_fcf('AAPL')
    ev_to_fcf_fake_stock = api_utils.get_ev_to_fcf('NOTASYMBOL')

    assert isinstance(ev_to_fcf_aapl, float)
    assert ev_to_fcf_fake_stock is None

