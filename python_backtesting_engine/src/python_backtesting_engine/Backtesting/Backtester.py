# Backtester.py

"""
Backtester
class contains all necessary operations (besides StratFile which
is stored in the main folder) to fully execute a backtest.Furthermore,
it is a convenient data storage object. A pon calling obj.constructor
all data will populate including
fileLoc: Location of user input csv data
inTT: Timetable of dates and prices gathered from a user input csv
Returns: Daily returns of each asset during all provided data points
coinList: List of assets gathered from csv file
data: Using StratFile, a new version of returns is generated.If the
algorithm is holding an asset on that day, the data points
remain, otherwise it is changed to zero.This yields the actual
returns assuming instantaneous re-balancing at 12: 00:00 UTC
daily.
"""
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from python_backtesting_engine.Backtesting import StratFile


class Backtester:
    # %%
    def __init__(self, data_file):
        self._file_loc = data_file[0]
        self._csv_df = pd.read_csv(self._file_loc, index_col=0, infer_datetime_format=True, parse_dates=True)
        self._logical_df = StratFile.strat_file(self._csv_df.astype(np.number).pct_change(1))
        self._ret = self._csv_df.astype(np.number).pct_change(1)

    # %%
    @staticmethod
    def calc_ret(logic_df, ret):
        """
        :param logic_df: dataframe of ones and zeros, ones representing when an algorithm is holding an asset,zeros
         when not holding the asset.
        :param ret: returns at each data point (except the last since N data points yields N-1 returns values)
        :return: mult: element wise multiplication of two data frames (differing in size by one row)
        """

        # clean data
        logic_df_ = logic_df.fillna(0)[1:]

        ret_ = ret.fillna(0)[:-1]
        ret_ = ret_ + 1  # change from +10% == 0.10 to +10% == 1.10

        # Element wise multiplication of matrices
        mult = logic_df_.reset_index(drop=True) * ret_.reset_index(drop=True)
        mult[mult == 0] = 1

        return mult

    # %%
    @staticmethod
    def val_each_asset(algo_ret):
        """

        :param algo_ret: returns based off StratFile
        :return: cum_dict - communicative values in dictionary
        """
        cum_dict = {}
        for (col_name, col_data) in algo_ret.iteritems():
            vals = col_data.loc[~(col_data == 0)]

            cum_dict.update({col_name: vals.cumprod()})

        return cum_dict

    @staticmethod
    def ending_vals(cum_dict):
        """
        :param cum_dict: communicative values in dictionary
        :return: cum_df -  communicative values in dataframe
        """
        cum_df = pd.concat(cum_dict, axis=1, sort=True)
        cum_df.fillna(method='ffill')
        cum_df.fillna(method='bfill')
        cum_df[cum_df == 0] = 1

        print(f'Ending Values, Each Starting at $1: \n'
              f'{cum_df.iloc[[-1]]}')

        return cum_df

    @staticmethod
    def daily_portfolio(cum_df):
        """
        :param cum_df: communicative values in dataframe
        """
        sum_vals = (cum_df.sum(axis=1))
        print("Value of entire portfolio each day:")
        print(sum_vals)

        return sum_vals

    #%%
    @staticmethod
    def sharpe(portfolio_val):
        """
        Computes Sharpe Ratio from dataframe of daily total portfolio value
        :param portfolio_val: dataframe of daily portfolio values
        :return: Sharpe Ratio
        """
        daily_ret = portfolio_val.astype(np.number).pct_change(1)
        daily_ret.dropna(inplace=True)
        sharpe_ratio = np.sqrt(365)*((np.mean(daily_ret)) / (np.std(daily_ret)))  # 365 --> 225 for stocks

        return round(sharpe_ratio, 4)

    # %%
    @staticmethod
    def more_stats(cumulative_df, daily_tot):
        end_vals = ((cumulative_df.iloc[-1] - 1)/1) * 100
        max_ret = np.max(end_vals)
        min_ret = np.min(end_vals)
        avg_ret = np.mean(end_vals)
        end_return = ((daily_tot.iloc[-1]-daily_tot.iloc[0])/daily_tot.iloc[0]) * 100
        np.round(end_return, 4)

        print(f"Max single asset return: {max_ret}% \n"
              f"Min single asset loss: {min_ret}% \n"
              f"Avg overall return: {avg_ret}% \n"
              f"Overall Return: {end_return}% \n")

    # %%

    @staticmethod
    def plotter(data1, data2, data3, data4):
        """
        :param data1: cum_dict, data from val_each_asset
        :param data2: cum_df, data from ending_vals
        :param data3: sum_vals, data from daily_portfolio
        :param data4: Sharpe Ratio
        :return: None
        """

        # Plot val_each_asset data
        fig1, ax1 = plt.subplots()
        for data in data1.values():
            ax1.plot(data)
        ax1.set_xlabel("Days (# Days)")
        ax1.set_ylabel("Value (Dollars) [Starting Value of 1 Dollar for Each]")
        plt.show()

        # Plot ending_vals data
        fig2, ax2 = plt.subplots()
        ax2.bar(x=data2.columns, height=data2.iloc[-1].values)
        ax2.set_xlabel("Asset")
        ax2.set_ylabel("Ending Value (Dollars) [Starting Value of 1 Dollar for Each]")
        plt.show()

        # Plot daily_portfolio data
        fig3, ax3 = plt.subplots()
        xvals = range(len(data3))
        ax3.plot(xvals, data3)
        ax3.set_xlabel("Days (# Days)")
        ax3.set_ylabel(f'Portfolio Value (Dollars) [starting value of {len(data2.columns)}]')
        plt.show()

        try:
            if data4 < 0:
                print("Sharpe Ratio is negative, strategy is not profitable \n"
                      f"Sharpe Ratio = {data4}, ")
            elif data4 >= 0:
                # Show Sharpe Ratio
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=data4,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={'axis': {'range': [None, 4]},
                           'steps': [
                               {'range': [-1, 1], 'color': "red"},
                               {'range': [1, 2], 'color': "yellow"},
                               {'range': [2, 3], 'color': "green"},
                               {'range': [3, 4], 'color': "green"}]},
                    title={'text': "Sharpe Ratio"}))
                fig.show()
            elif data4 > 4:
                print(f"Your sharpe ratio is so good it broke the dial gauge!!!! \n"
                      f"Sharpe Ratio = {data4} ")
        except TypeError:
            print("Error Sharpe Ratio is an invalid number or not a number")

    #%%
    def calc_stats(self):
        """
        :param  self:
        :returns: [cum_df, algo_ret]: [dataframe of cumulative values, returns based off StratFile]
        """
        tic = time.process_time()
        ret = self._ret
        algo_ret = self.calc_ret(self._logical_df, ret)
        toc = time.process_time()
        print(f'{(toc - tic) * 1000}ms')

        cum_dict = self.val_each_asset(algo_ret)

        cum_df = self.ending_vals(cum_dict)

        sum_vals = self.daily_portfolio(cum_df)

        sharpe_ratio = self.sharpe(sum_vals)

        self.more_stats(cum_df, sum_vals)

        self.plotter(cum_dict, cum_df, sum_vals, sharpe_ratio)
