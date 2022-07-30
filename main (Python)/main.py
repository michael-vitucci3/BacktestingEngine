# %%
# import packages
import warnings
import pandas as pd
import requests
import json
import pprint


# %%
def fetch_coins():
    # Get all coins from Coinbase
    headers = {"Accept": "application/json"}
    coins = requests.get("https://api.exchange.coinbase.com/currencies", headers=headers).json()
    url = "https://api.exchange.coinbase.com/products/"
    coinList = []
    for i in range(len(coins)):
        coinList.append(str(coins[i]['id']))
    coinList.sort()
    return coinList


# %%
def init_time():
    aDay = pd.Timedelta('1 day')
    start_date = pd.Timestamp('2015-01-01')
    end_date = pd.Timestamp('2015-01-01') + 300 * aDay
    return start_date, end_date


# %%
def next_time(fun_i):
    aDay = pd.Timedelta('1 day')
    end_date = pd.Timestamp("2015-01-01") + 300 * aDay * (fun_i + 1)
    if fun_i == 1:
        start_date = pd.Timestamp("2015-01-01") + 300 * aDay * fun_i
    else:
        start_date = pd.Timestamp("2015-01-01") + (300 * aDay * fun_i) + aDay
    return start_date, end_date


# %%
def fetch_data(coin, start_time, end_time):
    url = f'''https://api.pro.coinbase.com/products/{coin}-USD/candles?start={str(start_time)}Z&end={str(end_time)}Z&granularity=86400'''
    response = requests.get(url)
    data = pd.DataFrame(json.loads(response.text), columns=['date', 'low', 'high', 'open', 'close', 'volume'])

    # Create New DataFrame of Specific column by DataFrame.assign() method.
    df2 = pd.DataFrame().assign(date=data['date'], close=data['close'])
    df2['date'] = pd.to_datetime(df2['date'], unit='s')
    # df2.index('date')
    ind = df2['date'].index
    df3 = df2.set_index('date')
    df3.rename(columns={'date':'Date','close':coin},inplace=True)
    return df3


# %%
def create_df(df_dict):
    df = pd.concat(df_dict)
    return df


# %%


# %%
def create_dict():
    coinList = fetch_coins()
    not_loaded = []
    df_dict = {}

    for ii in range(len(coinList)):
        flag = False
        start_date, end_date = init_time()
        full_data = fetch_data(coinList[ii], start_date, end_date)
        for i in range(1, 9):
            start_date, end_date = next_time(i)
            data = fetch_data(coinList[ii], start_date, end_date)
            full_data = pd.concat([full_data, data])

        if not flag:
            if full_data.empty:
                print(f"{ii + 1}/{len(coinList)}: {coinList[ii]}  not loaded")
            else:
                temp = full_data.sort_index(ascending=True)
                df_dict.update({coinList[ii]: temp})
                print(f"{ii + 1}/{len(coinList)}: {coinList[ii]}  loaded")

    return df_dict


def dict_to_df(in_dict):
    first_key = next(iter(in_dict))
    out_df = in_dict[first_key]
    for df in list(in_dict.values())[1:]:
        try:
            out_df = pd.concat([out_df,df],
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
def create_csv():
    warnings.filterwarnings("ignore", category=FutureWarning)  # disable warning
    df_dict = create_dict()  # Create dictionary of dataframes
    final_df = dict_to_df(df_dict)  # Merge dictionary of dataframes into single dataframe
    final_df.to_csv('BigCSVData.csv')  # Save into .csv file
    print("__________________________________________\n"
          "| Completed importing data from Coinbase |\n"
          "__________________________________________")