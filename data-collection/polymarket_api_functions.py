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


def get_trades(event_slug, limit=1000):
    """
    This function returns the latest 100 trades for a given event slug.
    Using the event slug it finds the condition ID then uses that to get all trades in that market
    The metadata returned includes user info, price, and timestamp 
    """
    event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

    response = requests.get(event_url)

    data = json.loads(response.text)

    #first_market = data["markets"][0]

    # first_market = next(
    #     m for m in data["markets"]
    #     if m.get("slug") == 'will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show'
    # )

    #cID = first_market['conditionId']

    cID = '0x3488f31e6449f9803f99a8b5dd232c7ad883637f1c86e6953305a2ef19c77f20'

    trades_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cID}&filterType=CASH&filterAmount=50"

    trades_response = requests.get(trades_url)

    json_trades = trades_response.json()

    prettify = json.dumps(json_trades, indent=2)

    return(json_trades)


def user_history(user_id,limit=1000):
    '''
    user_id: proxywallet hex code, which is unique to a user
    limit: number of trades returned in one use of the API (max is 1000, which is the default) 
    Returns a list of lists with information about each trade that user has made
    lists: side of the trade they are on, the size of the trade, 
        the price, the timestamp, the outcome they are betting on, 
        the slug and the condition ID of the trade 
    '''

    user_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}"
    user_trades = requests.get(user_url)
    user_trades_json = user_trades.json()
    # setting up lists so that we can store data from multiple queries if the user has traded more than the limit
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
    time.sleep(5)
    while prev_length == limit:
        print("user has traded more than limit")
        new_url = f"https://data-api.polymarket.com/trades?user={user_id}&limit={limit}&offset={offset}"
        new_trades = requests.get(new_url)
        new_json = new_trades.json()
        for new_item in new_json:
            if new_item == 'error':
                # this is a corner case that comes up only if the user has traded a lot, 
                # which suggests two things: 
                # 1: we probably are running into an API limit 
                # 2: they probably aren't an insider trader
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


def trades_to_userhistory(trades_csv, trades_cutoff=5, sus_date=None, price_max=0.85, price_min=0, max_trades=25):
    '''
    inputs: trades_csv: a csv of all the trades in the market (above a certain volume)
    trades_cutoff: the number of trades needed to consider a user as insider trading (the fewer trades the more suspicious)
    percentile: the percentile of potential winnings a trade needs to be to be flagged as potentially insider trading
    sus_date: TBD
    price_max: the maximum price for us to consider a trade 
        (a high price suggests less risk which makes insider trading less likely)
    priec_min: the minimum price for us to consider a trade 
        (default is zero because insider trading seems plausible on a very low probability event)
    cutoff: the percent of the max trade in the market it has to be to flag as suspicious (def could change this later)
    return: a dataframe which contains the information from get_trades about each trade as well as information about the user's trading history
        added columns are: mean potential winnings, total number of trades, number of trades before the flagged trade, 
        number of trades after the flagged trade, and the percentile of the potential winnings as compared to the other trades
    '''
    # creating a mask to filter for if a trade was included, so we can easily trim the dataframe later
    trade_mask = [False]*len(trades_csv)
    trades_csv['winnings'] = trades_csv['size'] - trades_csv['price']*trades_csv['size']
    sorted_trades = trades_csv.sort_values(by='winnings',ascending=False)
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
        timestamp = row['timestamp'] #add implementation for filtering before/after a suspicous date later...
        if (buy == 'BUY') and (price < price_max) and (price > price_min):
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
    trades_csv['trade_used'] = trade_mask
    trades_filtered = trades_csv[trades_csv['trade_used']==True].copy()
    trades_filtered['user_mean_winnings'] = user_mean_winnings
    trades_filtered['user_number_of_trades'] = user_sum_trades
    trades_filtered['user_trades_before_this_trade'] = user_num_before
    trades_filtered['user_trades_after_this_trade'] = user_num_after
    trades_filtered[f'user_90th_percentile_winnings'] = user_winnings_percentile
    trades_filtered.drop('trade_used', axis=1, inplace=True)
    print("complete")
    return trades_filtered

def plot_price_history(trades_csv):
    '''
    Takes a csv of all the trades in the market and plots the price over time as a lineplot
    parameters: trades_csv: a csv retrieved from get_trades with information on every trade in a market
    returns: none (plots a line plot using matplotlib)
    '''
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


def analyze_history(final_trades_csv):
    '''
    Iterates through the final trades csv and returns a list of 1-10 scores of how likely we think the trade is an insider trade
    after running this function we could add it as a column to our final dataframe?
    '''
    # logic for adding to insider score: 
    insider_scores = []
    for index, row in final_trades_csv.iterrows():
        insider_score = 'Low Risk'
        user_trades = row['user_number_of_trades']
        percentile = row['user_90th_percentile_winnings']
        potential_winnings = row['winnings']
        mean = row['user_mean_winnings']
        if user_trades <= 20:
            if potential_winnings >= percentile:
                insider_score = 'High Risk'
            if (potential_winnings < percentile) and (potential_winnings > mean):
                insider_score = 'Medium Risk'
        if (user_trades > 20) and (user_trades <= 50):
            if potential_winnings >= percentile:
                insider_score = 'High Risk'
            if (potential_winnings < percentile) and (potential_winnings > mean):
                insider_score = 'Medium Risk'
        if (user_trades > 50) and (user_trades <= 200):
            if potential_winnings >= percentile:
                insider_score = 'Medium Risk'
        insider_scores.append(insider_score)
    return insider_scores

            
        
