
## Commands
### account
List the information of the linked account. If no account is linked, an error message is printed.

### linkaccount <alpaca_api_key> <alpaca_secret>
Store the user's API key and secret for the current session. This allows the user to interact with their account (e.g., to place orders).

### newbasket (\<symbol0> \<symbol1> \<symboli>) <weighting_method> <basket_weight>
Create a new basket of stocks and stores it locally; this does not place any orders. Possible weighting methods are: market_cap, equal, and value. Basket weight must be greater than 0 and less than or equal to 100. 

### newbasketfromindex <index_symbol> <weighting_method> <basket_weight>
Create a new basket of stocks from an index (e.g., the S&P500 (symbol: ^GSPC)). Calling this is identical to calling `newbasket` and replacing `<index_symbol>` with a list of the index's constituents.

### inspectbasket <basket_name>
List the basket's weighting method, weight, and constituents.

### buybasket <basket_name>
Buy each stock in the basket, and weight each one according to the weighting method of the basket. The total cost of the basket equals the basket weight multipled by the account equity (total cost = basket weight * equity). If there is not enough cash to cover the total cost, nothing in the basket is purchased.

### rebalance
Rebalance one's portfolio according to the weighting methods in the baskets that constitute one's portfolio.

### listindices
Print a list of stock indices. Most of these will be supported by `newbasketfromindex`.

