
'''
Code that reads in our trades data for each of our markets, filters them further, 
and writes a final csv for our website
'''
import numpy as np
import pandas as pd
import polymarket_api_functions as paf # pylint: disable=import-error

halftime = pd.read_csv("data_collection/sb_performance_trades.csv")
iran_strike = pd.read_csv("data_collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data_collection/maduro_trades.csv")

halftime_full_df = paf.trades_to_userhistory(halftime)
iran_full_df = paf.trades_to_userhistory(iran_strike)
maduro_full_df = paf.trades_to_userhistory(maduro)

full_df = pd.concat([halftime_full_df,iran_full_df,maduro_full_df],ignore_index=True)
print(np.shape(full_df))
print(full_df.head())
scores = paf.analyze_history(full_df)
full_df['Insider_scores'] = scores
full_df.to_csv('trades_for_website.csv',index=False)
