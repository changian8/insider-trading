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



def trades_to_userhistory(trades_csv,cutoff=0.8):
    '''
    inputs: a csv of all the trades in the market (above a certain volume)
    cutoff: the percent of the max trade in the market it has to be to flag as suspicious (def could change this later)
    outputs: right now just prints the dataframes of all the trades that user has made, 
    but probably will want to either write a file or return a suspicion score for that trader
    '''
    winnings = trades_csv['size'] - trades_csv['price']*trades_csv['size']
    max_winnings = max(winnings)
    user_list = []
    print(max_winnings)
    for index,row in trades_csv.iterrows():
        price = row['price']
        size = row['size']
        winnings = size - price*size
        buy = row['side']
        if winnings > max_winnings*cutoff and buy == 'BUY':
            user_list.append(row['proxyWallet'])
    for user in user_list:
        user_info = paf.user_history(user)
        users_zipped = list(zip(*user_info))
        user_df = pd.DataFrame(users_zipped)
        user_df.columns = ['sides','sizes','prices','potential_winnings','timestamps','outcomes','slugs','condition_ids']
        print(np.shape(user_df))
        print(user_df)
    print("complete")
    return None


def plot_price_history(trades_csv):
    sorted_trades = trades_csv.sort_values(by='timestamp')
    timestamp_list =[]
    for row in sorted_trades.iterrows():
        timestamp = row['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        timestamp_list.append(dt_object)
    plt.figure(1)
    plt.plot(timestamp_list,trades_csv['price'])
    plt.show()
    return None

trades_to_userhistory(halftime)


    






