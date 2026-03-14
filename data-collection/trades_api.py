"""
Gets the latest 1000 trades of a market for a given event slug
then converts to a dataframe and writes it out to a csv
"""

import json

import requests
import pandas as pd

def get_trades(event_slug, offset, limit=1000):
    """
    This function returns the latest 1000 trades for a given event slug.
    Using the event slug it finds the condition ID then uses that to get all trades in that market
    The metadata returned includes user info, price, and timestamp.
    Commented code represents manual condition id input,
    which is used for slugs with multiple markets such us strikes iran or sb performer
    """
    event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

    response = requests.get(event_url, timeout = 5)

    data = json.loads(response.text)

    first_market = data["markets"][0]

    # Get custom market for lady gaga performing at superbowl
    # Since the market who_performs_at_sb consists of multiple submarkets to bet on
    # first_market = next(
    #     m for m in data["markets"]
    #     if m.get("slug") == 'will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show'
    # )

    cond_id = first_market['conditionId']

    # Manually input condition id for us_strikes_iran_by since there are multiple
    # submarkets for each day that there are bets on
    # cond_id = '0x3488f31e6449f9803f99a8b5dd232c7ad883637f1c86e6953305a2ef19c77f20'

    trades_url = (f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&side=BUY&"
                  f"offset={offset}&market={cond_id}")

    trades_response = requests.get(trades_url, timeout = 5)

    json_trades = trades_response.json()

    return json_trades

# List of our different event slug markets we intend to get trades from
EVENT_SLUG = 'us-strikes-iran-by'
# 'us-strikes-iran-by'
# 'will-there-be-a-streaker-at-super-bowl-lix'
# 'who-will-perform-at-super-bowl-halftime-show'
# 'us-strikes-iran-by-feb-28-odds-30-by-friday'
# 'maduro-in-us-custody-by-january-31'
# 'what-will-be-said-during-south-park-prediction-market-episode-tonight'

# Get latest 4000 trades from our market given SLUG
# since max offset in API is 3000
all_trades1 = get_trades(EVENT_SLUG, 0)
all_trades2 = get_trades(EVENT_SLUG, 1000)
all_trades3 = get_trades(EVENT_SLUG, 2000)
all_trades4 = get_trades(EVENT_SLUG, 3000)
all_trades = all_trades1 + all_trades2 + all_trades3 + all_trades4

# Convert our trade data into a dataframe
# selecting only the columns we are interested in
# then creating column representing total value traded
# and sorting our dataframe by timestamp to latest trades
cols = [
    "proxyWallet",
    "side",
    "conditionId",
    "size",
    "price",
    "timestamp",
    "title",
    "slug",
    "eventSlug",
    "outcome",
    "outcomeIndex",
    "name",
]

df = pd.DataFrame(
    [{col: trade.get(col) for col in cols} for trade in all_trades]
)

df["total_trade_value"] = df["price"] * df["size"]
df_sorted = df.sort_values(by="timestamp", ascending=False)

# Convert dataframe to CSV
# df_sorted.to_csv("us_strikes_iran_trades_updated.csv", index=False)
