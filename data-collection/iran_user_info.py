# IRAN INSIDER TRADERS
import pandas as pd
import numpy as np
import polymarket_api_functions as paf
#users were linked in the tweet 

dicedicedice = "0xdde15ebd95330ce69136dc0ccd810d22382e02c5"
neodbs = "0x56efadc9defe5b7a21af751e0d026f2cf54136db"
planktonbets = "0x38745db27f7360a287f6ca3c9b6a6a9c76149801"
unnamed_1 = "0x1caa6a7ad0c6916aef7b67946de2e57ad24846a0"
nothingeverhappens911 = "0xa4eb52229991c074bc560f825bf2776d77acd010"

#initializing empty lists to build dataframe of all users data
names_list = [dicedicedice,neodbs,planktonbets,unnamed_1,nothingeverhappens911]
proxyWallet = []
side = []
conditionId = []
size = []
price = []
timestamp = []
title = []
slug = []
eventSlug = []
outcome = []
outcomeIndex = []
name = []
total_trade_value = []
winnings = []
trade_used = []
user_mean_winnings = []
user_number_of_trades = []
user_trades_before_this_trade = []
user_trades_after_this_trade = []
user_num_in_price_range = []
trade_percentile_winnings_compared_to_user_history = []
for item in names_list:
    user_info = paf.user_history(item)
    ttv = user_info[1]*user_info[2]
    total_trade_value.extend(ttv)
    side.extend(user_info[0])
    size.extend(user_info[1])
    price.extend(user_info[2])
    winnings.extend(user_info[3])
    timestamp.extend(user_info[4])
    outcome.extend(user_info[5])
    slug.extend(user_info[6])
    conditionId.extend(user_info[7])
    this_name = [item] * len(user_info[0])
    fillin = [True] * len(user_info[0])
    mean_winnings = [np.mean(user_info[3])]
    trade_used.extend(fillin)
    proxyWallet.extend(this_name)
    name.extend(this_name)

user_data = [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids,names]
users_zipped = list(zip(*user_data))
user_df = pd.DataFrame(users_zipped)
user_df.columns = ['sides','sizes','prices','potential_winnings','timestamps','outcomes','slugs','condition_ids','names']
print(np.shape(user_df))
print(user_df.head())
user_df.to_csv('Iran_insider_traders_trades_info.csv',index=False)


            







    