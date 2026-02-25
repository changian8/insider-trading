import matplotlib.pyplot as plt
import numpy as np
import time
import requests, json
from datetime import datetime

def date_to_unix(date):
    '''
    Takes in a date in mm/dd/yyyy format and returns the appropriate unix date
    '''
    date_dt = datetime.strptime(date,"%m/%d/%Y")
    date_unix = int(date_dt.timestamp())
    return(date_unix)

def unix_to_date(unix):
    unix_dt = datetime.fromtimestamp(unix)
    mdy = unix_dt.strftime("%m/%d/%Y/%H:%M:%S")
    return mdy

def get_clob(market):
    '''
    Takes in the market json and returns the two clob ids (idk why there are 2)
    '''
    clob_list = json.loads(market[0]['clobTokenIds'])
    return clob_list

def price_at_time(clob,time,interval = 172800):
    #may want to provide possibility of getting clob if given slug?
    #and convert time to unix from mm/dd/YY if interested
    #we're going to go back and forward a week? which is 
    startt = time - interval
    history_url = f"https://clob.polymarket.com/prices-history?market={clob}&startTs={startt}"
    history = requests.get(history_url)
    history_json = history.json()
    return history_json['history']

def flag_users(trades_json,price_cutoff,trade_outcome):
    flagged_users = []
    for i in range(len(trades_json)):
        trade_info = trades_json[i]
        if trade_info['price'] < price_cutoff and trade_info['outcome']==trade_outcome:
            print("trade flagged")
            print(f"wallet: {trade_info['proxyWallet']}")
            flagged_users.append(trade_info['proxyWallet'])
            print(f"size: {trade_info['size']}")
            print(f"price: {trade_info['price']}")

def user_history(user_id,limit=1000):
    '''
    Takes a user_id (proxywallet hex code) and a limit (max is 1000, which is the default) 
    Returns a list of lists with information about each trade that user has made
    Info is the side of the trade they are on, the size of the trade, 
    the price, the timestamp, the outcome they are betting on, 
    the slug and the condition ID of the trade 
    '''
    #first part is fetching the most recent 1000 trades that the user has made and storing them in a json
    user_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}"
    user_trades = requests.get(user_url)
    user_trades_json = user_trades.json()
    
    #now we will iterate through the json and add all of the features we need to a list
    #this will allow us to easily expand past the limit of 1000 trades 
    #and ensures that we don't store useless info like the users profile picture
    sides = []
    sizes = []
    prices = []
    timestamps = []
    outcomes = []
    slugs = []
    condition_ids = []
    for item in user_trades_json:
        sides.append(item['side'])
        sizes.append(item['size'])
        prices.append(item['price'])
        timestamps.append(item['timestamp'])
        outcomes.append(item['outcome'])
        slugs.append(item['slug'])
        condition_ids.append(item['conditionId'])
    prev_length = len(user_trades_json)
    offset = limit
    #idk how much we need this but probably best practice to have a little sleep
    time.sleep(1)
    while prev_length == limit:
        print("user has traded more than limit")
        new_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}&offset={offset}"
        new_trades = requests.get(new_url)
        new_json = new_trades.json()
        for new_item in new_json:
            sides.append(new_item['side'])
            sizes.append(new_item['size'])
            prices.append(new_item['price'])
            timestamps.append(new_item['timestamp'])
            outcomes.append(new_item['outcome'])
            slugs.append(new_item['slug'])
            condition_ids.append(new_item['conditionId'])
        offset += limit
        prev_length = len(new_json)
    return [sides,sizes,prices,timestamps,outcomes,slugs,condition_ids]

def trades_hist(size_list):
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

def filter_trades(cond_id, min_size, min_price=0.05, max_price=0.95,limit=500):
    '''
    cond_id: the market
    min_size: the minimum size of the trade in USD
    min_price, max_price: sets limits on the price (see if this is actually important later)
    limit: the max number of trades to fetch
    '''
    url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cond_id}&filterType=CASH&side=BUY&filterAmount={min_size}"
    trades = requests.get(url)
    trades_json = trades.json()
    num_trades = len(trades_json)
    if num_trades == limit:
        #could either increase limit or increase min size
        new_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cond_id}&filterType=CASH&side=BUY&filterAmount={min_size*1.5}"
        trades = requests.get(new_url)
        trades_json = trades.json()
    #also need to filter for the price range
    #need to think of a good way to ensure that we get all the trades in the market that meet our conditions 
    #(or we need to change our conditions so we get all possible trades)
    