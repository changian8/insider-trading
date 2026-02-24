import requests
import json

"""
This function returns the latest 100 trades for a given event slug.
Using the event slug it finds the condition ID then uses that to get all trades in that market
The metadata returned includes user info, price, and timestamp 
"""
def get_trades(event_slug, limit=100):

    event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

    response = requests.get(event_url)

    data = json.loads(response.text)

    first_market = data["markets"][0]

    cID = first_market['conditionId']

    trades_url = f"https://data-api.polymarket.com/trades?limit={limit}&takerOnly=true&market={cID}"

    trades_response = requests.get(trades_url)

    json_trades = trades_response.json()

    prettify = json.dumps(json_trades, indent=2)

    return(prettify)

event_slug = 'us-strikes-iran-by'
print(get_trades(event_slug))

