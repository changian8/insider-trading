"""
The module pulls data from the Google trend using pytrend API and
functions for visualizing Google Trends data
against YouTube search interest.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq


def get_trend(time_range, key_words, location):
    """
    Fetches Google Trends data and saves it to a CSV file.
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

    pytrends.build_payload(key_words, timeframe=time_range, geo=location)
    data = pytrends.interest_over_time()

    if data.empty:
        print("No data found for these parameters.")
        return

    output_filename = f"{key_words[0]}.csv"
    data.to_csv(output_filename)
    print(f"File saved: {output_filename}")



def plot_trends(csv_filename, incident_date_str):
    """
    Plots trends from a CSV file against YouTube search counts.
    """
    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found.")
        return

    data_frame = pd.read_csv(csv_filename)


    if 'date' not in data_frame.columns or 'youtube' not in data_frame.columns:
        print("Error: CSV must contain 'date' and 'youtube' columns.")
        return

    data_frame['date'] = pd.to_datetime(data_frame['date'])
    incident_date = pd.to_datetime(incident_date_str)
    ignore_cols = ['date', 'youtube', 'isPartial']
    trend_cols = [col for col in data_frame.columns if col not in ignore_cols]


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
    plt.gcf().set_facecolor('#ffebcd')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Using UPPER_CASE for constants to satisfy Pylint C0103
    GEO = 'US'

    # Superbowl Analysis
    TIME_SB = '2026-02-01 2026-02-15'
    KEYWORDS_SB = ['Superbowl', 'Superbowl halftime', 'bad bunny', 'youtube']
    get_trend(TIME_SB, KEYWORDS_SB, GEO)
    plot_trends('Superbowl.csv', '2026-02-08')

    # Venezuela Analysis
    TIME_VZ = '2025-12-25 2026-01-10'
    KEYWORDS_VZ = ['Venezuela', 'Venezuela President', 'youtube']
    get_trend(TIME_VZ, KEYWORDS_VZ, GEO)
    plot_trends('Venezuela.csv', '2026-01-03')

    # Iran Analysis
    TIME_IR = '2026-02-21 2026-03-08'
    KEYWORDS_IR = ['Iran', 'US strikes Iran', 'US invades Iran', 'youtube']
    get_trend(TIME_IR, KEYWORDS_IR, GEO)
    plot_trends('Iran.csv', '2026-02-28')
