# window_dialog.py

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def b1_clicked():
    data_file = QtWidgets.QFileDialog.getOpenFileName(caption="Choose Data:",
                                                      directory="./src/python_backtesting_engine/data")
    print(data_file)
    from python_backtesting_engine.Backtesting import Backtester

    a = Backtester
    a.Backtester(data_file).calc_stats()


def b2_clicked():
    from python_backtesting_engine.Coinbase_Fetcher import FetchCoinbaseData

    a = FetchCoinbaseData
    a.FetchCoinbaseData().create_csv()


def b3_clicked():
    from python_backtesting_engine.Brownian_Motion import BrownianMotion

    a = BrownianMotion
    a.BrownianMotion().save_csv()


def window_dialog():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Please choose what you would like to do:")

    b1 = QtWidgets.QPushButton(win)
    b1.setText("Backtest")
    b1.setGeometry(50, 50, 200, 50)

    b2 = QtWidgets.QPushButton(win)
    b2.setText("Fetch Coinbase Data")
    b2.setGeometry(50, 150, 200, 50)

    b3 = QtWidgets.QPushButton(win)
    b3.setText("Generate Brownian Motion")
    b3.setGeometry(50, 250, 200, 50)
    b1.clicked.connect(b1_clicked)
    b2.clicked.connect(b2_clicked)
    b3.clicked.connect(b3_clicked)

    win.show()
    sys.exit(app.exec_())


window_dialog()
