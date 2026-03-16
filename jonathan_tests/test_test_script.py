import pandas as pd
from data_collection import polymarket_api_functions as paf

empty_trade_df = pd.read_csv("jonathan_tests/test_empty_trades_df.csv")
non_sus_trade  = ['test_user','BUY','condid_ex',1.09,0.99,1770429543,'title_ex','slug_ex','eventslug_ex','Yes',0,'test_name',0.99]
empty_copy = empty_trade_df.copy()
empty_copy['winnings'] = None
empty_copy['user_mean_winnings'] = None
empty_copy['user_number_of_trades'] = None
empty_copy['user_trades_before_this_trade'] = None
empty_copy['user_trades_after_this_trade'] = None
empty_copy['user_90th_percentile_winnings'] = None
empty_trade_df.loc[0] = non_sus_trade
empty_return = paf.trades_to_userhistory(empty_trade_df)
print(f"trades:{empty_trade_df}")
print(f"copy:{empty_copy}")
print(f"return:{empty_return}")
print(empty_copy.equals(empty_return))