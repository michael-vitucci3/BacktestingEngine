import pandas as pd
from matplotlib.pylab import plot, show, grid, xlabel, ylabel
import numpy as np
from Brownian_Motion import brownian

"""
Adapted from scipy cookbook: https://scipy-cookbook.readthedocs.io/items/BrownianMotion.html
"""


class BrownianMotion:

    @staticmethod
    def create_asset_data():
        # The Wiener process parameter.
        delta = 2
        # Total time.
        t = 10.0
        # Number of steps.
        n = 10000
        # Time step size
        dt = t / n
        # Number of realizations to generate.
        m = int(input("input number of assets:", ))
        # Create an empty array to store the realizations.
        x = np.empty((m, n + 1))
        # Initial values of x.
        x[:, 0] = 50

        brownian.brownian(x[:, 0], n, dt, delta, out=x[:, 1:])

        t = np.linspace(0.0, n * dt, n + 1)
        for k in range(m):
            plot(t, x[k])
        xlabel('t', fontsize=16)
        ylabel('x', fontsize=16)
        grid(True)
        show()
        return [x.T, n]  # Transpose x inorder to convert to dataframe later

    def to_df(self):

        [data, num_steps] = self.create_asset_data()
        b = pd.Timestamp.now() - num_steps*pd.Timedelta('1 Day')
        new_index = pd.date_range(start=b, periods=10001, freq='D').round("D")
        df_data = pd.DataFrame(data, index=new_index)

        return df_data

    def save_csv(self):
        df = self.to_df()
        df.to_csv('./Brownian_Motion/brownian_data.csv')
        print(".csv saved, click 'backtest' to backtest on this data")
