import matplotlib.pyplot as plt
import numpy as np
import time
import requests, json
from datetime import datetime

# Helper functions

def date_to_unix(date):
    '''
    Takes in a date in mm/dd/yyyy format and returns the appropriate unix date
    '''
    date_dt = datetime.strptime(date,"%m/%d/%Y")
    date_unix = int(date_dt.timestamp())
    return(date_unix)


def unix_to_date(unix):
    '''
    Takes in a unit timestamp and returns the date in m/d/y/h:m:s
    '''
    unix_dt = datetime.fromtimestamp(unix)
    mdy = unix_dt.strftime("%m/%d/%Y/%H:%M:%S")
    return mdy


def get_clob(market):
    '''
    Takes in the market json and returns the two clob ids (idk why there are 2)
    '''
    clob_list = json.loads(market[0]['clobTokenIds'])
    return clob_list


# Price History
def price_at_time(clob,time,interval = 172800):
    '''
    clob: the market clob
    time: time we are interested in flagging 
    interval: the interval we are interested - distance in both directions from time
    returns the price history over a specified interval around a time of interest
    '''
    startt = time - interval
    history_url = f"https://clob.polymarket.com/prices-history?market={clob}&startTs={startt}"
    history = requests.get(history_url)
    history_json = history.json()
    return history_json['history']


# getting the trades
def get_trades(cond_id, min_size,limit=1000):
    '''
    Perform the API query to get suspicious trades. Designed to filter as much as possible in the query.
    This should be combined with previous work
    cond_id: the market
    min_size: the minimum size of the trade in USD
    limit: the max number of trades to fetch
    '''
    url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cond_id}&filterType=CASH&side=BUY&filterAmount={min_size}"
    trades = requests.get(url)
    trades_json = trades.json()
    num_trades = len(trades_json)
    time.sleep(1)
    if num_trades == limit:
        #could either increase limit or increase min size
        new_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cond_id}&filterType=CASH&side=BUY&filterAmount={min_size*1.5}"
        trades = requests.get(new_url)
        trades_json = trades.json()
    return trades_json
    # I'm going to leave filtering the price range for later on when we iterate through the list 
    # If it seems like this is a problem (way too many trades at a super high price) I will come back to this later.


# taking the trades we got that are a certain size and filtering them down to what is actually interesting
def filter_trades(trades_json,winnings_cutoff,timestamp):
    '''
    This function filters the flagged high volume trades beyond what we can do in the API query
    If we think of more criteria to filter by that are not available in query add them here
    trades_json: takes a json of trades (should be filtered to exclude small trades and potentially by date of trade as well)
    winnings_cutoff: the minimum amount the user stands to win that we consider suspicious
    timestamp: the timestamp cutoff (no trades after a certain date)
    return: a list of features for each trade, price, size, timestamp, user, outcome, probably will need more later
    '''
    sizes = []
    prices = []
    timestamps = []
    outcomes = []
    users = []
    num_flagged = 0
    for i in range(len(trades_json)):
        trade_info = trades_json[i]
        trade_size = trade_info['size']
        trade_price = trade_info['price']
        trade_timestamp = trade_info['timestamp']
        trade_outcome = trade_info['outcome']
        trade_user = trade_info['proxyWallet']
        winnings = trade_size - trade_size*trade_price
        if (winnings > winnings_cutoff) and (trade_timestamp < timestamp):
            sizes.append(trade_size)
            prices.append(trade_price)
            timestamps.append(trade_timestamp)
            outcomes.append(trade_outcome)
            users.append(trade_user)
            num_flagged += 1
    print(f"Number of flagged trades: {num_flagged}")
    return [sizes, prices, timestamps, outcomes, users]


# User History
def user_history(user_id,limit=1000):
    '''
    user_id: proxywallet hex code, which is unique to a user
    limit: number of trades returned in one use of the API (max is 1000, which is the default) 
    Returns a list of lists with information about each trade that user has made
    lists: side of the trade they are on, the size of the trade, 
    the price, the timestamp, the outcome they are betting on, 
    the slug and the condition ID of the trade 
    '''
    #first part is fetching the most recent 1000 trades that the user has made and storing them in a json
    user_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}"
    user_trades = requests.get(user_url)
    user_trades_json = user_trades.json()
    
    #this will allow us to easily expand past the limit of 1000 trades 
    #and ensures that we don't store useless info like the users profile picture
    sides = []
    sizes = []
    prices = []
    potential_winnings = []
    timestamps = []
    outcomes = []
    slugs = []
    condition_ids = []
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
    #idk how much we need this but probably best practice to have a little sleep
    time.sleep(5)
    while prev_length == limit:
        print("user has traded more than limit")
        new_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}&offset={offset}"
        new_trades = requests.get(new_url)
        new_json = new_trades.json()
        for new_item in new_json:
            # CURRENTLY GETTING AN ERROR HERE, IDK what it is because it was working for the previous test user, 
            # will look into it later
            if new_item == 'error':
                continue
            sides.append(new_item['side'])
            sizes.append(new_item['size'])
            prices.append(new_item['price'])
            timestamps.append(new_item['timestamp'])
            outcomes.append(new_item['outcome'])
            slugs.append(new_item['slug'])
            condition_ids.append(new_item['conditionId'])
        offset += limit
        prev_length = len(new_json)
    return [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids]


def trades_plot(size_list):
    '''
    Takes a Json which contains all the trades a user has made
    Plots a histogram of the sizes of the trades they have made
    And returns a numerical summary of the sizes
    '''
    plt.hist(size_list)
    plt.show()
    num_trades = len(size_list)
    size_sd = np.std(size_list)
    quartiles = np.quantile(size_list, [0.25,0.5,0.75])
    dictionary = {'number of trades':num_trades, "quartiles": quartiles, "standard deviation":size_sd}
    return dictionary


def analyze_history(user_history_data,sus_trade):
    '''
    Takes information about a user's history and returns a set of metrics to evaluate how suspicious the trade they made is relative to their behavior
    user_history_data: the user history data from the user_history function
    sus_trade: info on the suspicious trade, in list form from filter_trades
    Returns: list of metrics:
    how big it was relative to other trades (percentile?) - uses sizes
    how much money do they stand to win (percentile?)- combo of price and size
    how early it was relative to other trades (percentile?) could also return date? - uses prices
    did they buy? - sides
    is there any pattern to prices that this trade doesn't follow? - outcomes/sides?
    ie: important general info is how often they buy/sell, how often they trade, average and sd of trades
    could also then go back and take these relative to their markets? too much API use? - uses slug/condid
    also difference in timestamps could be good... something is more suspicious if it happens right before cutoff date?
    '''
    #should we define these metrics relative to the market?
    #probably best to have our boundaries definable as parameters
    trade_size = sus_trade[0]
    trade_price = sus_trade[1]
    trade_winnings = (1/trade_price)*trade_size
    trade_date = sus_trade[2]
    num_trades = len(user_history_data[0])
    winnings_greater = 0
    date_earlier = 0
    for i in range(num_trades):
        if user_history_data[3][i] > trade_winnings:
            winnings_greater += 1
        if user_history_data[4][i] < trade_date:
            date_earlier += 1
    print(f"sus trades potential winnings: {trade_winnings}")
    print(f"number of trades with more potential winnings: {winnings_greater}")
    print(f"date of the sus trade: {trade_date}")
    print(f"number of trades earlier than sus date: {date_earlier}")


# basic set up stuff
'''
jan_thirty_unix = date_to_unix("01/30/2026")
jan_thirtyone_unix = date_to_unix("01/31/2026")
jan_third_unix = date_to_unix("01/03/2026")
invasion_time = jan_thirty_unix + 21600


maduro_filter_url = f"https://gamma-api.polymarket.com/markets?order=id&ascending=false&closed=true&limit=200&end_date_min={jan_thirty_unix}&end_date_max={jan_thirtyone_unix}&volume_num_min=11000000&volume_num_max=11100000"
maduro_response = requests.get(maduro_filter_url)
maduro_info = maduro_response.json()
maduro_cond_id = maduro_info[0]['conditionId']




# getting all trades on the maduro bet that have size more than 500 
# (this is a bit imperfect but based on this I don't think we'll run into API limits)
sus_trades = get_trades(maduro_cond_id, 500)
print(len(sus_trades))

# this filters based on the expected payout: 
#   we're really probably more interested in expected profit than size because it's interepretation is so dependent on price
num_actually_sus = 0
sus_traders = []
# we can see that most of the trades we classify as 'sus' trades here are actually after the invasion and realtively cheap
# this def means we need to filter for date in a different function
# I don't love flag_users because we also need the trade info, so I think I will make a new function for that 

actually_sus = filter_trades(sus_trades, 5000, invasion_time)
for item in actually_sus:
    sus_history = user_history(item[4]) 
    analyze_history(sus_history,item)
    '''

# IRAN INSIDER TRADERS

#users were linked in the tweet 

import pandas as pd
dicedicedice = "0xdde15ebd95330ce69136dc0ccd810d22382e02c5"
neodbs = "0x56efadc9defe5b7a21af751e0d026f2cf54136db"
planktonbets = "0x38745db27f7360a287f6ca3c9b6a6a9c76149801"
unnamed_1 = "0x1caa6a7ad0c6916aef7b67946de2e57ad24846a0"
nothingeverhappens911 = "0xa4eb52229991c074bc560f825bf2776d77acd010"

#initializing empty lists to build dataframe of all users data
names_list = [dicedicedice,neodbs,planktonbets,unnamed_1]
sides = []
sizes = []
prices = []
potential_winnings = []
timestamps = []
outcomes = []
slugs = []
condition_ids = []
names = []
for item in names_list:
    user_info = user_history(item)
    sides.extend(user_info[0])
    sizes.extend(user_info[1])
    prices.extend(user_info[2])
    potential_winnings.extend(user_info[3])
    timestamps.extend(user_info[4])
    outcomes.extend(user_info[5])
    slugs.extend(user_info[6])
    condition_ids.extend(user_info[7])
    this_name = [item] * len(user_info[0])
    names.extend(this_name)

user_data = [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids,names]
users_zipped = list(zip(*user_data))
user_df = pd.DataFrame(users_zipped)
user_df.columns = ['sides','sizes','prices','potential_winnings','timestamps','outcomes','slugs','condition_ids','names']
print(np.shape(user_df))
print(user_df.head())
user_df.to_csv('Iran_insider_traders_trades_info.csv',index=False)


            







    