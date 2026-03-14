'''
Tests for the user history and analysis aspect of this project
'''
from data_collection import polymarket_api_functions as paf
import unittest

class HistoryAnalysisTests(unittest.TestCase):

    # user_history tests:
    # incorrect type of user_id
    def test_type_id(self):
        user_id = 67
        with self.assertRaises(TypeError):
            paf.user_history(user_id)

    # incorrecet type of limit
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

    # warning for small limit? - might be a good idea to get rid of limit parameter completely
    # goes over the limit
    # user with no trades
    # user with a lot of trades
