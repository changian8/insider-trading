'''
A file for getting the price history plots for each of our markets
'''
import pandas as pd
import polymarket_api_functions as paf

halftime = pd.read_csv("data-collection/sb_performance_trades.csv")
iran_strike = pd.read_csv("data-collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data-collection/maduro_trades.csv")

min_halftime_timestamp = paf.unix_to_date(min(halftime['timestamp']))
max_halftime_timestamp = paf.unix_to_date(max(halftime['timestamp']))
print(f"earliest halftime trade: {min_halftime_timestamp}")
print(f"latest halftime trade: {max_halftime_timestamp}")

min_iran_timestamp = paf.unix_to_date(min(iran_strike['timestamp']))
max_iran_timestamp = paf.unix_to_date(max(iran_strike['timestamp']))
print(f"earliest Iran trade: {min_iran_timestamp}")
print(f"latest Iran trade: {max_iran_timestamp}")

min_maduro_timestamp = paf.unix_to_date(min(maduro['timestamp']))
max_maduro_timestamp = paf.unix_to_date(max(maduro['timestamp']))
print(f"earliest trade: {min_maduro_timestamp}")
print(f"latest trade: {max_maduro_timestamp}")


paf.plot_price_history(halftime,"Halftime Special Guest")
paf.plot_price_history(iran_strike,"Iran Strike")
paf.plot_price_history(maduro,"Maduro Capture")
