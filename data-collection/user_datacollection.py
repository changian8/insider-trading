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



def trades_to_userhistory(trades_csv, trades_cutoff=5, percentile=90, sus_date=None, price_max = 0.85, price_min = 0):
    '''
    inputs: a csv of all the trades in the market (above a certain volume)
    cutoff: the percent of the max trade in the market it has to be to flag as suspicious (def could change this later)
    outputs: right now just prints the dataframes of all the trades that user has made, 
    return: indices of trades we're interested in (top 10 for each market?) and full csv of everything we're interested in
    '''
    #create mask to filter for if a trade was included, and a potential winnings column in original trades_csv
    trade_mask = [False]*len(trades_csv)
    
    trades_csv['winnings'] = trades_csv['size'] - trades_csv['price']*trades_csv['size']
    #this will ensure that we efficiently get the biggest trades in the market
    sorted_trades = trades_csv.sort_values(by='winnings',ascending=False)
    #storing each users metrics to add to a df later
    user_mean_winnings = []
    user_sum_trades = []
    user_num_before = []
    user_num_after = []
    user_num_non_extreme_price = []
    user_winnings_percentile = []
    index_used_trades = []
    user_list = []
    n_trades = 0
    n_suspicious_trades = 0
    for index,row in sorted_trades.iterrows():
        buy = row['side']
        user = row['proxyWallet']
        potential_winnings = row['winnings']
        price = row['price']
        timestamp = row['timestamp'] #add implementation for filtering before/after a suspicous date later...
        if (buy == 'BUY') and (price < price_max) and (price > price_min):
            index_used_trades.append(index)
            user_list.append(user)
            n_trades += 1
            trade_mask[index] = True
            user_info = paf.user_history(user)
            user_n_trades = len(user_info[0])
            avg_winnings = np.mean(user_info[3])
            user_mean_winnings.append(avg_winnings)
            user_sum_trades.append(user_n_trades)
            n_before = 0
            n_after = 0
            n_in_price_range = 0
            for index in range(user_n_trades):
                if user_info[4][index] < timestamp:
                    n_before += 1
                if user_info[4][index] > timestamp:
                    n_after += 1
                if (user_info[2][index] > price_min) and (user_info[2][index] < price_max):
                    n_in_price_range += 1
            user_num_before.append(n_before)
            user_num_after.append(n_after)
            user_num_non_extreme_price.append(n_in_price_range)
            winnings_percentile = np.percentile(user_info[3],percentile)
            user_winnings_percentile.append(winnings_percentile)
        # if trader has not traded a lot and has traded for generally less, flag as a suspicious trade, and the price is pretty normal
        if (user_n_trades <= trades_cutoff) and (potential_winnings >= winnings_percentile):
            n_suspicious_trades += 1
        #we will stop when we get two suspicious trades or 25 total trades (to avoid too much data)
        if n_suspicious_trades >= 10:
            break
        if n_trades >= 25:
            break
    trades_csv['trade_used'] = trade_mask
    trades_filtered = trades_csv[trades_csv['trade_used']==True].copy()
    trades_filtered['user_mean_winnings'] = user_mean_winnings
    trades_filtered['user_number_of_trades'] = user_sum_trades
    trades_filtered['user_trades_before_this_trade'] = user_num_before
    trades_filtered['user_trades_after_this_trade'] = user_num_after
    trades_filtered['user_num_in_price_range'] = user_num_non_extreme_price
    trades_filtered['trade_percentile_winnings_compared_to_user_history'] = user_winnings_percentile
    print("complete")
    # what we need to do: put the trades data AND the important user info into a dataframe, 
    # for each market we will produce one and then join them ?
    return trades_filtered


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

halftime_full_df = trades_to_userhistory(halftime)
iran_full_df = trades_to_userhistory(iran_strike)
maduro_full_df = trades_to_userhistory(maduro)

print(np.shape(halftime_full_df))
print(np.shape(iran_full_df))
print(np.shape(maduro_full_df))
full_df = pd.concat([halftime_full_df,iran_full_df,maduro_full_df],ignore_index=True)
print(np.shape(full_df))
print(full_df)
full_df.to_csv('trades_for_website.csv',index=False)





    






