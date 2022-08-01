import easygui

input_var = easygui.ynbox('Please Select What You Would Like To Do', 'Title', ['Get Coinbase Data', 'Backtest'])

if input_var == 1:
    import GetCoinbaseData
    a = GetCoinbaseData
    a.GetCoinbaseData.create_csv()

else:
    import Backtester
    a=Backtester.Backtester
    a.calc_stats()