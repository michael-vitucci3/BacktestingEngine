
input_var = input('enter 1 for fetching data and 2 for backtesting data')
import GetCoinbaseData
import Backtester

input_var = input('enter 1 for fetching data and 2 for backtesting data')

if input_var == 1:
    import GetCoinbaseData
    a = GetCoinbaseData
    a.GetCoinbaseData.create_csv()

else:
    import Backtester
    a=Backtester.Backtester
    a.calc_stats()