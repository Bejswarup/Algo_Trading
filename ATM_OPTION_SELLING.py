import pandas as pd
import time
from datetime import date
import datetime
from kite_trade import *
import os
import copy

enctocken = "HvDnFYC+Qt8rPcLv4FZtdl/fswCbetTj2Pqc6ZCUOAZvm4C0Ws3izis9eb3ltpzFhzkVJFtds5KZGvVxfHk+hibVL4ZQXb8SScm5onxplvOc3np6qAmMuw=="

kite = KiteApp(enctoken = enctocken)

def scan_chart_data():

    print("Historical Thread Started")

    while True:

            data = kite.historical_data(instrument_token=list(spot_df_main.index) [0],
                                            interval="5minute",
                                            from_date= datetime.datetime.now().date()- datetime.timedelta(days=2),
                                            to_date = datetime.datetime.now())

#                     break
#                 except Exception as e:
#                     time.sleep(0.5)
            df=pd.DataFrame(data)
            df["only_date"] = df["date"].apply(lambda x: x.date())
            df=df.set_index("date")

            df["EMA"] = df["close"].ewm(span=5, adjust=False).mean()
            df = df[df["only_date"]==datetime.datetime.now().date()]
            df = df[:-1]

            if len(df)!=0:
                if list(df["low"]) [-1] > list(df ["EMA"])[-1]:
                    return True
                else:
                    return False


def ATM_strick_of_CE_PE(instrument, limit, ce_or_pe):
    df = pd.DataFrame(kite.instruments("NFO"))
    columns_to_drop = ['instrument_token', 'exchange_token', 'last_price', 'tick_size']
    df.drop(columns_to_drop, axis=1, inplace=True)
    df['expiry'] = pd.to_datetime(df['expiry'], format='%Y-%m-%d')
    if instrument == "NSE:NIFTY FIN SERVICE":
        data = kite.ltp(["NSE:NIFTY FIN SERVICE"])
        ltp_of_instrument = data["NSE:NIFTY FIN SERVICE"]['last_price']
        name = "FINNIFTY"
    if instrument == "NSE:NIFTY BANK":
        data = kite.ltp(["NSE:NIFTY BANK"])
        ltp_of_instrument = data["NSE:NIFTY BANK"]['last_price']
        name = "BANKNIFTY"
    if instrument == "NSE:NIFTY 50":
        data = kite.ltp(["NSE:NIFTY 50"])
        ltp_of_instrument = data["NSE:NIFTY 50"]['last_price']
        name = "NIFTY"
    if instrument == "NSE:NIFTY MID SELECT":
        data = kite.ltp(["NSE:NIFTY MID SELECT"])
        ltp_of_instrument = data["NSE:NIFTY MID SELECT"]['last_price']
        name = "MIDCPNIFTY"
    pd.set_option('display.max_columns', None)
    if ce_or_pe == 'CE':
        condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'CE') & \
                    (df['exchange'] == 'NFO') & (0 < df['strike'] - ltp_of_instrument) & (
                                df['strike'] - ltp_of_instrument < limit) & \
                    (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                    (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))
        df = df[condition]
    if ce_or_pe == 'PE':
        condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'PE') & \
                    (df['exchange'] == 'NFO') & (0 < ltp_of_instrument - df['strike']) & (
                                ltp_of_instrument - df['strike'] < limit) & \
                    (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                    (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))
        df = df[condition]
    return df["tradingsymbol"].iloc[0]


def Call_Put_Sell(instrument, lots, qty_per_lot, limit, call_or_put, k):
    #     while scan_chart_data is not True:
    #         time.sleep(10)
    strike = ATM_strick_of_CE_PE(instrument, limit, call_or_put)
    strike1 = strike
    trade = pd.DataFrame(columns=['spot_symbol', 'trade_symbol', 'trade_direction', 'Lots', 'trade_qty',
                                  "entry_price", "entry_time", "sl", 'exit_price' "exit_time", "pnl"])

    print("Strike Price: ", strike)
    no_lots = lots
    selling_qty = no_lots * qty_per_lot

    strike = f"NFO:{strike}"
    data = kite.ltp([strike])
    #     to place live order

    # kite.place_order(variety=kite.VARIETY_REGULAR,
    #                  exchange=kite.EXCHANGE_NFO,
    #                  tradingsymbol=strike1,
    #                  transaction_type=kite.TRANSACTION_TYPE_SELL,
    #                  quantity=selling_qty,
    #                  product=kite.PRODUCT_MIS,
    #                  order_type=kite.ORDER_TYPE_MARKET,
    #                  price=None,
    #                  validity=None,
    #                  disclosed_quantity=None,
    #                  trigger_price=None,
    #                  squareoff=None,
    #                  stoploss=None,
    #                  trailing_stoploss=None,
    #                  tag=None)

    entry_price = data[strike]['last_price']
    sl = k
    trade_df = {'spot_symbol': instrument, 'trade_symbol': strike1, 'trade_direction': 'SELL', 'Lots': lots,
                'trade_qty': selling_qty, "entry_price": entry_price, "entry_time": None, "sl": sl, 'exit_price': None,
                "exit_time": None, "pnl": None}
    trade_df['entry_time'] = datetime.datetime.now().time()
    exit_price = entry_price + sl
    print("Entry Price : ", round(entry_price, 2))
    print("Stop Loss : ", round(exit_price, 2))
    temp = entry_price
    while True:
        data = kite.ltp([strike])
        ltp = data[strike]['last_price']

        if ltp < temp - sl:
            exit_price = round(temp, 2)
            temp = temp - sl
            print("Updated Stop Loss = ", exit_price)
        if ltp >= exit_price:
            # kite.place_order(variety=kite.VARIETY_REGULAR,
            #                  exchange=kite.EXCHANGE_NFO,
            #                  tradingsymbol=strike1,
            #                  transaction_type=kite.TRANSACTION_TYPE_BUY,
            #                  quantity=selling_qty,
            #                  product=kite.PRODUCT_MIS,
            #                  order_type=kite.ORDER_TYPE_MARKET,
            #                  price=None,
            #                  validity=None,
            #                  disclosed_quantity=None,
            #                  trigger_price=None,
            #                  squareoff=None,
            #                  stoploss=None,
            #                  trailing_stoploss=None,
            #                  tag=None)
            trade_df['exit_price'] = exit_price
            trade_df['exit_time'] = datetime.datetime.now().time()
            pnl = (entry_price - exit_price) * selling_qty
            pnl = round(pnl, 2)
            trade_df['pnl'] = pnl
            print("PNL = ", pnl)
            break
        if datetime.datetime.now().time() > datetime.time(15, 20, 10):
            # kite.place_order(variety=kite.VARIETY_REGULAR,
            #                  exchange=kite.EXCHANGE_NFO,
            #                  tradingsymbol=strike1,
            #                  transaction_type=kite.TRANSACTION_TYPE_BUY,
            #                  quantity=selling_qty,
            #                  product=kite.PRODUCT_MIS,
            #                  order_type=kite.ORDER_TYPE_MARKET,
            #                  price=None,
            #                  validity=None,
            #                  disclosed_quantity=None,
            #                  trigger_price=None,
            #                  squareoff=None,
            #                  stoploss=None,
            #                  trailing_stoploss=None,
            #                  tag=None)
            trade_df['exit_price'] = exit_price
            trade_df['exit_time'] = datetime.datetime.now().time()
            pnl = (entry_price - ltp) * selling_qty
            pnl = round(pnl, 2)
            trade_df['pnl'] = pnl
            print("PNL = ", pnl)
            break

    os.makedirs("Logs", exist_ok=True)
    csv_file_path = f"Logs/{datetime.datetime.now().date()}.csv"
    if os.path.exists(csv_file_path):
        existing_df = pd.read_csv(csv_file_path)
        existing_df = pd.concat([existing_df, pd.DataFrame({0: trade_df}).transpose()], ignore_index=True)
    else:
        existing_df = pd.concat([trade, pd.DataFrame({0: trade_df}).transpose()], ignore_index=True)
    existing_df.to_csv(csv_file_path, index=False)
    time.sleep(1)