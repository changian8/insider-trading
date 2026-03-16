"""
Unit tests for data_collection functions using pytest.
"""
import os
import pandas as pd
import pytest
from data_collection.google_trend import get_trend, plot_trends

# --- Tests for get_trend ---

def test_get_trend_invalid_time_format():
    """Checks if incorrect time string length or format raises ValueError."""
    with pytest.raises(ValueError, match="Invalid time format"):
        get_trend("2026-01-01", ["test"], "US")  # Too short

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

# --- Tests for plot_trends ---

def test_plot_trends_file_not_found(capsys):
    """Verifies that a missing file doesn't crash the program."""
    plot_trends("fake_file.csv", "2026-01-01")
    captured = capsys.readouterr()
    assert "Error: The file 'fake_file.csv' was not found." in captured.out

def test_plot_trends_missing_columns(tmp_path, capsys):
    """Verifies error message when CSV is missing required columns."""
    # Create a temporary CSV with wrong columns
    d = tmp_path / "wrong_cols.csv"
    df = pd.DataFrame({"wrong": [1, 2], "cols": [3, 4]})
    df.to_csv(d, index=False)
    
    plot_trends(str(d), "2026-01-01")
    captured = capsys.readouterr()
    assert "Error: CSV must contain 'date' and 'youtube' columns." in captured.out