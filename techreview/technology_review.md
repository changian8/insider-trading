# Technology Review: Python Library Selection for Insider Trading

**Course:** Data 515 

**Project:** Insider Trading Watchdog

**Team Members:** Aaron Kann, Ian Chang, Jonathan Grothe, Josh Tseng  

**Date:** 2/23/2026

---

# 1. Background and Problem Statement

## 1.1 Project Overview

As [recent viral bets](https://www.npr.org/2026/01/05/nx-s1-5667232/polymarket-maduro-bet-insider-trading) surrounding current events have gone viral in that the internet suggests blatant insider trading, 
we wanted to test our hypothesis that insider trading occurs on Polymarket in such a blatant fashion
that it is obvious to the outside eye,
and create a "watch dog" website that explains our findings and methodologies to interested users while allowing them to
explore the data. 

## 1.2 Technology Requirement

We will need access the Polymarket betting data, which is not the focus of 
not focus on this technical review as we can use their official API.  


Other than that, we would like to get data on the relevance of a term in the public discourse 
in order to measure the popularity of a topic
to see whether a bet's amount alligns with the public exposure it is getting.  
An API that allows us to track the popularity of a term's google search
seems like a wise choice.  

## 1.3 Use Case Requirements

List the functional and technical requirements.

**Functional requirements:**
- Retrieve interest over time for keywords
- Retrieve related queries
- Support geographic filtering
- Able to filter for a period of time


**Technical requirements:**
- Compatible with Python 3
- Reliable and maintained
- Efficient for repeated queries

---

# 2. Candidate Libraries

We evaluated the following three libraries:

1. pytrends  
2. SerpApi Google Trends API  
3. Apify Google Trends API  


## 2.1 Library 1: Pytrends

**Author:** Community-maintained (unofficial Google Trends API) 

**Repository:** https://github.com/GeneralMills/pytrends  

**Type:** Unofficial scraper

**Summary:**  
Pytrends is an unoffical Google trend library, which reverse engineers Google trends request and retrieves trend data without paying for an API key.

**Key Features:**
- Interest over time
- Interest by region
- Related queries
- Related topics
- No API key required

**Installation:**

```bash

pip install pytrends
```
## 2.2 Library 2: SerpApi Google Trends API

**Author:** SerpApi  
**Organization:** SerpApi LLC  
**Type:** Official managed API service  
**Website:** https://serpapi.com  
**Python Compatibility:** Python 3.x  

### Summary

SerpApi provides a structured API to retrieve Google Trends data reliably. It uses managed infrastructure to avoid rate limits and blocking.

### Key Features

- Reliable Google Trends data access
- Handles rate limiting automatically
- Provides structured JSON output

### Installation

```bash
pip install google-search-results
```
## 2.3 Library 3: Trendspyg

**Author:** Open-source community  
**Repository:** https://github.com/flack0x/trendspyg  
**Type:** Open-source Google Trends library  

**Summary:**  
trendspyg is a free and open-source Python library designed to retrieve real-time Google Trends data.

**Key Features:**
- Retrieve real-time trending searches
- Support for 125+ countries and 51 US states
- Category filtering (sports, technology, health, etc.)
- Multiple output formats (DataFrame, CSV, JSON)
- Built-in caching for improved performance
- Async support for parallel data retrieval

**Installation:**

```bash
pip install trendspyg

```

---

# 3. Technologies Comparison

Simple examples of each library 

## 3.1 Pytrend

```python
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US')

pytrends.build_payload(
    ['Venezuela', 'Venezuela President'],
    timeframe='2026-01-01 2026-01-31',
    geo='US'
)

```

The output gives you a timeseries table from the begining of January to end of January in 2026, and colmns as Venezuela and Venezuela President, where the cell will be the relative intrest overtime. Pytrends also allows us to filter for the geo location, and able to put multiple related words in the search list.

```
date,Venezuela,Venezuela President
2026-01-01,2,0
2026-01-02,1,0
2026-01-03,100,10
2026-01-04,57,6
....
```
Above is the first several rows of the datagrame we obtain from pytrends. 


## 3.2 SerpApi

As this API costs money to use, it is impracitcal to use this API at scale.

Thus, unfortunately, we will not test this API as it does not fit into our technical requirements.

## 3.3 Trendpyg

```python
from trendspyg import download_google_trends_rss

trends = download_google_trends_rss(geo='US')

for trend in trends[:500]:
    print(f"{trend['trend']} - {trend['traffic']}")
    if trend['news_articles']:
        print(f"  {trend['news_articles'][0]['headline']}")

```

The output gives us the click rate of the current articles, and able to filter for geo location as well.
However, it is a lot harder to filter for the key words that we would be interested for.

example of output 
```
lottery powerball winning numbers - 200+
  Powerball winning numbers for Monday, February 23, 2026
tropical cyclone horacio - 200+
  Tropical Cyclone Horacio: Earth’s first Category 5 tropical cyclone of 2026
panama canal ports - 2000+
  Panama cancels China-linked port deal, hands canal terminals to Maersk, MSC
bobby cannavale - 200+
```

---

# 4. Final Choice

After installing the three different python libraries, we decided to officially use the pytrends API. 
Pytrends offers a simple bridge to Google trends intrest over a specific period for free.
The other two solve this issue but add additional complexity not worth taking on;
trendpyg requires to download the information in the past hours and process from there,
whereas SerpApi only gives a small amount of free request, anything more we will need to pay.

Pytrends also allows users to find the intrest of a list of words during a period of time, where each word is compared to others search counts, allows us to request a list of related words. 

# 5. Limitations of the Technology 

Pytrends is easy to use and fits the functional and technical requirements we need such as filtering for geolocation,
a period of time, and search for a word list. 
However, it does have some limitations.

For example, due to the methodology of the library, it is unable to give us the exact search counts for the keywords, instead giving us a relative intrest of certain word over time and normalizing it as a number from 0 - 100, where 100 means during that period of time that word has the most seraches compared to all the words in the list throughout the entire period. 
A solution we thought of in order to overcome this issue is including very steady high search words in the key word list as an anchor, such as words like facebook or instagram, all have similar high intrest on a given time.
Although not perfect, it will be the closest proxy we can reasonably obtain. 

Another concern is since it is an unoffical libary maintained by an open source community, it means if Google changes the backend, the whole libary could stop working immidiately.  
This would be an issue worth addressing if we got to the extended phases of this project and wanted to implement a live tracker, however, we have defined the scope of the project for the sake of DSE515 to end at a data analysis and written report.
Therefore, we believe the pytrends API, which has been used by previous group project members for personal projects over 6 months ago, to be a safe option to work for the remaining three-week class sprint as we attempt to scale the project. 
