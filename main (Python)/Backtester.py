'''% Backtester


class contains all necessary operations (besides StratFile which
% is stored in the main folder) to fully execute a backtest.Furthermore,

% it is a convient data storage object.Apon calling obj.constructor
% all data will populate including
% fileLoc: Location of user input csv data
% inTT: Timetable of dates and prices gathered from a user input csv
% Returns: Daily returns of each asset during all provided data points
% coinList: List of assets gathered from csv file
% data: Using StratFile, a new version of returns is generated.If the
% algorithm is holding an asset on that day, the data points
% remain, otherwise it is changed to zero.This yeilds the actual
% returns assuming instintanious rebalancing at 12: 00:00 UTC
% daily. classdef Backtester properties name fileLoc inTT returns coinList data end
'''

import easygui
import numpy
import pandas as pd
import StratFile
import numpy as np
import time
import matplotlib.pyplot as plt



class Backtester:
    def __init__(self):
        self.file_loc = easygui.fileopenbox(msg="Please Select .csv file of price data", filetypes="*.csv")
        self.in_df = self.load_df()
        self.ret = self.in_df.pct_change(1)
        self.logical_df = StratFile.StratFile(self.ret)

    def load_df(self):
        return pd.read_csv(self.file_loc, index_col=0)

    def get_in_df(self):
        return self.in_df

    def get_strat(self):
        return self.logical_df

    def calc_ret(self, logic_df, ret):
        logic_df_ = logic_df.copy()
        logic_df_ = logic_df_.fillna(0)
        logic_df_ = logic_df_[1:]
        print(logic_df_)
        # logic_df_np = logic_df_np.replace(np.nan, 0)
        ret_ = ret.copy()
        ret_ = ret_.fillna(0)
        ret_ = ret_[:-1]
        ret_ = ret_ + 1
        # ret_np = ret_np.replace(np.nan, 0)
        print(ret_)
        mult = logic_df_.reset_index(drop=True) * ret_.reset_index(drop=True)
        #mult.loc[~(mult==0).all(axis=1)]
        print(mult)
        return mult

    def calc_stats(self):
        cum_dict={}
        tic = time.process_time()
        algo_ret = self.calc_ret(self.logical_df, self.ret)
        toc = time.process_time()
        print(f'{(toc - tic) * 1000}ms')
        for (col_name, col_data) in algo_ret.iteritems():
            portfolio_val = [1]
            vals = col_data.loc[~(col_data==0)]
            plt.plot(vals.index, vals, '-')

            cum_dict.update({col_name: vals.cumprod()})

        plt.show()

        cum_df = pd.concat(cum_dict, axis=1, sort=True)
        cum_df.fillna(method='ffill')
        cum_df.fillna(method='bfill')
        cum_df[cum_df==0] = 1

        print(f'Ending Values, Each Starting at $1: \n'
              f'{cum_df.iloc[[-1]]}')
        plt.bar(x=cum_df.columns,height=cum_df.iloc[-1].values)
        plt.show()

        sum_vals = []
        for i in range(len(cum_df.columns)):
            sum_vals.append(cum_df.iloc[i].sum())

        xvals = range(len(sum_vals))

        plt.plot(xvals,sum_vals)
        plt.show()



a = Backtester()
b = a.calc_stats()
