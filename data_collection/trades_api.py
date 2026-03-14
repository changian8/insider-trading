import requests
import json
import time

import pandas as pd


"""
This function returns the latest 100 trades for a given event slug.
Using the event slug it finds the condition ID then uses that to get all trades in that market
The metadata returned includes user info, price, and timestamp 
"""
def get_trades(event_slug, offset, limit=1000):

    event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

    response = requests.get(event_url)

    data = json.loads(response.text)

    # first_market = data["markets"][0]

    # first_market = next(
    #     m for m in data["markets"]
    #     if m.get("slug") == 'will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show'
    # )

    #cID = first_market['conditionId']

    cID = '0x3488f31e6449f9803f99a8b5dd232c7ad883637f1c86e6953305a2ef19c77f20'

    trades_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&offset={offset}&market={cID}&filterType=CASH&filterAmount=10"

    trades_response = requests.get(trades_url)

    json_trades = trades_response.json()

    prettify = json.dumps(json_trades, indent=2)

    return(json_trades)

event_slug = 'us-strikes-iran-by'
# 'us-strikes-iran-by'
# 'will-there-be-a-streaker-at-super-bowl-lix'
# 'who-will-perform-at-super-bowl-halftime-show'
# 'us-strikes-iran-by-feb-28-odds-30-by-friday'
# 'maduro-in-us-custody-by-january-31'
# 'what-will-be-said-during-south-park-prediction-market-episode-tonight'
all_trades1 = get_trades(event_slug, 0)
time.sleep(5)
all_trades2 = get_trades(event_slug, 1000)
time.sleep(5)
all_trades3 = get_trades(event_slug, 2000)
time.sleep(5)
all_trades4 = get_trades(event_slug, 3000)
all_trades = all_trades1 + all_trades2 + all_trades3 + all_trades4

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
df_sorted = df.sort_values(by="total_trade_value", ascending=False)

print(df_sorted.head())
print(df_sorted.shape)
#print(df_sorted.duplicated().any())
df_sorted.to_csv("us_strikes_iran_trades.csv", index=False)
