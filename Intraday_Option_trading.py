import pandas as pd
import time
from datetime import date
import datetime
from kite_trade import KiteApp
import os
import sys
from colorama import Fore, Style


class App:
    kite = None

    def __init__(self, enctoken):

        self.kite = KiteApp(enctoken)

    #  Strike selection for Call or Put options. Strike will be selected according to OTM or ITM or ATM
    #  provided by the user.
    def strike_of_ce_pe(self, instrument, ce_or_pe, a_o_i):
        df = pd.DataFrame(self.kite.instruments("NFO"))
        columns_to_drop = ['instrument_token', 'exchange_token', 'last_price', 'tick_size']
        df.drop(columns_to_drop, axis=1, inplace=True)
        df['expiry'] = pd.to_datetime(df['expiry'], format='%Y-%m-%d')
        name = None
        ltp_of_instrument = None
        if instrument[0] == "NSE:NIFTY FIN SERVICE":
            data = self.kite.ltp(["NSE:NIFTY FIN SERVICE"])
            ltp_of_instrument = data["NSE:NIFTY FIN SERVICE"]['last_price']
            name = "FINNIFTY"
        if instrument[0] == "NSE:NIFTY BANK":
            data = self.kite.ltp(["NSE:NIFTY BANK"])
            ltp_of_instrument = data["NSE:NIFTY BANK"]['last_price']
            name = "BANKNIFTY"
        if instrument[0] == "NSE:NIFTY 50":
            data = self.kite.ltp(["NSE:NIFTY 50"])
            ltp_of_instrument = data["NSE:NIFTY 50"]['last_price']
            name = "NIFTY"
        if instrument[0] == "NSE:NIFTY MID SELECT":
            data = self.kite.ltp(["NSE:NIFTY MID SELECT"])
            ltp_of_instrument = data["NSE:NIFTY MID SELECT"]['last_price']
            name = "MIDCPNIFTY"
        condition = None
        if a_o_i == 'OTM':
            if ce_or_pe == 'CE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'CE') & \
                            (df['exchange'] == 'NFO') & (instrument[2] < df['strike'] - ltp_of_instrument) & (
                                    df['strike'] - ltp_of_instrument <= 2 * instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))
            if ce_or_pe == 'PE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'PE') & \
                            (df['exchange'] == 'NFO') & (instrument[2] < ltp_of_instrument - df['strike']) & (
                                    ltp_of_instrument - df['strike'] <= 2 * instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))

        if a_o_i == 'ITM':
            if ce_or_pe == 'CE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'CE') & \
                            (df['exchange'] == 'NFO') & (0 < ltp_of_instrument - df['strike']) & (
                                    ltp_of_instrument - df['strike'] < instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))

            if ce_or_pe == 'PE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'PE') & \
                            (df['exchange'] == 'NFO') & (0 <= df['strike'] - ltp_of_instrument) & (
                                    df['strike'] - ltp_of_instrument < instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))
        if a_o_i == 'ATM':
            if ce_or_pe == 'CE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'CE') & \
                            (df['exchange'] == 'NFO') & (0 < df['strike'] - ltp_of_instrument) & (
                                    df['strike'] - ltp_of_instrument < instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))

            if ce_or_pe == 'PE':
                condition = (df['name'] == name) & (df["segment"] == 'NFO-OPT') & (df['instrument_type'] == 'PE') & \
                            (df['exchange'] == 'NFO') & (0 <= ltp_of_instrument - df['strike']) & (
                                    ltp_of_instrument - df['strike'] < instrument[2]) & \
                            (df['expiry'].dt.month == int(date.today().strftime("%m"))) & \
                            (df['expiry'].dt.day - int(date.today().strftime("%d")) < 7) & (
                                    0 <= df['expiry'].dt.day - int(date.today().strftime("%d")))

        df = df[condition]
        return df["tradingsymbol"].iloc[0]

    #  Taking trades
    def call_put_trade(self, instrument, lots, call_or_put, a_o_i, b_s, sl, target, v_l):
        #     getting the in the money (ITM) strike price from option chart
        entry_price = None
        exit_price = None
        print(f"You are doing {v_l} trading:")
        strike = self.strike_of_ce_pe(instrument, call_or_put, a_o_i)
        strike1 = strike
        trade = pd.DataFrame(columns=['spot_symbol', 'trade_symbol', 'Buy_Sell', 'Lots', 'trade_qty',
                                      "entry_price", "entry_time", "sl", 'exit_price', "exit_time", "pnl",
                                      "virtual_live"])

        print("Strike Price: ", strike)
        no_lots = lots
        selling_qty = no_lots * instrument[1]

        strike = f"NFO:{strike}"
        data = self.kite.ltp([strike])
        entry_price = data[strike]['last_price']
        #     to place buy order
        if v_l == "live":
            self.kite.place_order(variety=self.kite.VARIETY_REGULAR,
                                  exchange=self.kite.EXCHANGE_NFO,
                                  tradingsymbol=strike1,
                                  transaction_type=b_s,
                                  quantity=selling_qty,
                                  product=self.kite.PRODUCT_MIS,
                                  order_type=self.kite.ORDER_TYPE_MARKET,
                                  price=None,
                                  validity=None,
                                  disclosed_quantity=None,
                                  trigger_price=None,
                                  squareoff=None,
                                  stoploss=None,
                                  trailing_stoploss=None,
                                  tag=None)
            entry_price = self.kite.orders()["average_price"]

        if b_s == 'BUY':
            sl = min(sl, entry_price)
        if b_s == 'SELL':
            sl = sl
        target = target
        entry_time = str(datetime.datetime.now().time())[:8]
        if b_s == 'BUY':
            exit_price = abs(entry_price - sl)
        if b_s == 'SELL':
            exit_price = abs(entry_price + sl)

        print("Entry Price : ", round(entry_price, 2))
        print("Stop Loss : ", round(exit_price, 2))
        temp = entry_price
        pnl = None
        while True:
            data = self.kite.ltp([strike])
            ltp = data[strike]['last_price']
            if b_s == 'BUY':
                if ltp > temp + sl:
                    exit_price = round(temp, 2)
                    temp = temp + sl
                    print("Updated Stop Loss = ", exit_price)
                if ltp <= exit_price or (target != 0.0 and ltp >= (entry_price + sl * target)):
                    if v_l == "live":
                        self.kite.place_order(variety=self.kite.VARIETY_REGULAR,
                                              exchange=self.kite.EXCHANGE_NFO,
                                              tradingsymbol=strike1,
                                              transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                              quantity=selling_qty,
                                              product=self.kite.PRODUCT_MIS,
                                              order_type=self.kite.ORDER_TYPE_MARKET,
                                              price=None,
                                              validity=None,
                                              disclosed_quantity=None,
                                              trigger_price=None,
                                              squareoff=None,
                                              stoploss=None,
                                              trailing_stoploss=None,
                                              tag=None)

                        exit_price = self.kite.orders()["average_price"]
                    break
                if datetime.datetime.now().time() > datetime.time(15, 20, 10):
                    if v_l == "live":
                        self.kite.place_order(variety=self.kite.VARIETY_REGULAR,
                                              exchange=self.kite.EXCHANGE_NFO,
                                              tradingsymbol=strike1,
                                              transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                              quantity=selling_qty,
                                              product=self.kite.PRODUCT_MIS,
                                              order_type=self.kite.ORDER_TYPE_MARKET,
                                              price=None,
                                              validity=None,
                                              disclosed_quantity=None,
                                              trigger_price=None,
                                              squareoff=None,
                                              stoploss=None,
                                              trailing_stoploss=None,
                                              tag=None)
                        exit_price = self.kite.orders()["average_price"]

                    break
                pnl = (ltp - entry_price) * selling_qty
                pnl = round(pnl, 2)
                color = Fore.RED if pnl < 0 else Fore.GREEN
                sys.stdout.write(f"\r{color}P&L: {pnl} LTP: {ltp}{Style.RESET_ALL}")
                sys.stdout.flush()
            if b_s == 'SELL':
                if ltp < temp - sl:
                    exit_price = round(temp, 2)
                    temp = temp - sl
                    print("\n Updated Stop Loss = ", exit_price)
                if ltp >= exit_price or (target != 0.0 and ltp <= (entry_price - sl * target)) or ltp <= 1:
                    if v_l == "live":
                        self.kite.place_order(variety=self.kite.VARIETY_REGULAR,
                                              exchange=self.kite.EXCHANGE_NFO,
                                              tradingsymbol=strike1,
                                              transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                              quantity=selling_qty,
                                              product=self.kite.PRODUCT_MIS,
                                              order_type=self.kite.ORDER_TYPE_MARKET,
                                              price=None,
                                              validity=None,
                                              disclosed_quantity=None,
                                              trigger_price=None,
                                              squareoff=None,
                                              stoploss=None,
                                              trailing_stoploss=None,
                                              tag=None)
                        exit_price = self.kite.orders()["average_price"]
                    break
                if datetime.datetime.now().time() > datetime.time(15, 20, 10):
                    if v_l == "live":
                        self.kite.place_order(variety=self.kite.VARIETY_REGULAR,
                                              exchange=self.kite.EXCHANGE_NFO,
                                              tradingsymbol=strike1,
                                              transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                              quantity=selling_qty,
                                              product=self.kite.PRODUCT_MIS,
                                              order_type=self.kite.ORDER_TYPE_MARKET,
                                              price=None,
                                              validity=None,
                                              disclosed_quantity=None,
                                              trigger_price=None,
                                              squareoff=None,
                                              stoploss=None,
                                              trailing_stoploss=None,
                                              tag=None)
                        exit_price = self.kite.orders()["average_price"]
                    break
                pnl = (entry_price - ltp) * selling_qty
                pnl = round(pnl, 2)
                color = Fore.RED if pnl < 0 else Fore.GREEN
                sys.stdout.write(f"\r{color}P&L: {pnl} LTP: {ltp}{Style.RESET_ALL}")
                sys.stdout.flush()
        time.sleep(1)
        exit_time = str(datetime.datetime.now().time())[:8]
        trade_df = dict(spot_symbol=instrument[0], trade_symbol=strike1, Buy_Sell=b_s, Lots=lots, trade_qty=selling_qty,
                        entry_price=entry_price, entry_time=entry_time, sl=sl, exit_price=exit_price,
                        exit_time=exit_time, pnl=pnl, virtual_live=v_l)
        os.makedirs("Logs", exist_ok=True)
        csv_file_path = f"Logs/{datetime.datetime.now().date()}.csv"
        if os.path.exists(csv_file_path):
            existing_df = pd.read_csv(csv_file_path)
            existing_df = pd.concat([existing_df, pd.DataFrame({0: trade_df}).transpose()], ignore_index=True)
        else:
            existing_df = pd.concat([trade, pd.DataFrame({0: trade_df}).transpose()], ignore_index=True)
        existing_df.to_csv(csv_file_path, index=False)
        time.sleep(1)

    # take trade

    def taking_trade(self):
        instrument = {0: ["NSE:NIFTY FIN SERVICE", 40, 50], 1: ["NSE:NIFTY BANK", 15, 100], 2: ["NSE:NIFTY 50", 50, 50],
                      3: ["NSE:NIFTY MID SELECT", 75, 25]}
        ce_or_pe = {0: 'CE', 1: 'PE'}
        buy_sell = {0: 'BUY', 1: 'SELL'}
        atm_itm_otm = {0: 'ATM', 1: 'ITM', 2: 'OTM'}
        virtual_live = {0: "virtual", 1: "live"}
        print("Select one options instrument:")
        i = int(input(
            f"0: {instrument[0][0]}, 1: {instrument[1][0]}, 2: {instrument[2][0]}, 3: {instrument[3][0]}. You selected:  "))
        print("Select Call OR Put:")
        c_p = int(input(f"0: {ce_or_pe[0]}, 1: {ce_or_pe[1]}. You selected: "))
        print("Select ATM, ITM or OTM strike Price:")
        a_o_i = int(input(f"0: {atm_itm_otm[0]}, 1: {atm_itm_otm[1]}, 2: {atm_itm_otm[2]}. You selected: "))
        print("Want to buy or sell?")
        b_s = int(input(f"0: {buy_sell[0]}, 1: {buy_sell[1]}. You selected: "))
        no_of_lots = int(input("Provide number of lots: "))
        sl = float(input("Provide SL on Options price: "))
        target = float(input("Provide a number of you want to give target as multiple of sl. Otherwise enter 0: "))
        print("virtual or live trading?")
        v_l = int(input(f"0:{virtual_live[0]}, 1:{virtual_live[1]}. You selected: "))

        self.call_put_trade(instrument[i], no_of_lots, ce_or_pe[c_p], atm_itm_otm[a_o_i], buy_sell[b_s], sl, target,
                            virtual_live[v_l])