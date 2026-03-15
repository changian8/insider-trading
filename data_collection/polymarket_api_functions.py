'''
A set of functions to work with the polymarket API
Ultimately these are designed to be able to help take a csv of trades 
to a smaller csv file of flagged trades with additional info on 
if we think each trade may have been an insider trade
'''
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

# Helper functions

def date_to_unix(date):
    '''
    Takes in a date in mm/dd/yyyy format and returns the appropriate unix date
    '''
    date_dt = datetime.strptime(date,"%m/%d/%Y")
    date_unix = int(date_dt.timestamp())
    return date_unix


def unix_to_date(unix):
    '''
    Takes in a unit timestamp and returns the date in m/d/y/h:m:s
    '''
    unix_dt = datetime.fromtimestamp(unix)
    mdy = unix_dt.strftime("%m/%d/%Y/%H:%M:%S")
    return mdy


def user_history(user_id,limit=1000):
    '''
    Parameters:
    user_id: proxywallet hex code, which is unique to a user
    limit: number of trades returned in one use of the API (max is 1000, which is the default) 
    Returns:
    A list of lists with information about each trade that user has made
    lists: side of the trade they are on, the size of the trade, 
        the price, the timestamp, the outcome they are betting on, 
        the slug, and the condition ID of the trade 
    '''
    if not isinstance(user_id, str):
        raise TypeError("user_id is not a string")
    if not isinstance(limit, int):
        raise(TypeError("limit is not an int"))
    user_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}"
    user_trades = requests.get(user_url, timeout=(3,5))
    user_trades_json = user_trades.json()
    user_check = user_trades_json[0]['proxyWallet']
    # using lists so we can store data from multiple queries
    sides = []
    sizes = []
    prices = []
    potential_winnings = []
    timestamps = []
    outcomes = []
    slugs = []
    condition_ids = []
    if user_check != user_id:
        print("user either has not traded at all or does not exist")
        return [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids]
    for item in user_trades_json:
        potensh_winnings = item['size'] - item['price']*item['size']
        sides.append(item['side'])
        sizes.append(item['size'])
        prices.append(item['price'])
        potential_winnings.append(potensh_winnings)
        timestamps.append(item['timestamp'])
        outcomes.append(item['outcome'])
        slugs.append(item['slug'])
        condition_ids.append(item['conditionId'])
    prev_length = len(user_trades_json)
    offset = limit
    time.sleep(5)
    while prev_length == limit:
        print("user has traded more than limit")
        new_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}&offset={offset}"
        new_trades = requests.get(new_url, timeout=(3,5))
        new_json = new_trades.json()
        for new_item in new_json:
            if new_item == 'error':
                # this is a corner case that comes up only if the user has traded a lot,
                # which suggests two things:
                # 1: we probably are running into an API limit
                # 2: they probably aren't an insider trader
                # probably related to the max offset being 4000...
                continue
            sides.append(new_item['side'])
            sizes.append(new_item['size'])
            prices.append(new_item['price'])
            timestamps.append(new_item['timestamp'])
            outcomes.append(new_item['outcome'])
            slugs.append(new_item['slug'])
            condition_ids.append(new_item['conditionId'])
        offset += limit # could add check here to prevent error
        if offset >= 4000:
            print("max number of fetchable trades for one user reached")
        prev_length = len(new_json)
    return [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids]


def trades_to_userhistory(trades_df, price_max=0.85, price_min=0.1, max_trades=25):
    '''
    Parameters: 
    trades_csv: a pandas dataframe of all the trades in the market (above a certain volume)
    price_max: the maximum price for us to consider a trade 
        (a high price suggests less risk which makes insider trading less likely)
    price_min: the minimum price for us to consider a trade 
        (default is zero because insider trading seems plausible on a very low probability event)
    max_trades: the maximum number of trades to consider per market 
    return: 
    A dataframe which contains the information from get_trades about each trade 
    and information about the user's trading history
    added columns are: 
        mean potential winnings, total number of trades, number of trades before the flagged trade,
        number of trades after the flagged trade, and the user's 90th percentile potential winnings
    '''

    if not isinstance(trades_df, pd.DataFrame):
        raise TypeError("trades_df is not a pandas data frame")
    
    if 'size' in trades_df.columns:
        if  trades_df['size'].dtype != np.float64:
            raise TypeError("size column is not a numpy float")
    else:
        raise ValueError("data frame doesn't contain size column")
    
    if 'price' in trades_df.columns:
        if  trades_df['price'].dtype != np.float64:
            raise TypeError("price column is not a numpy float")
    else:
        raise ValueError("data frame doesn't contain price column")
    
    if 'timestamp' in trades_df.columns:
        if  trades_df['timestamp'].dtype != np.int64:
            raise TypeError("timestamp column is not expected type")
    else:
        raise ValueError("data frame doesn't contain timestamp column")
    
    #current typez; object
    '''
    if 'side' in trades_df.columns:
        if  trades_df['side'].dtype != str:
            raise TypeError("side column is not a string")
    else:
        raise ValueError("data frame doesn't contain side column")
    
    
    if 'proxyWallet' in trades_df.columns:
        if trades_df['proxyWallet'].dtype != str:
            raise TypeError("proxyWallet column is not a string")
    else:
        raise ValueError("data frame doesn't contain proxyWallet column")
    '''

    # check that price boundaries are ints from 0 to 1

    if isinstance(price_max, (int,float)):
        if (price_max <= 0) or (price_max > 1):
            raise ValueError("Invalid range for price_max")
    else:
        raise TypeError("Invalid type for price_max")
    
    if isinstance(price_min, (int,float)):
        if (price_min < 0) or (price_min >= 1):
            raise ValueError("Invalid range for price_min")
    else:
        raise TypeError("Invalid type for price_min")

    # check that max trades isn't too big and is the right type

    if isinstance(max_trades, int):
        if max_trades > 200:
            raise ValueError("max_trades is too big, limit is 200")
    else:
        raise TypeError("Invalid type for max_trades")
    
    # creating a mask to filter for if a trade was included
    trade_mask = [False]*len(trades_df)
    trades_df['winnings'] = trades_df['size'] - trades_df['price']*trades_df['size']
    sorted_trades = trades_df.sort_values(by='winnings',ascending=False)
    timestamp_max = max(sorted_trades['timestamp'])
    timestamp_min = min(sorted_trades['timestamp'])
    timestamp_diff = timestamp_max - timestamp_min
    timestamp_third = timestamp_diff * 0.333
    # now we'll check if we're in the first quarter ? half ? of trades based on time?
    user_mean_winnings = []
    user_sum_trades = []
    user_num_before = []
    user_num_after = []
    user_winnings_percentile = []
    index_used_trades = []
    user_list = []
    n_trades = 0
    for index,row in sorted_trades.iterrows():
        buy = row['side']
        user = row['proxyWallet']
        price = row['price']
        timestamp = row['timestamp']
        if (buy == 'BUY') and (price_min < price < price_max) and (timestamp <= timestamp_min + timestamp_third):
            index_used_trades.append(index)
            user_list.append(user)
            n_trades += 1
            trade_mask[index] = True
            user_info = user_history(user)
            user_n_trades = len(user_info[0])
            avg_winnings = np.mean(user_info[3])
            user_mean_winnings.append(avg_winnings)
            user_sum_trades.append(user_n_trades)
            n_before = 0
            n_after = 0
            for index in range(user_n_trades):
                if user_info[4][index] < timestamp:
                    n_before += 1
                if user_info[4][index] > timestamp:
                    n_after += 1
            user_num_before.append(n_before)
            user_num_after.append(n_after)
            winnings_percentile = np.percentile(user_info[3],90)
            user_winnings_percentile.append(winnings_percentile)
        # we will stop at a certain point to avoid too much data
        if n_trades >= max_trades:
            break
    trades_df['trade_used'] = trade_mask
    trades_filtered = trades_df[trades_df['trade_used']].copy()
    trades_filtered['user_mean_winnings'] = user_mean_winnings
    trades_filtered['user_number_of_trades'] = user_sum_trades
    trades_filtered['user_trades_before_this_trade'] = user_num_before
    trades_filtered['user_trades_after_this_trade'] = user_num_after
    trades_filtered['user_90th_percentile_winnings'] = user_winnings_percentile
    trades_filtered.drop('trade_used', axis=1, inplace=True)
    if len(trades_filtered) == 0:
        print("no flagged trades")
    if len(trades_filtered) < 10:
        print("less than 10 trades found")
    print("complete")
    return trades_filtered

def plot_price_history(trades_csv,market_name):
    '''
    Takes a csv of all the trades in the market and plots the price over time as a lineplot
    parameters: 
    trades_csv: a csv retrieved from get_trades with information on every trade in a market
    returns: none (plots a line plot using matplotlib)
    '''
    prices_updated = []
    sorted_trades = trades_csv.sort_values(by='timestamp')
    timestamp_list =[]
    for index, row in sorted_trades.iterrows():
        timestamp = row['timestamp']
        dt_object = datetime.fromtimestamp(timestamp)
        timestamp_list.append(dt_object)
        price = row['price']
        if row['outcome'] == 'No':
            price  = 1-price
        prices_updated.append(price)
    fig = plt.figure(1)
    fig.set_facecolor('#ffebcd')
    plt.ylabel("Price of yes")
    plt.xlabel("Date")
    plt.title(f"Price History For {market_name}")
    plt.plot(timestamp_list,prices_updated)
    plt.show()
    return 'Success'


def analyze_history(final_trades_df):
    '''
    Iterates through the final trades csv and returns a list evaluating each trade
    Parameters: 
    final_trades_csv: The dataframe from trades_to_userhistory
    Returns:
        A list with a rating of how likely we think that trade is to be insider tading
        the list is on a scale of 1 (not likely to be insider trading) to 5 (very likely)
    '''
    # logic for adding to insider score:
    # add number of trades before this one and number after to n_trades filtering
    # add 90th percentile volume to percentile
    insider_scores = []
    for index, row in final_trades_df.iterrows():
        insider_score = 'Low Risk'
        user_trades = row['user_number_of_trades']
        percentile = row['user_90th_percentile_winnings']
        potential_winnings = row['winnings']
        mean = row['user_mean_winnings']
        num_before = row['user_trades_before_this_trade']
        if (user_trades <= 20) and (num_before == 0):
            if percentile >= mean:
                insider_score = 'High Risk'
        if (20 < user_trades <= 50) and (num_before == 0):
            if potential_winnings >= percentile:
                insider_score = 'High Risk'
            if mean < potential_winnings < percentile:
                insider_score = 'Medium Risk'
        if 50 < user_trades <= 200:
            if (potential_winnings >= percentile) and (num_before <= 5):
                insider_score = 'Medium Risk'
        insider_scores.append(insider_score)
    return insider_scores
