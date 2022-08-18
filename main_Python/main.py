import PySimpleGUI as sg
import FetchCoinbaseData
import Backtester

sg.theme('DarkAmber')
layout = [[sg.Text('Please Choose What You Would Like To Do')],
            [sg.Button('Fetch Coinbase Data'), sg.Button('Backtest'), sg.Button('Cancel')]]

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
    elif event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()
