'''
Tests for the user history and analysis aspect of this project
'''
import unittest
import pandas as pd
from data_collection import polymarket_api_functions as paf

class HistoryAnalysisTests(unittest.TestCase):

    # user_history tests:

    # incorrect type of user_id
    def test_type_id(self):
        user_id = 67
        with self.assertRaises(TypeError):
            paf.user_history(user_id)

    # incorrect type of limit
    def test_type_limit(self):
        user_id = "0xadc2efbf97ce7b25f7a638aabdba196c657cd1c9"
        limit = "sixtyseven"
        with self.assertRaises(TypeError):
            paf.user_history(user_id,limit)

    # incorrect user_id - doesn't exist
    def test_user_dne(self):
        user_id = "abcdefghijklmnopqrstuvwxyzIdontlikeinsidertrading"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response,[[],[],[],[],[],[],[],[]])

    # user with no trades
    # note: this is an account I created with no trades
    def test_no_trades(self):
        user_id = "0x15a52c8504b2318f99aD7df8f511F30393BD6660-1773553384642"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response,[[],[],[],[],[],[],[],[]])

    # user with a few of trades
    def test_normal_user(self):
        # note: this is supposed to be a user that probably won't trade anymore, but if they do this test may fail...
        # one of the noted iran strike potential insider traders
        user_id = "0xa4eb52229991c074bc560f825bf2776d77acd010"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response, [['BUY','BUY'],[889.12,21508.02],[0.25,0.19],[666.84,17421.4962],[1772242789,1772240143],['Yes','Yes'],
                                         ['us-strikes-iran-by-march-1-2026-492','us-strikes-iran-by-february-28-2026-227-967-547-688-589-491-592-418-452-924-384-915-464-672-196-157-993-596-269-535-381-391-471-256-988-997-296-225-762-973-292-827-345-182-558-215-794-879-189-761'],
                                         ['0x15aa3c1259a716915e068a0d63c3885d2301d29e8982cbb1717ecb9b63d02d95', '0x3488f31e6449f9803f99a8b5dd232c7ad883637f1c86e6953305a2ef19c77f20']])
        

    # trades_to_userhistory tests:

    # check all the types 

    def test_not_a_df(self):
        trades_df= [['a'],['B'],['c'],['d']]
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(trades_df)

    def test_size_column(self):
        halftime_size_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_size = halftime_size_test.rename(columns = {'size':'not_size'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_size)
        size_wrong_type = ['a']*len(halftime_size_test)
        halftime_size_test['size'] = size_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_size_test)

    def test_price_column(self):
        halftime_price_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_price = halftime_price_test.rename(columns = {'price':'not_price'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_price)
        price_wrong_type = ['b']*len(halftime_price_test)
        halftime_price_test['price'] = price_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_price_test)
    
    def test_timestamp_column(self):
        halftime_ts_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_ts = halftime_ts_test.rename(columns = {'timestamp':'not_timestamp'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_ts)
        ts_wrong_type = ['c']*len(halftime_ts_test)
        halftime_ts_test['timestamp'] = ts_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_ts_test)

    def test_side_column(self):
        halftime_side_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_side = halftime_side_test.rename(columns = {'side':'not_side'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_side)
        side_wrong_type = [1]*len(halftime_side_test)
        halftime_side_test['side'] = side_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_side_test)
        
    def test_proxyWallet_column(self):
        halftime_pw_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_pw = halftime_pw_test.rename(columns = {'proxyWallet':'not_proxyWallet'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_pw)
        pw_wrong_type = [1]*len(halftime_pw_test)
        halftime_pw_test['proxyWallet'] = pw_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pw_test)

    def test_max_trends(self):
        halftime_trades_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        max = "as many trades as possible >:)"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_trades_test, max_trades=max)
        max = 250
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_trades_test, max_trades=max)
    
    def test_price_min(self):
        halftime_pmin_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        min = "nothing"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=min)
        min = -1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=min)
        min = 10
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=min)
        min = 1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=min)

    def test_price_max(self):
        halftime_pmax_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        max = "nothing"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=max)
        max = 10
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=max)
        max = -1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=max)
        max = 0
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=max)

    def test_empty_df(self):
        empty_df = pd.read_csv("jonathan_tests/test_empty_trades_df.csv")
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(empty_df)
       

    def test_no_flagged(self):
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
        self.assertEqual(list(empty_return.columns), list(empty_copy.columns))
        self.assertEqual(len(empty_return), 0)

    def test_bigger_df(self):
        halftime_analysis_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_flagged = paf.trades_to_userhistory(halftime_analysis_test)
        halftime_expected = pd.read_csv("jonathan_tests/halftime_test.csv")
        self.assertEqual(list(halftime_flagged.columns), list(halftime_expected.columns))
        self.assertEqual(len(halftime_flagged), 25)

    # plot price history tests:

    # check types
    # check columns

    # analyze_history tests
    
    # check type of df
    # check columns (existence, types)
    # check a few normal examples - all low risk, some of all, etc.

suite = unittest.TestLoader().loadTestsFromTestCase(HistoryAnalysisTests)
_ = unittest.TextTestRunner().run(suite)
