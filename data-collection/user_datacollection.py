import matplotlib.pyplot as plt
import numpy as np
import requests, json
from datetime import datetime
import pandas as pd
import polymarket_api_functions as paf
from datetime import datetime

#first step: filter the trades by the most suspicious
# seems like streaker went on to the field at approximately 6:38 local time

# so it looks like this is LAST years super bowl
streaker = pd.read_csv("data-collection/sb_streaker_trades.csv")

# this is only lady gaga (which is probablay good enough for us)
halftime = pd.read_csv("data-collection/sb_performance_trades.csv")

iran_strike = pd.read_csv("data-collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data-collection/maduro_trades.csv")


user_list_halftimeshow = []
user_list_iranstrike = []
user_list_madurocapture =[]



def trades_to_userhistory(trades_csv):
    '''
    inputs: a csv of all the trades in the market (above a certain volume)
    cutoff: the percent of the max trade in the market it has to be to flag as suspicious (def could change this later)
    outputs: right now just prints the dataframes of all the trades that user has made, 
    return: indices of trades we're interested in (top 10 for each market?) and full csv of everything we're interested in
    '''
    trades_csv['winnings'] = trades_csv['size'] - trades_csv['total_trade_value']
    sorted_trades = trades_csv.sort_values(by='winnings',ascending=False)
    index_used_trades = []
    user_list = []
    n_trades = 0
    n_suspicious_trades = 0
    for index,row in trades_csv.iterrows():
        buy = row['side']
        user = row['proxyWallet']
        timestamp = row['timestamp']
        if (buy == 'BUY') and (user not in user_list):
            index_used_trades.append(index)
            user_list.append(user)
            n_trades += 1
            user_info = paf.user_history(user)
            user_n_trades = len(user_info[0])
            mean_winnings = np.mean(user_info[3])
            # look through and count all trades before timestamp
        # if trader has not traded a lot, has traded for generally a lot less, and wasn't very active before this trade:
        # n_suspicious_trades += 1
        if n_suspicious_trades >= 2:
            break
    
    # metrics: number of other trades, 
    # size of other trades relative to other trades (a few ways to do this), 
    # trades before and after this trade
    # winningness in other trades? that are closed
    for user in user_list:
        user_info = paf.user_history(user)
        users_zipped = list(zip(*user_info))
        user_df = pd.DataFrame(users_zipped)
        user_df.columns = ['sides','sizes','prices','potential_winnings','timestamps','outcomes','slugs','condition_ids']
        print(np.shape(user_df))
        print(user_df)
    print("complete")
    return index_used_trades, user_list


def plot_price_history(trades_csv):
    prices_updated = []
    sorted_trades = trades_csv.sort_values(by='timestamp')
    timestamp_list =[]
    for index,row in sorted_trades.iterrows():
        print(row)
        timestamp = row['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        timestamp_list.append(dt_object)
        price = row['price']
        if row['outcome'] == 'No':
            price  = 1-price
        prices_updated.append(price)
    plt.figure(1)
    plt.plot(timestamp_list,prices_updated)
    plt.show()
    return None

index_trades, user_list = trades_to_userhistory(halftime)
print(index_trades)
print(user_list)


    






