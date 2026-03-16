'''
The module pulls data from the Google trend using pytrend API and
functions for visualizing Google Trends data 
against YouTube search interest.

'''

import os
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt


def get_trend(time_range, key_words, location):
    """
    Fetches Google Trends data and saves it to a CSV file.

    Args:
        time_range (str): Date range 'YYYY-MM-DD YYYY-MM-DD'.
        key_words (list[str]): List of keywords to search.
        location (str): Two-letter country abbreviation (e.g., 'US').
    """

    if not isinstance(time_range, str) or len(time_range) != 21:
        raise ValueError("Invalid time format. Must be 'YYYY-MM-DD YYYY-MM-DD'.")
    
    if time_range[10] != ' ' or time_range[4] != '-' or time_range[15] != '-':
        raise ValueError("Invalid date delimiters. Use YYYY-MM-DD format.")

    if not isinstance(key_words, list) or not key_words:
        raise ValueError("key_words must be a non-empty list.")
    
    for word in key_words:
        if not isinstance(word, str):
            raise ValueError(f"Keyword '{word}' must be a string.")

    if not isinstance(location, str) or len(location) != 2:
        raise ValueError("location must be a 2-letter country code (e.g., 'US').")
    
    if not location.isupper():
        raise ValueError("location should be uppercase (e.g., 'US').")

    pytrends = TrendReq(hl='en-US')

    try:
        pytrends.build_payload(
            key_words,
            timeframe=time_range,
            geo=location
        )

        data = pytrends.interest_over_time()

        if data.empty:
            print("No data found for these parameters.")
            return

        output_filename = f"{key_words[0]}.csv"
        data.to_csv(output_filename)
        print(f"File saved: {output_filename}")

    except Exception as err:
        print(f"Request failed: {err}")




def plot_trends(csv_filename, incident_date_str):
    """
    Plots trends from a CSV file against YouTube search counts.

    Args:
        csv_filename (str): Path to the CSV file containing trend data.
        incident_date_str (str): The date of the event (e.g., '2026-01-01').
    """
    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found.")
        return

    try:
        data_frame = pd.read_csv(csv_filename)
    except Exception as err:
        print(f"Error reading CSV: {err}")
        return

    if 'date' not in data_frame.columns or 'youtube' not in data_frame.columns:
        print("Error: CSV must contain 'date' and 'youtube' columns.")
        return

    data_frame['date'] = pd.to_datetime(data_frame['date'])
    incident_date = pd.to_datetime(incident_date_str)

    ignore_cols = ['date', 'youtube', 'isPartial']
    trend_cols = [col for col in data_frame.columns if col not in ignore_cols]

    if not trend_cols:
        print("No search trend columns found in the CSV.")
        return

    peak_col = data_frame[trend_cols].max().idxmax()

    sorted_indices = (data_frame['date'] - incident_date).abs().argsort()
    closest_row = data_frame.iloc[sorted_indices[:1]]
    
    incident_trend_value = closest_row[peak_col].values[0]
    incident_x_pos = closest_row['date'].values[0]

    plt.figure(figsize=(10, 6))
    plt.plot(data_frame['date'], data_frame[peak_col], label=f"Trend: {peak_col}")
    plt.plot(data_frame['date'], data_frame['youtube'], label='YouTube Search')
    
    plt.axvline(x=incident_date, color='red', linestyle='--', label='Incident Date')
    plt.scatter(incident_x_pos, incident_trend_value, color='black', zorder=5)

    plt.xlabel("Date")
    plt.ylabel("Search Interest")
    plt.title(f"{peak_col} vs YouTube Search Interest")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    time = '2026-02-01 2026-02-15'
    key_words = ['Superbowl', 'Superbowl halftime', 'bad bunny','youtube']
    geo = 'US'
    get_trend(time, key_words, geo)
    plot_trends('Superbowl.csv', '2026-02-08')


    time = '2025-12-25 2026-01-10'
    key_words = ['Venezuela', 'Venezuela President', 'youtube']
    geo = 'US'
    get_trend(time, key_words, geo)
    plot_trends('Venezuela.csv', '2026-01-03')


    time = '2026-02-21 2026-03-08'
    key_words = ['Iran', 'US strikes Iran', 'US invades Iran', 'US bombs Iran','youtube']
    geo = 'US'
    get_trend(time, key_words, geo)
    plot_trends('Iran.csv', '2026-02-28')