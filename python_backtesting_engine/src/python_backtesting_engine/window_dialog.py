# window_dialog.py

def window_dialog():

    import easygui
    from python_backtesting_engine.Coinbase_Fetcher import FetchCoinbaseData
    from python_backtesting_engine.Backtesting import Backtester
    from python_backtesting_engine.Brownian_Motion import BrownianMotion

    reply = ""
    while reply != "end":
        msg = "Please select what you would like to do:"
        choices = ["Backtest", "Fetch Coinbase Data", "Generate Brownian Data", "end"]
        reply = easygui.choicebox(msg=msg, choices=choices)

        if reply == 'Backtest':
            a = Backtester
            a.Backtester().calc_stats()
        elif reply == 'Fetch Coinbase Data':
            a = FetchCoinbaseData
            a.FetchCoinbaseData().create_csv()
        elif reply == 'Generate Brownian Data':
            a = BrownianMotion
            a.BrownianMotion().save_csv()
        elif reply == 'end':
            exit()
