import unittest
from unittest.mock import patch, Mock
#import requests
#import pandas as pd

from data_collection.trades_api import get_trades


class MockResponse:
    def __init__(self, json_data, text_data=None, status_code=200):
        self._json = json_data
        self.text = text_data if text_data else ""
        self.status_code = status_code

    def json(self):
        return self._json


class TestGetTrades(unittest.TestCase):

    @patch("trades_api.requests.get")
    def test_get_trades_success(self, mock_get):
        """Test normal successful API call"""

        mock_get.side_effect = [
            Mock(text='{"markets":[{"conditionId":"abc"}]}'),
            MockResponse([{"price":0.5,"size":10}])
        ]

        trades = get_trades("test-event",0)

        self.assertIsInstance(trades,list)
        self.assertEqual(trades[0]["price"],0.5)


    @patch("trades_api.requests.get")
    def test_empty_markets(self, mock_get):
        """Test event slug returns no markets"""

        mock_get.return_value = Mock(text='{"markets":[]}')

        with self.assertRaises(IndexError):
            get_trades("bad-event",0)


    @patch("trades_api.requests.get")
    def test_missing_markets_key(self, mock_get):
        """API response missing markets key"""

        mock_get.return_value = Mock(text='{}')

        with self.assertRaises(KeyError):
            get_trades("bad-event",0)


    @patch("trades_api.requests.get")
    def test_missing_condition_id(self, mock_get):
        """Market missing conditionId"""

        mock_get.return_value = Mock(text='{"markets":[{}]}')

        with self.assertRaises(KeyError):
            get_trades("bad-event",0)


    @patch("trades_api.requests.get")
    def test_empty_trades(self, mock_get):
        """Trades API returns empty list"""

        mock_get.side_effect = [
            Mock(text='{"markets":[{"conditionId":"abc"}]}'),
            MockResponse([])
        ]

        trades = get_trades("event",0)

        self.assertEqual(trades,[])


    @patch("trades_api.requests.get")
    def test_trades_returns_dict(self, mock_get):
        """Trades API returns dict instead of list"""

        mock_get.side_effect = [
            Mock(text='{"markets":[{"conditionId":"abc"}]}'),
            MockResponse({"error":"bad"})
        ]

        trades = get_trades("event",0)

        self.assertIsInstance(trades,dict)


    @patch("trades_api.requests.get")
    def test_request_timeout(self, mock_get):
        """Network timeout"""

        mock_get.side_effect = requests.exceptions.Timeout

        with self.assertRaises(requests.exceptions.Timeout):
            get_trades("event",0)


    def test_dataframe_creation(self):
        """Test dataframe creation with valid trades"""

        trades = [
            {"price":0.5,"size":10,"timestamp":1},
            {"price":0.6,"size":20,"timestamp":2}
        ]

        cols = ["price","size","timestamp"]

        df = pd.DataFrame(
            [{col: trade.get(col) for col in cols} for trade in trades]
        )

        df["total_trade_value"] = df["price"] * df["size"]

        self.assertEqual(len(df),2)
        self.assertEqual(df["total_trade_value"].iloc[0],5)


    def test_missing_trade_fields(self):
        """Trades missing fields"""

        trades = [
            {"price":0.5},
            {"size":10}
        ]

        cols = ["price","size"]

        df = pd.DataFrame(
            [{col: trade.get(col) for col in cols} for trade in trades]
        )

        self.assertTrue(df.isna().any().any())


    def test_timestamp_sort(self):
        """Test timestamp sorting"""

        df = pd.DataFrame({
            "timestamp":[1,3,2]
        })

        df_sorted = df.sort_values(by="timestamp",ascending=False)

        self.assertEqual(df_sorted.iloc[0]["timestamp"],3)


if __name__ == "__main__":
    unittest.main()