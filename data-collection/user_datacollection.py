import matplotlib.pyplot as plt
import numpy as np
import requests, json
from datetime import datetime
import pandas as pd
import polymarket_api_functions as paf

#first step: filter the trades by the most suspicious
# seems like streaker went on to the field at approximately 6:38 local time

streaker = pd.read_csv("data-collection/sb_streaker_trades.csv")

user_list = []
# so it looks like this is LAST years super bowl

num_buys = 0
for index,row in streaker.iterrows():
    time = paf.unix_to_date(row['timestamp'])
    buy = row['side']
    if buy == 'BUY':
        num_buys += 1

print(num_buys)



