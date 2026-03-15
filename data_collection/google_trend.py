'''
The module pulls data from the Google trend using pytrend API 
'''

from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

def get_trend(time, key_words, location):
    '''
    time(str) is the duration of time we are intrested, in the format of 'xxxx-xx-xx yyyy-yy-yy' inclusive
    where xxxx-xx-xx is the start and yyyy-yy-yy is the end
    key_words(list[str]) list of strings we are intrested looking up the trend
    location(str) the searches location we are intrested in

    '''
    
    pytrends = TrendReq(hl='en-US')

    pytrends.build_payload(
        key_words,
        timeframe=time,
        geo=location
    )

    data = pytrends.interest_over_time()
    data.to_csv(f"{key_words[0]}.csv")
    

def plot_trends(filename, incident_date):
    '''
    Used to plot the trends from a csv file, against Youtube Search counts.
    '''
    df = pd.read_csv(filename)

    df['date'] = pd.to_datetime(df['date'])
    incident_date = pd.to_datetime(incident_date)
    trend_cols = [c for c in df.columns if c not in ['date', 'youtube', 'isPartial']]
    peak_col = df[trend_cols].max().idxmax()
    row = df.iloc[(df['date'] - incident_date).abs().argsort()[:1]]
    incident_trend = row[peak_col].values[0]
    incident_x = row['date'].values[0]
    plt.figure()
    plt.plot(df['date'], df[peak_col], label=peak_col)
    plt.plot(df['date'], df['youtube'], label='youtube')
    plt.axvline(x=incident_date, linestyle='--', label='incident')
    plt.scatter(incident_x, incident_trend)
    plt.xlabel("Date")
    plt.ylabel("Search Interest")
    plt.title(f"{peak_col} vs YouTube Search Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


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


time = '2026-02-21 2026-03-8'
key_words = ['Iran', 'US strikes Iran', 'US invades Iran', 'US bombs Iran','youtube']
geo = 'US'
get_trend(time, key_words, geo)
plot_trends('Iran.csv', '2026-02-28')