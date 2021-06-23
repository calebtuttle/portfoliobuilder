
## Commands
### account
Lists the information of the linked account. If no account is linked, an error message is printed.

### linkaccount <alpaca_api_key> <alpaca_secret>
Stores the user's API key and secret for the current session. This allows the user to interact with their account (e.g., to place orders).

### newbasket (\<symbol0> \<symbol1> \<symboli>) <weighting_method> <basket_weight>
Creates a new basket of stocks and stores it locally; does not place any orders. Possible weighting methods are: market_cap, equal, and value. Basket weight must be greater than 0 and less than or equal to 100. 

### newbasketfromindex <index_symbol> <weighting_method> <basket_weight>
Create a new basket of stocks from an index (e.g., the S&P500 (symbol: ^GSPC)). Calling this is identical to calling `newbasket` and replacing `<index_symbol>` with a list of the index's constituents.

### inspectbasket <basket_name>
List the basket's weighting method, weight, and constituents.

### listindices
Print a list of stock indices. Most of these will be supported by `newbasketfromindex`.

