import requests
import json

event_slug = 'us-strikes-iran-by'
event_url = f"https://gamma-api.polymarket.com/events/slug/{event_slug}"

response = requests.get(event_url)

json_response = response.text

data = json.loads(json_response)

first_market = data["markets"][0]

cID = first_market['conditionId']

trades_url = f"https://data-api.polymarket.com/trades?limit=100&takerOnly=true&market={cID}"

trades_response = requests.get(trades_url)

json_trades = trades_response.json()

prettify = json.dumps(json_trades, indent=2)

print(prettify)
