

# # First Way to Login
# # You can use your Kite app in mobile
# # But You can't login anywhere in 'kite.zerodha.com' website else this session will disconnected

# user_id = "RPD374"       # Login Id
# password = "Swarup@1997"      # Login password
# twofa = "263645"         # Login Pin or TOTP
#
# enctoken = get_enctoken(user_id, password, twofa)
# kite = KiteApp(enctoken=enctoken)

# # Second way is provide 'enctoken' manually from 'kite.zerodha.com' website
# # Than you can use login window of 'kite.zerodha.com' website Just don't logout from that window
# # # Process shared on YouTube 'TradeViaPython'

# enctocken = "06wjyd9zhjcNozdF5GXNNQH8Cgcid91ZhXng794A4bTcHu4z2YPjrDOZy0hJIrSb6X65AtUw1cZ2EhffNd3/T22LinFf8SAkELDWJ3jeb+PWFBuRuhTZGw=="
# api_key = "your api key"
# kite = KiteConnect(api_key=api_key)
from kite_trade import *
enctocken = "HvDnFYC+Qt8rPcLv4FZtdl/fswCbetTj2Pqc6ZCUOAZvm4C0Ws3izis9eb3ltpzFhzkVJFtds5KZGvVxfHk+hibVL4ZQXb8SScm5onxplvOc3np6qAmMuw=="

kite = KiteApp(enctoken = enctocken)
import pandas as pd
# Get Historical Data
# import datetime
# instrument_token = 408065
# from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
# to_datetime = datetime.datetime.now()
# interval = "5minute"
# print(kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False))
tradingsymbol = "FINNIFTY23SEP19800CE"
pd.set_option('display.max_columns', None)
print(pd.DataFrame(kite.orders()))
# # Place Order
# order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=kite.EXCHANGE_NFO,
#                          tradingsymbol=tradingsymbol,
#                          transaction_type=kite.TRANSACTION_TYPE_SELL,
#                          quantity=40,
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=None,
#                          validity=None,
#                          disclosed_quantity=None,
#                          trigger_price=None,
#                          squareoff=None,
#                          stoploss=None,
#                          trailing_stoploss=None,
#                          tag="TradeViaPython")
#
# print(order)

