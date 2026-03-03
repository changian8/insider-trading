import requests
import json

import pandas as pd


"""
This function returns the latest 100 trades for a given event slug.
Using the event slug it finds the condition ID then uses that to get all trades in that market
The metadata returned includes user info, price, and timestamp 
"""
def get_trades(event_slug, limit=1000):

    event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

    response = requests.get(event_url)

    data = json.loads(response.text)

    #first_market = data["markets"][0]

    first_market = next(
        m for m in data["markets"]
        if m.get("slug") == 'will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show'
    )

    cID = first_market['conditionId']

    trades_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cID}&filterType=CASH&filterAmount=50"

    trades_response = requests.get(trades_url)

    json_trades = trades_response.json()

    prettify = json.dumps(json_trades, indent=2)

    return(json_trades)

event_slug = 'who-will-perform-at-super-bowl-halftime-show'
# 'us-strikes-iran-by'
# 'will-there-be-a-streaker-at-super-bowl-lix'
# 'who-will-perform-at-super-bowl-halftime-show'
# 'us-strikes-iran-by-feb-28-odds-30-by-friday'
# 'maduro-in-us-custody-by-january-31'
all_trades = get_trades(event_slug)
print(all_trades)

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
df_sorted.to_csv("sb_performance_trades.csv", index=False)
