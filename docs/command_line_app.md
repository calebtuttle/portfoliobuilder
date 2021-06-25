
## Commands
### account
List the information of the linked account. If no account is linked, an error message is printed.

### linkaccount <alpaca_api_key> <alpaca_secret>
Store the user's API key and secret for the current session. This allows the user to interact with their account (e.g., to place orders). Note: This command is unnecessary if you have already set the environment variables.

### newbasket (\<symbol0> \<symbol1> \<symboli>) <weighting_method> <basket_weight>
Create a new basket of stocks and stores it locally; this does not place any orders. Possible weighting methods are: market_cap, equal, and value. Basket weight must be greater than 0 and less than or equal to 100. 
Example: `newbasket (AAPL MSFT AMZN FB GOOGL) equal 10`

### newbasketfromindex <index_symbol> <weighting_method> <basket_weight>
Create a new basket of stocks from an index (e.g., the S&P500 (symbol: ^GSPC)). Calling this is identical to calling `newbasket` and replacing `<index_symbol>` with a list of the index's constituents.
Example: `newbasketfromindex ^GSPC equal 80`

### inspectbasket <basket_name>
List the basket's weighting method, weight, constituents, and whether it is active.

### addsymbols <basket_name> <symbol1> <symboli>
Add stocks to the designated basket. Only works if the basket is not active.

### buybasket <basket_name>
Buy each stock in the basket, and weight each one according to the weighting method of the basket. The total cost of the basket equals the basket weight multipled by the account equity (total cost = basket weight * equity). If there is not enough cash to cover the total cost, nothing in the basket is purchased. If the basket is already active, nothing will be done.

### sellbasket <basket_name>
Sell all shares of each stock in the basket. Note: this will cause unexpected behavior if multiple active baskets have overlapping holdings; when creating baskets, ensure each basket's stocks are unique to that basket, or reimplement some of this program.

### deletebasket <basket_name>
Sell the basket and delete it from the database.

### rebalance <basket_name>
Rebalance the basket according to its weighting method.

### listindices
Print a list of stock indices. Most of these will be supported by `newbasketfromindex`.

