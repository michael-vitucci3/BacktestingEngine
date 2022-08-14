import json
import warnings

import numpy as np
import pandas as pd
import requests


# %%
class GetCoinbaseData:
    # %%
    def __init__(self):
        self.coin_list = self.fetch_coins()

    # %%
    @staticmethod
    def fetch_coins():
        """
        Get all coins from Coinbase
        :return: coin_list - list of all coins on Coinbase
        """

        headers = {"Accept": "application/json"}
        coins = requests.get("https://api.exchange.coinbase.com/currencies", headers=headers).json()
        coin_list = []
        for i in range(len(coins)):
            coin_list.append(str(coins[i]['id']))
        coin_list.sort()
        return coin_list

    # %%
    @staticmethod
    def init_time():
        """
        :return: [start_time, end_time]: initial time/day to use
        """

        a_day = pd.Timedelta('1 day')
        start_date = pd.Timestamp('2015-01-01')
        end_date = pd.Timestamp('2015-01-01') + 300 * a_day
        return start_date, end_date

    # %%
    @staticmethod
    def next_time(fun_i):
        """
        param fun_i: copy of i for function use
        :return: [start_date, end_date] - new start/end date
        """

        a_day = pd.Timedelta('1 day')
        end_date = pd.Timestamp("2015-01-01") + 300 * a_day * (fun_i + 1)
        if fun_i == 1:
            start_date = pd.Timestamp("2015-01-01") + 300 * a_day * fun_i
        else:
            start_date = pd.Timestamp("2015-01-01") + (300 * a_day * fun_i) + a_day
        return start_date, end_date

    # %%
    @staticmethod
    def fetch_data(coin, start_time, end_time):
        """
        :param coin: current coin
        :param start_time: start  time
        :param end_time: end time
        :return: df3 - dataframe of values fetched from api call
        """

        url = f'''https://api.pro.coinbase.com/products/{coin}-USD/candles?start={str(start_time)}Z&end={str(end_time)}Z&granularity=86400'''
        response = requests.get(url)
        data = pd.DataFrame(json.loads(response.text), columns=['date', 'low', 'high', 'open', 'close', 'volume'])

        # Create New DataFrame of Specific column by DataFrame.assign() method.
        df2 = pd.DataFrame().assign(date=data['date'], close=data['close'])
        df2['date'] = pd.to_datetime(df2['date'], unit='s')
        df3 = df2.set_index('date')
        df3.rename(columns={'date': 'Date', 'close': coin}, inplace=True)

        return df3

    # %%
    @staticmethod
    def create_df(df_dict):
        """
        Make one dataframe from dict of dataframes
        :param df_dict: dict of dataframes
        :return: df - single dataframe from many concatenated dataframes
        """

        df = pd.concat(df_dict)
        return df

    # %%
    def create_dict(self):
        """
        :param self:
        :return: df_dict = dict of dataframes (each key value pair representing a coins data)
        """
        coin_list = self.coin_list
        df_dict = {}

        for ii in range(len(coin_list)):
            flag = False
            start_date, end_date = self.init_time()
            full_data = self.fetch_data(coin_list[ii], start_date, end_date)
            for i in range(1, 9):
                start_date, end_date = self.next_time(i)
                data = self.fetch_data(coin_list[ii], start_date, end_date)
                full_data = pd.concat([full_data, data])

            if not flag:
                if full_data.empty:
                    print(f"{ii + 1}/{len(coin_list)}: {coin_list[ii]}  not loaded")
                else:
                    temp = full_data.sort_index(ascending=True)
                    df_dict.update({coin_list[ii]: temp})
                    print(f"{ii + 1}/{len(coin_list)}: {coin_list[ii]}  loaded")

        return df_dict

    # %%
    @staticmethod
    def dict_to_df(in_dict):
        """
        turns a dictionary of dataframes into one dataframe, concatenating column wise

        :param in_dict: dict of dataframes
        :return: out_df - single dataframe
        """
        first_key = next(iter(in_dict))
        out_df = in_dict[first_key]
        for df in list(in_dict.values())[1:]:

            try:
                out_df = pd.concat([out_df, df],
                                   axis=1,
                                   join="outer",
                                   ignore_index=False,
                                   keys=None,
                                   levels=None,
                                   names=None,
                                   verify_integrity=False,
                                   sort=False,
                                   copy=True)
                print(out_df)
            except:
                print(f'{df} Not Loaded')

        return out_df

    # %%
    def create_csv(self):
        """
        create csv file of all daily data of all coins on Coinbase
        """
        warnings.filterwarnings("ignore", category=FutureWarning)  # disable warning
        df_dict = self.create_dict()  # Create dictionary of dataframes
        final_df = self.dict_to_df(df_dict)  # Merge dictionary of dataframes into single dataframe
        final_df.to_csv('BigCSVData.csv', na_rep=np.NaN)  # Save into .csv file
        print("__________________________________________\n"
              "| Completed importing data from Coinbase |\n"
              "__________________________________________")
