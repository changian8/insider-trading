"""
Test module for get_trades from trades_api
"""
import unittest
import pandas as pd

from data_collection import trades_api

class TestGetTrades(unittest.TestCase):
    """
    Tests for get_trades
    """

    def test_get_trades_success(self):
        """Test normal successful API call"""

        event_slug = 'us-strikes-iran-by'
        trades = trades_api.get_trades(event_slug,0)
        trades_df = pd.DataFrame(trades)

        self.assertFalse(trades_df.isna().any().any())

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
    