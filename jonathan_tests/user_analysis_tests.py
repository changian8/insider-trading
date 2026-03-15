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
        halftime_size_test.loc['size'] = size_wrong_type
        with self.assertRaises(TypeError):
            paf.trades_to_userhistory(halftime_size_test)

        
    # and requirements of the df 
    # and parameter edge cases
    # check simple normal example - one where we break and one where we don't ?
    # check example where no trades are flagged
    # could try tying potential winnings on the last flagged trade and seeing what gets chosen ?
    # doesn't really matter to me because it will just be ordered by whatever it was ordered by before sorting by value (timestamp)
    # could try for a user with very few trades so 90th percentile doesn't make sense ?
    # but it still is ok it will just only be their biggest trade flagging it (will still work for us roughly)

    # plot price history tests:

    # check types
    # check columns

    # analyze_history tests
    
    # check type of df
    # check columns (existence, types)
    # check a few normal examples - all low risk, some of all, etc.

suite = unittest.TestLoader().loadTestsFromTestCase(HistoryAnalysisTests)
_ = unittest.TextTestRunner().run(suite)
