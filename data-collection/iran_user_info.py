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
names_list = [dicedicedice,neodbs,planktonbets,unnamed_1]
sides = []
sizes = []
prices = []
potential_winnings = []
timestamps = []
outcomes = []
slugs = []
condition_ids = []
names = []
for item in names_list:
    user_info = paf.user_history(item)
    sides.extend(user_info[0])
    sizes.extend(user_info[1])
    prices.extend(user_info[2])
    potential_winnings.extend(user_info[3])
    timestamps.extend(user_info[4])
    outcomes.extend(user_info[5])
    slugs.extend(user_info[6])
    condition_ids.extend(user_info[7])
    this_name = [item] * len(user_info[0])
    names.extend(this_name)

user_data = [sides,sizes,prices,potential_winnings,timestamps,outcomes,slugs,condition_ids,names]
users_zipped = list(zip(*user_data))
user_df = pd.DataFrame(users_zipped)
user_df.columns = ['sides','sizes','prices','potential_winnings','timestamps','outcomes','slugs','condition_ids','names']
print(np.shape(user_df))
print(user_df.head())
user_df.to_csv('Iran_insider_traders_trades_info.csv',index=False)


            







    