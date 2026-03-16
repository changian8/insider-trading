'''
A file for getting the price history plots for each of our markets
'''
import pandas as pd
import polymarket_api_functions as paf

'''
halftime = pd.read_csv("data_collection/sb_performance_trades.csv")
iran_strike = pd.read_csv("data_collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data_collection/maduro_trades.csv")

min_halftime_timestamp = paf.unix_to_date(min(halftime['timestamp']))
max_halftime_timestamp = paf.unix_to_date(max(halftime['timestamp']))
halftime_yes = (halftime['outcome'] == 'Yes').sum()
print(f"number of yes halftime bets: {halftime_yes}")
print(f"earliest halftime trade: {min_halftime_timestamp}")
print(f"latest halftime trade: {max_halftime_timestamp}")

min_iran_timestamp = paf.unix_to_date(min(iran_strike['timestamp']))
max_iran_timestamp = paf.unix_to_date(max(iran_strike['timestamp']))
iran_yes = (iran_strike['outcome'] == 'Yes').sum()
print(f"number of yes iran bets: {iran_yes}")
print(f"earliest Iran trade: {min_iran_timestamp}")
print(f"latest Iran trade: {max_iran_timestamp}")

min_maduro_timestamp = paf.unix_to_date(min(maduro['timestamp']))
max_maduro_timestamp = paf.unix_to_date(max(maduro['timestamp']))
maduro_yes = (maduro['outcome'] == 'Yes').sum()
print(f"number of yes maduro bets: {maduro_yes}")
print(f"earliest trade: {min_maduro_timestamp}")
print(f"latest trade: {max_maduro_timestamp}")
'''

'''
paf.plot_price_history(halftime,"Halftime Special Guest")
paf.plot_price_history(iran_strike,"Iran Strike")
paf.plot_price_history(maduro,"Maduro Capture")
'''
halftime = pd.read_csv("data_collection/sb_performance_trades.csv")
iran_strike = pd.read_csv("data_collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data_collection/maduro_trades.csv")
ht_endt = max(halftime['timestamp'])
iran_endt = max(iran_strike['timestamp'])
maduro_endt = max(maduro['timestamp'])

slug_list = ["maduro-in-us-custody-by-january-31","will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show",
             "us-strikes-iran-by-february-28-2026-227-967-547-688-589-491-592-418-452-924-384-915-464-672-196-157-993-596-269-535-381-391-471-256-988-997-296-225-762-973-292-827-345-182-558-215-794-879-189-761"]
clob_list = paf.get_clobs(slug_list)
for clob in clob_list[0]:
    paf.price_at_time(clob,maduro_endt)




