import requests

url = "https://data-api.polymarket.com/trades?limit=100&takerOnly=true&market=0x3bed62b0b7e3eb52c1f0d8a5d11edad1f74989038fc1cae2889cdbe96a248dfe"

response = requests.get(url)

print(response.text)