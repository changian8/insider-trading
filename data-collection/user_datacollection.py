import numpy as np
import pandas as pd
import polymarket_api_functions as paf


#first step: filter the trades by the most suspicious
# seems like streaker went on to the field at approximately 6:38 local time

# so it looks like this is LAST years super bowl
streaker = pd.read_csv("data-collection/sb_streaker_trades.csv")

# this is only lady gaga (which is probablay good enough for us)
halftime = pd.read_csv("data-collection/sb_performance_trades.csv")

iran_strike = pd.read_csv("data-collection/us_strikes_iran_trades.csv")
maduro = pd.read_csv("data-collection/maduro_trades.csv")


user_list_halftimeshow = []
user_list_iranstrike = []
user_list_madurocapture =[]

halftime_full_df = paf.trades_to_userhistory(halftime)
iran_full_df = paf.trades_to_userhistory(iran_strike)
maduro_full_df = paf.trades_to_userhistory(maduro)

print(np.shape(halftime_full_df))
print(np.shape(iran_full_df))
print(np.shape(maduro_full_df))
full_df = pd.concat([halftime_full_df,iran_full_df,maduro_full_df],ignore_index=True)
print(np.shape(full_df))
print(full_df)
scores = paf.analyze_history(full_df)
full_df['Insider_scores'] = scores
full_df.to_csv('trades_for_website.csv',index=False)





    






