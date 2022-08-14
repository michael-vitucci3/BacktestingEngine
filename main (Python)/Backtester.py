"""
% Backtester
class contains all necessary operations (besides StratFile which
% is stored in the main folder) to fully execute a backtest.Furthermore,
% it is a convenient data storage object. Apon calling obj.constructor
% all data will populate including
% fileLoc: Location of user input csv data
% inTT: Timetable of dates and prices gathered from a user input csv
% Returns: Daily returns of each asset during all provided data points
% coinList: List of assets gathered from csv file
% data: Using StratFile, a new version of returns is generated.If the
% algorithm is holding an asset on that day, the data points
% remain, otherwise it is changed to zero.This yeilds the actual
% returns assuming instantaneous rebalancing at 12: 00:00 UTC
% daily.
"""

import time

import easygui
import matplotlib.pyplot as plt
import pandas as pd

import StratFile


class Backtester:
    # %%
    def __init__(self):
        self.file_loc = easygui.fileopenbox(msg="Please Select .csv file of price data", filetypes="*.csv")
        self.in_df = self.load_df()
        self.ret = self.in_df.pct_change(1)
        self.logical_df = StratFile.strat_file(self.ret)

    # %%
    def load_df(self):
        """
        :param self:
        :return: a dataframe of price values generated from user selection of csv file
        """

        return pd.read_csv(self.file_loc, index_col=0)

    # %%
    def get_in_df(self):
        """
        :param self:
        :return: in_df: a dataframe of price values generated from user selection of csv file
        """

        return self.in_df

    # %%
    def get_strat(self):
        """
        :param self:
        :return: logical_df: dataframe of ones and zeros, ones representing when an algorithm is holding an asset,
         zeros when not holding the asset. (calculated based off of contents of StratFile)
        """

        return self.logical_df

    # %%
    @staticmethod
    def calc_ret(logic_df, ret):
        """
        :param logic_df: dataframe of ones and zeros, ones representing when an algorithm is holding an asset,zeros
         when not holding the asset.
        :param ret: returns at each data point (except the last since N data points yields N-1 returns values)
        :return: mult: element wise multiplication of two data frames (differing in size by one row)
        """

        logic_df_ = logic_df.copy()
        logic_df_ = logic_df_.fillna(0)
        logic_df_ = logic_df_[1:]
        print(logic_df_)

        ret_ = ret.copy()
        ret_ = ret_.fillna(0)
        ret_ = ret_[:-1]
        ret_ = ret_ + 1

        print(ret_)
        mult = logic_df_.reset_index(drop=True) * ret_.reset_index(drop=True)
        mult[mult == 0] = 1
        print(mult)
        return mult

    # %%
    def calc_stats(self):
        """
        :param  self:
        :returns: [cum_df, algo_ret]: [dataframe of cumulative values, returns based off StratFile]
        """
        tic = time.process_time()
        algo_ret = self.calc_ret(self.logical_df, self.ret)
        toc = time.process_time()
        print(f'{(toc - tic) * 1000}ms')

        cum_dict = self.val_each_asset(algo_ret)

        cum_df = self.ending_vals(cum_dict)

        self.daily_portfolio(cum_df)

        return cum_df, algo_ret

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
            plt.plot(vals.index, vals, '-')

            cum_dict.update({col_name: vals.cumprod()})

        plt.show()

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
        plt.bar(x=cum_df.columns, height=cum_df.iloc[-1].values)

        plt.show()

        return cum_df

    @staticmethod
    def daily_portfolio(cum_df):
        """
        :param cum_df: communicative values in dataframe
        """
        sum_vals = (cum_df.sum(axis=1))

        print("Value of entire portfolio each day:")
        print(sum_vals)
        xvals = range(len(sum_vals))

        plt.plot(xvals, sum_vals)
        plt.show()


a = Backtester()
b, c = a.calc_stats()
