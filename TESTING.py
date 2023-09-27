import pandas as pd

from Intraday_Option_trading import *
enctocken = "K5HwKEAiavdCr1q0s4IUzRUgbIlw9mZ5mRs/LxlgMnkTTyhhwQTJLd6dEZmIvT5/BZpR7sdqaWrI1jKRhW0qCAm+YBO7DyE2XBiBxBdjxWnUPygu9938Xw=="

option = App(enctocken)
# option.taking_trade()

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1900)  # Adjust the width as needed

# pd.set_option('display.max_rows', None)
print(pd.DataFrame(option.kite.margins()))