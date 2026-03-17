"""
A module for getting the price history plots for each of our markets
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from data_collection import polymarket_api_functions as paf


def get_all_market(clobs, t_start, t_end):
    """
    Fetches market data for a list of clobs.
    """
    market_results = []
    for i in range(3):
        try:
            current_ids = json.loads(clobs[i])
            target_id = current_ids[0]
            start_unix = int(paf.date_to_unix(t_start[i]))
            end_unix = int(t_end[i])
            print(f"Iter {i} - Requesting ID: {target_id}")
            market_results.append(paf.price_at_time(target_id, start_unix, end_unix))
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error in iteration {i}: {e}")
    return market_results


def save_market_plots(data_list, titles):
    """
    Generates individual plots for market history.
    - Outer Background: #ffebcd
    - Inner Plot: White
    - No shading or grid lines.
    """
    saved_files = []
    for i, market_data in enumerate(data_list):
        history = market_data.get('history', [])
        if not history:
            print(f"Skipping index {i}: No history found.")
            continue

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#ffebcd')
        ax.set_facecolor('white')
        data_frame = pd.DataFrame(history)
        data_frame['datetime'] = pd.to_datetime(data_frame['t'], unit='s')

        ax.plot(data_frame['datetime'], data_frame['p'], marker='o',
                linestyle='-', markersize=4, color='#1f77b4',
                linewidth=2, label='Price')

        ax.set_title(titles[i], fontweight='bold', fontsize=20,
                     color='#333333', pad=20)
        ax.set_ylabel("Price ($)", fontweight='bold')
        ax.set_ylim(0, 1.05)
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(rotation=45)
        plt.tight_layout()
        filename = f"{titles[i].lower()}_history.png"
        plt.savefig(filename)
        saved_files.append(filename)
        plt.close(fig)
    return saved_files


if __name__ == '__main__':
    HALFTIME = pd.read_csv("data_collection/sb_performance_trades.csv")
    IRAN_STRIKE = pd.read_csv("data_collection/us_strikes_iran_trades.csv")
    MADURO = pd.read_csv("data_collection/maduro_trades.csv")
    HT_ENDT = max(HALFTIME['timestamp'])
    IRAN_ENDT = max(IRAN_STRIKE['timestamp'])
    MADURO_ENDT = max(MADURO['timestamp'])
    TIME_END = [MADURO_ENDT, HT_ENDT, IRAN_ENDT]
    TIME_START = ['12/25/2025', '02/01/2026', '02/21/2026']
    SLUG_LIST = [
        "maduro-in-us-custody-by-january-31",
        "will-lady-gaga-perform-during-the-super-bowl-lx-halftime-show",
        "us-strikes-iran-by-february-28-2026-227-967-547-688-589-491-592-418-"
        "452-924-384-915-464-672-196-157-993-596-269-535-381-391-471-256-988-"
        "997-296-225-762-973-292-827-345-182-558-215-794-879-189-761"
    ]

    CLOB_LIST = paf.get_clobs(SLUG_LIST)
    RES = get_all_market(clobs=CLOB_LIST, t_start=TIME_START, t_end=TIME_END)
    FILENAMES = save_market_plots(RES, ["Venezuela", "Superbowl", "Iran"])
