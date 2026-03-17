"""
Unit tests for data_collection functions using pytest.
"""
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from data_collection.google_trend import get_trend, plot_trends

# --- Existing Tests for get_trend (Validation) ---

def test_get_trend_invalid_time_format():
    """Checks if incorrect time string length or format raises ValueError."""
    with pytest.raises(ValueError, match="Invalid time format"):
        get_trend("2026-01-01", ["test"], "US")

def test_get_trend_invalid_delimiters():
    """Checks if wrong delimiters (not dashes) raise ValueError."""
    with pytest.raises(ValueError, match="Invalid date delimiters"):
        get_trend("2026.01.01 2026.01.02", ["test"], "US")

def test_get_trend_invalid_location():
    """Checks if non-uppercase or wrong length location raises ValueError."""
    with pytest.raises(ValueError, match="location must be a 2-letter country code"):
        get_trend("2026-01-01 2026-01-10", ["test"], "USA")
    with pytest.raises(ValueError, match="location should be uppercase"):
        get_trend("2026-01-01 2026-01-10", ["test"], "us")


def test_get_trend_invalid_keywords_content():
    """Checks line 25: raises ValueError if keyword list contains non-strings."""
    with pytest.raises(ValueError, match="Keyword '123' must be a string"):
        # Passing a list that contains an integer instead of all strings
        get_trend("2026-01-01 2026-01-10", ["valid", 123], "US")

def test_get_trend_empty_keywords():
    """Covers line 25: non-empty list check."""
    with pytest.raises(ValueError, match="key_words must be a non-empty list"):
        get_trend("2026-01-01 2026-01-21", [], "US")
# --- New Tests for get_trend (Functional/Success) ---

@patch('data_collection.google_trend.TrendReq')
def test_get_trend_success(mock_trend_req, tmp_path):
    """Tests successful data retrieval and CSV saving using Mocks."""
    # 1. Setup mock data
    mock_df = pd.DataFrame({
        'date': ['2026-01-01', '2026-01-02'],
        'test_kw': [10, 20],
        'isPartial': [False, False]
    })
    
    mock_instance = mock_trend_req.return_value
    mock_instance.interest_over_time.return_value = mock_df
    
    os.chdir(tmp_path)
    get_trend("2026-01-01 2026-01-02", ["test_kw"], "US")
    
    assert os.path.exists("test_kw.csv")
    saved_df = pd.read_csv("test_kw.csv")
    assert 'test_kw' in saved_df.columns

@patch('data_collection.google_trend.TrendReq')
def test_get_trend_no_data(mock_trend_req, capsys):
    """Tests behavior when pytrends returns an empty dataframe."""
    mock_instance = mock_trend_req.return_value
    mock_instance.interest_over_time.return_value = pd.DataFrame()
    
    get_trend("2026-01-01 2026-01-02", ["empty"], "US")
    captured = capsys.readouterr()
    assert "No data found for these parameters." in captured.out

# --- Tests for plot_trends ---

def test_plot_trends_file_not_found(capsys):
    """Verifies that a missing file doesn't crash the program."""
    plot_trends("fake_file.csv", "2026-01-01")
    captured = capsys.readouterr()
    assert "Error: The file 'fake_file.csv' was not found." in captured.out

def test_plot_trends_missing_columns(tmp_path, capsys):
    """Verifies error message when CSV is missing required columns."""
    d = tmp_path / "wrong_cols.csv"
    df = pd.DataFrame({"wrong": [1, 2], "cols": [3, 4]})
    df.to_csv(d, index=False)
    
    plot_trends(str(d), "2026-01-01")
    captured = capsys.readouterr()
    assert "Error: CSV must contain 'date' and 'youtube' columns." in captured.out

@patch('matplotlib.pyplot.show')
def test_plot_trends_success(mock_show, tmp_path):
    """Verifies successful plotting logic and data processing."""
    # 1. Create a valid mock CSV
    d = tmp_path / "valid_data.csv"
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "youtube": [50, 60, 70],
        "Superbowl": [10, 100, 10],
        "isPartial": [False, False, False]
    })
    df.to_csv(d, index=False)
    
    # 2. Run the plot function (mock_show prevents a window from popping up)
    plot_trends(str(d), "2026-01-02")
    
    # 3. If it reached plt.show(), the logic passed
    assert mock_show.called