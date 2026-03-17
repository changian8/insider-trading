"""
Unit tests for price_history_plots module.
"""
import os
import json
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_collection.price_history_plots import get_all_market, save_market_plots
import data_collection.price_history_plots as php
from unittest.mock import patch, MagicMock

def test_get_all_market(capsys):
    """
    Test for normal running
    """
    mock_paf = MagicMock()
    mock_paf.date_to_unix.return_value = 1735689600
    mock_paf.price_at_time.return_value = {"history": []}
    original_paf = getattr(php, 'paf', None)
    php.paf = mock_paf
    try:
        clob_list = ['{bad: json}', '["id2"]', '["id3"]']
        time_start = ["2026-01-01"] * 3
        time_end = [1735689600] * 3
        php.get_all_market(clob_list, time_start, time_end)
        captured = capsys.readouterr()
        assert "Error in iteration 0" in captured.out
    finally:
        php.paf = original_paf



def test_get_all_market_json_error(capsys):
    """Verifies error handling when clob_list contains invalid JSON strings."""
    clob_list = ['invalid_json', '["id2"]', '["id3"]']
    time_start = ['12/25/2025'] * 3
    time_end = [1735085800] * 3
    results = get_all_market(clob_list, time_start, time_end)
    captured = capsys.readouterr()
    assert "Error in iteration 0" in captured.out
    assert len(results) <= 3 

@patch('data_collection.price_history_plots.plt.savefig')
@patch('data_collection.price_history_plots.plt.show')
def test_save_market_plots_success(mock_show, mock_save, tmp_path):
    """Verifies plot generation and file saving logic without opening windows."""
    mock_data = [
        {"history": [{"t": 1735084800, "p": 0.5}, {"t": 1735084900, "p": 0.6}]},
        {"history": [{"t": 1735084800, "p": 0.2}]},
        {"history": []}
    ]
    titles = ["Test1", "Test2", "Test3"]
    os.chdir(tmp_path)
    saved_files = save_market_plots(mock_data, titles)
    assert "test1_history.png" in saved_files
    assert "test2_history.png" in saved_files
    assert len(saved_files) == 2
    assert mock_save.called

def test_save_market_plots_no_history(capsys):
    """Verifies skip logic when history key is missing."""
    mock_data = [{"not_history": []}]
    save_market_plots(mock_data, ["Venezuela"])
    captured = capsys.readouterr()
    assert "Skipping index 0: No history found." in captured.out