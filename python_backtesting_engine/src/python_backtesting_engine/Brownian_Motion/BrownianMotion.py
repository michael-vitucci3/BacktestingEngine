import numpy as np
import pandas as pd
from matplotlib.pylab import plot, show, grid, xlabel, ylabel
import os
import inspect
import python_backtesting_engine
from python_backtesting_engine.Brownian_Motion import brownian, config

"""
Adapted from scipy cookbook: https://scipy-cookbook.readthedocs.io/items/BrownianMotion.html
"""


class BrownianMotion:
    def __init__(self):
        brownian_dict = config.get_brownian_config()
        # The Wiener process parameter.
        self.delta = brownian_dict["delta"]
        # Total time.
        self.t = brownian_dict["t"]
        # Number of steps.
        self.n = brownian_dict["n"]
        # Time step size
        self.dt = self.t / self.n
        # Number of realizations to generate.
        self.m = brownian_dict["m"]
        # Create an empty array to store the realizations.
        self.x = np.empty((self.m, self.n + 1))
        # Initial values of x.
        self.x[:, 0] = brownian_dict['x0']

    def set_config_vals(self, var, value):
        """

        :type value: int | float
        :type var: str |chr

        """
        if var == "delta":
            self.delta = value
        elif var == "t":
            self.t = value
        elif var == "n":
            self.n = value
        elif var == "m":
            self.m = value
        elif var == "x0":
            self.x = value
        else:
            print("Invalid Variable")

    def create_asset_data(self):
        brownian.brownian(self.x[:, 0], self.n, self.dt, self.delta, out=self.x[:, 1:])

        t = np.linspace(0.0, self.n * self.dt, self.n + 1)
        for k in range(self.m):
            plot(t, self.x[k])
        xlabel('t', fontsize=16)
        ylabel('x', fontsize=16)
        grid(True)
        show()
        return [self.x.T, self.n]  # Transpose x inorder to convert to dataframe later

    def to_df(self) -> pd.DataFrame:
        [data, num_steps] = self.create_asset_data()
        b = pd.Timestamp.now() - num_steps * pd.Timedelta('1 Day')
        new_index = pd.date_range(start=b, periods=(num_steps + 1), freq='D').round("D")
        df_data = pd.DataFrame(data, index=new_index)

        return df_data

    def save_csv(self):
        df = self.to_df()
        try:
            os.mkdir(os.path.dirname(inspect.getfile(python_backtesting_engine)) + '/data')
        except FileExistsError:
            print("data folder exists, skipping creation")
        df.to_csv(os.path.dirname(inspect.getfile(python_backtesting_engine)) + '/data/brownian_data.csv')
        print(".csv saved, click 'backtest' to backtest on this data")
