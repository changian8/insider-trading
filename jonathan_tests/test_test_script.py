import pandas as pd
from data_collection import polymarket_api_functions as paf

halftime_90p_test = pd.read_csv("jonathan_tests/halftime_test.csv")
halftime_no_90p = halftime_90p_test.rename(columns = {'user_90th_percentile_winnings':'wrong_name'})
paf.analyze_history(halftime_no_90p)