def window_dialog():

    import PySimpleGUI as sg

    from Coinbase_Fetcher import FetchCoinbaseData
    from Backtesting import Backtester
    from Brownian_Motion import brownian_motion

    sg.theme('DarkAmber')
    layout = [[sg.Text('Please Choose What You Would Like To Do')],
              [sg.Button('Fetch Coinbase Data'), sg.Button('Backtest'),
               sg.Button('Fetch Geometric Brownian Motion Data'),
               sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('BacktestingEngine.v2', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == 'Fetch Coinbase Data':
            a = FetchCoinbaseData
            a.FetchCoinbaseData().create_csv()
        elif event == 'Backtest':
            a = Backtester
            a.Backtester().calc_stats()
        elif event == 'Fetch Geometric Brownian Motion Data':
            a = brownian_motion.BrownianMotion().save_csv()
        elif event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        elif event is not None:
            print("Invalid Input")
            break

    window.close()
    exit()
