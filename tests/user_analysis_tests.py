'''
Tests for the user history and analysis aspect of this project
'''
import unittest
import pandas as pd
from data_collection import polymarket_api_functions as paf

class HistoryAnalysisTests(unittest.TestCase):
    '''
    tests for the code Jonathan worked on
    mainly tests user history and analysis,
    there are sections for each function defined by one line comments
    '''
    # user_history tests:

    def test_type_id(self):
        '''
        test for if the user id is an incorrect type
        '''
        user_id = 67
        with self.assertRaises(TypeError):
            paf.user_history(user_id)

    def test_type_limit(self):
        '''
        test for if the limit is an incorrect type
        '''
        user_id = "0xadc2efbf97ce7b25f7a638aabdba196c657cd1c9"
        limit = "sixtyseven"
        with self.assertRaises(TypeError):
            paf.user_history(user_id,limit)

    def test_user_dne(self):
        '''
        test for if the user id doesn't exist
        '''
        user_id = "abcdefghijklmnopqrstuvwxyzIdontlikeinsidertrading"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response,[[],[],[],[],[],[],[],[]])

    def test_no_trades(self):
        '''
        test for a user that has no trades 
        note: this user id is an account I created that hasn't trade and won't ever
        '''
        user_id = "0x15a52c8504b2318f99aD7df8f511F30393BD6660-1773553384642"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response,[[],[],[],[],[],[],[],[]])

    def test_normal_user(self):
        '''
        test for a user that does have trades
        this is a noted user who traded in the iran strike market
        if the user trades in the future but if they do the expected output will change
        '''
        user_id = "0xa4eb52229991c074bc560f825bf2776d77acd010"
        user_response = paf.user_history(user_id)
        self.assertEqual(user_response, [['BUY','BUY'],[889.12,21508.02],[0.25,0.19],[666.84,17421.4962],[1772242789,1772240143],
                                         ['Yes','Yes'],
                                         ['us-strikes-iran-by-march-1-2026-492','us-strikes-iran-by-february-28-2026-227-967-547-688-589-491-592-418-452-924-384-915-464-672-196-157-993-596-269-535-381-391-471-256-988-997-296-225-762-973-292-827-345-182-558-215-794-879-189-761'],
                                         ['0x15aa3c1259a716915e068a0d63c3885d2301d29e8982cbb1717ecb9b63d02d95', '0x3488f31e6449f9803f99a8b5dd232c7ad883637f1c86e6953305a2ef19c77f20']])

    # trades_to_userhistory tests:

    def test_not_a_df(self):
        '''
        test for if the trades df is an incorrect type
        '''
        trades_df= [['a'],['B'],['c'],['d']]
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(trades_df)

    def test_size_column(self):
        '''
        tests to ensure that the size column is in the dataframe
        and contains the correct data type
        '''
        halftime_size_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_size = halftime_size_test.rename(columns = {'size':'not_size'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_size)
        size_wrong_type = ['a']*len(halftime_size_test)
        halftime_size_test['size'] = size_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_size_test)

    def test_price_column(self):
        '''
        tests to ensure that the price column is in the dataframe
        and contains the correct data type
        '''
        halftime_price_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_price = halftime_price_test.rename(columns = {'price':'not_price'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_price)
        price_wrong_type = ['b']*len(halftime_price_test)
        halftime_price_test['price'] = price_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_price_test)

    def test_timestamp_column(self):
        '''
        tests to ensure that the timestamp column is in the dataframe
        and contains the correct data type
        '''
        halftime_ts_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_ts = halftime_ts_test.rename(columns = {'timestamp':'not_timestamp'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_ts)
        ts_wrong_type = ['c']*len(halftime_ts_test)
        halftime_ts_test['timestamp'] = ts_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_ts_test)

    def test_side_column(self):
        '''
        tests to ensure that the side column is in the dataframe
        and contains the correct data type
        '''
        halftime_side_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_side = halftime_side_test.rename(columns = {'side':'not_side'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_side)
        side_wrong_type = [1]*len(halftime_side_test)
        halftime_side_test['side'] = side_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_side_test)

    def test_proxy_wallet_column(self):
        '''
        tests to ensure that the proxyWallet column is in the dataframe
        and contains the correct data type
        '''
        halftime_pw_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_no_pw = halftime_pw_test.rename(columns = {'proxyWallet':'not_proxyWallet'})
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_no_pw)
        pw_wrong_type = [1]*len(halftime_pw_test)
        halftime_pw_test['proxyWallet'] = pw_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pw_test)

    def test_max_trades(self):
        '''
        tests to ensure that the max_trades parameter is the correct type
        and isn't too large
        '''
        halftime_trades_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        test_max = "as many trades as possible >:)"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_trades_test, max_trades=test_max)
        test_max = 250
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_trades_test, max_trades=test_max)

    def test_price_min(self):
        '''
        tests to ensure that the price_min parameter is the correct type
        and is a possible price minimum
        '''
        halftime_pmin_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        test_min = "nothing"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=test_min)
        test_min = -1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=test_min)
        test_min = 10
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=min)
        test_min = 1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmin_test, price_min=test_min)

    def test_price_max(self):
        '''
        tests to ensure that the price_max parameter is the correct type
        and is a possible price maximum
        '''
        halftime_pmax_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        test_max = "nothing"
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=test_max)
        test_max = 10
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=test_max)
        test_max = -1
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=test_max)
        test_max = 0
        with self.assertRaises(ValueError):
            paf.trades_to_userhistory(halftime_pmax_test, price_max=test_max)

    def test_empty_df(self):
        '''
        ensures that you can't call trades_to_userhistory on an empty dataframe
        '''
        empty_df = pd.read_csv("tests/test_empty_trades_df.csv")
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(empty_df)

    def test_no_flagged(self):
        '''
        test for trades_to_userhistory when no trades are flagged
        '''
        empty_trade_df = pd.read_csv("tests/test_empty_trades_df.csv")
        non_sus_trade  = ['test_user','BUY','condid_ex',1.09,0.99,1770429543,'title_ex',
                          'slug_ex','eventslug_ex','Yes',0,'test_name',0.99]
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
        '''
        tests a standard case of trades_to_userhistory
        '''
        halftime_analysis_test = pd.read_csv("data_collection/sb_performance_trades.csv")
        halftime_flagged = paf.trades_to_userhistory(halftime_analysis_test)
        halftime_expected = pd.read_csv("tests/halftime_test.csv")
        self.assertEqual(list(halftime_flagged.columns), list(halftime_expected.columns))
        self.assertEqual(len(halftime_flagged), 25)

    # analyze_history tests

    def test_analysis_not_df(self):
        '''
        tests the type of the input dataframe for analyze_history
        '''
        not_df = [["I like"],["lists"],[123]]
        with self.assertRaises(TypeError):
            paf.analyze_history(not_df)

    def test_user_num_trades_column(self):
        '''
        tests to ensure that the user_number_of_trades column is in the dataframe
        and contains the correct data type
        '''
        halftime_unt_test = pd.read_csv("tests/halftime_test.csv")
        halftime_no_unt = halftime_unt_test.rename(columns = {'user_number_of_trades':'wrong_name'})
        with self.assertRaises(ValueError):
            paf.analyze_history(halftime_no_unt)
        wrong_type = ['h']*len(halftime_unt_test)
        halftime_unt_test['user_number_of_trades'] = wrong_type
        with self.assertRaises(TypeError):
            paf.analyze_history(halftime_unt_test)

    def test_user_90p_column(self):
        '''
        tests to ensure that the user_90th_percentile_winnings column is in the dataframe
        and contains the correct data type
        '''
        halftime_90p_test = pd.read_csv("tests/halftime_test.csv")
        halftime_no_90p = halftime_90p_test.rename(columns =
                                                   {'user_90th_percentile_winnings':'wrong_name'})
        with self.assertRaises(ValueError):
            paf.analyze_history(halftime_no_90p)
        wrong_type = ['q']*len(halftime_90p_test)
        halftime_90p_test['user_90th_percentile_winnings'] = wrong_type
        with self.assertRaises(TypeError):
            paf.analyze_history(halftime_90p_test)

    def test_winnings_column(self):
        '''
        tests to ensure that the winnings column is in the dataframe
        and contains the correct data type
        '''
        halftime_winnings_test = pd.read_csv("tests/halftime_test.csv")
        halftime_no_winnings = halftime_winnings_test.rename(columns = {'winnings':'wrong_name'})
        with self.assertRaises(ValueError):
            paf.analyze_history(halftime_no_winnings)
        wrong_type = ['q']*len(halftime_winnings_test)
        halftime_winnings_test['winnings'] = wrong_type
        with self.assertRaises(TypeError):
            paf.analyze_history(halftime_winnings_test)

    def test_user_mean_w_column(self):
        '''
        tests to ensure that the user_mean_winnings is in the dataframe
        and contains the correct data type
        '''
        halftime_meanw_test = pd.read_csv("tests/halftime_test.csv")
        halftime_no_meanw = halftime_meanw_test.rename(columns =
                                                       {'user_mean_winnings':'wrong_name'})
        with self.assertRaises(ValueError):
            paf.analyze_history(halftime_no_meanw)
        wrong_type = ['q']*len(halftime_meanw_test)
        halftime_meanw_test['user_mean_winnings'] = wrong_type
        with self.assertRaises(TypeError):
            paf.analyze_history(halftime_meanw_test)

    def test_user_utbtt_column(self):
        '''
        tests to ensure that the user_trades_before_this_trade is in the dataframe
        and contains the correct data type
        '''
        halftime_utbtt_test = pd.read_csv("tests/halftime_test.csv")
        halftime_no_utbtt = halftime_utbtt_test.rename(columns =
                                                       {'user_trades_before_this_trade':'wrong_name'})
        with self.assertRaises(ValueError):
            paf.analyze_history(halftime_no_utbtt)
        wrong_type = ['q']*len(halftime_utbtt_test)
        halftime_utbtt_test['user_trades_before_this_trade'] = wrong_type
        with self.assertRaises(TypeError):
            paf.analyze_history(halftime_utbtt_test)

    def test_analysis_ht(self):
        '''
        tests a standard case of analyze_history
        '''
        halftime_user_info = pd.read_csv("tests/halftime_test.csv")
        analysis_output = paf.analyze_history(halftime_user_info)
        expected_output = ['Low Risk','Low Risk','Low Risk','Low Risk','High Risk','Low Risk',
                           'Low Risk','Low Risk','Low Risk','Low Risk','Low Risk','Low Risk',
                           'Low Risk','Low Risk','Low Risk','Low Risk','Low Risk','Low Risk',
                           'Low Risk','Low Risk','Low Risk','Low Risk','Low Risk','Low Risk',
                           'Low Risk',]
        self.assertEqual(analysis_output,expected_output)
