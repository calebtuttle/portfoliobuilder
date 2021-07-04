
## Commands
### inspectaccount
List the information of the linked Alpaca account. If no account is linked, an error message is printed.

### linkalpaca <alpaca_api_key> <alpaca_secret>
Store the user's Alpaca API key and secret for the current session. This allows the user to interact with their account (e.g., to place orders). Note: This command is unnecessary if you have already set the environment variables.

### newbasket <weighting_method> <basket_weight> (\<symbol0> \<symbol1> \<symboli>)
Create a new basket of stocks and stores it locally; this does not place any orders. Possible weighting methods are: market_cap, equal, value, and value_quality. Basket weight must be greater than 0 and less than or equal to 100. 
Example: `newbasket equal 10 (AAPL MSFT AMZN FB GOOGL)`

### newbasketfromindex <weighting_method> <basket_weight> <index_symbol>
Create a new basket of stocks from an index (e.g., the S&P500 (symbol: ^GSPC)). Calling this is identical to calling `newbasket` and replacing `<index_symbol>` with a list of the index's constituents.
Example: `newbasketfromindex equal 80 ^GSPC`

### listbaskets
Print the name of each basket in the database. 

### inspectbasket <basket_id>
List the basket's weighting method, weight, constituents, and whether it is active.

### addsymbols <basket_id> <symbol1> <symboli>
Add stocks to the designated basket. Only works if the basket is not active.
Example: `addsymbols Basket0 AAPL`

### buybasket <basket_id>
Buy each stock in the basket, and weight each one according to the weighting method of the basket. The total cost of the basket equals the basket weight multipled by the account equity (total cost = basket weight * equity). If there is not enough cash to cover the total cost, nothing in the basket is purchased. If the basket is already active, nothing will be done.

### sellbasket <basket_id>
Sell all shares of each stock in the basket. Note: this will cause unexpected behavior if multiple active baskets have overlapping holdings; when creating baskets, ensure each basket's stocks are unique to that basket, or reimplement some of this app.

### deletebasket <basket_id>
Sell the basket if it is active and delete it from the database.

### rebalance <basket_id>
Rebalance the basket according to its weighting method.

### listindices
Print a list of stock indices. Most of these will be supported by `newbasketfromindex`.

