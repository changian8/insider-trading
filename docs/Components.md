# Components 

## Market Information

First we will use the Polymarket markets API to filter markets to find the ones we are most interested in, and storing their market slugs. We will ensure that all markets are of a certain total value (we want to use high value markets to demonstrate our tool), are relatively recently closed, and can be insider traded on (we will use our discretion for the purposes of this project).

Here we will use the Polymarket Gamma API to get information about the market such as the definitions of each outcome (what constitutes winning or losing the bet), the time the market was opened, the time the market was closed, and the total volume traded in the market. As well as the general information that would be helpful to the user, the Gamma API also gives us access to the CLOB ID and the market's condition ID, both of which will be helpful later on. 

We will then use the Polymarket CLOB API to fetch the price history for the trade time within a specified time period. We will allow the user to choose from a small set of specified time periods around significant events, such as the price history over the entire time the market was open, the week before and after a spike, and the day before and after a price spike. Because we will choose a few relevant informational events for our final delivarble for this class, we will define the dates of 'spikes' oursleves, for demonstrative purposes. We will communicate the price history using a line plot, which will offer an easy visual comparison to the Google trends plots we will produce. 

Inputs: The specified market slug (via market API), the market's CLOB ID (via Gamma API), a timestamp (polymarket uses unix timestamps, which can be easily converted from mm/dd/YY using the datetime package)

Outputs: Fundamental market information (start date, end date, rules, total volume, etc.) and line plot of price history over multiple time intervals.

## Market History - Flag Suspicious trades

After looking at the market information, we can see when the market changes notably, which we can use to flag suspicious trades. We will define a suspicious trade as a very large buy order before any large shift in the market that is ultimately succesful. We intend for this to flag many trades that are not insider trading, as a type II error (a failure to catch an insider trader) is much worse than a type I error (incorrectly flagging a legal trader as an insider trader). 

To search for trades within the market, we will use the trades API, which allows us to filter by market, size of trade, and date. After we have a list of trades that meet these conditions, we will iterate through the list and remove all trades which are not succesful.  

Inputs: Market condition ID (this is different from the CLOB ID, but also available from the Gamma API), date (unix, we will pre define the dates as mentioned earlier), size of trade (we will define this relatively, as the largest 1% of trades in the market), and the outcome of the market (we will know this).

Outputs: A list of trades that may be insider trading. 
 

## Google Trends - Track Outside World's Attention to the Market

## User History - Corroborate User's Past Behavior, Market History, and Google Trends and Report Level of Concern

## The Webpage

Our webpage is our main software component. This is what we present our story with. In our website, 
we turn complex trading disclosures into a clear and detailed presentation for any audience to view. 
Our dashboard will contain trades for a filtered period of time that the user wants to look at.
The user can filter towards any market that they are interested in and scroll through each separate trade.
For each trade block, we have a icon showing the probability that the trade can be identified as an insider trade,
as well as information on the trade such as the trade amount, what time, the market that the trade was made in, 
as well as user information and any other factor that might show the possibility of an insider trade.
Our site will also include real time alerts as trades get processed on our website to prioritize recent trades
that were flagged by our algorithm. 

This way users such as legal workers can utilize the dashboard by filtering specific times and markets, 
using the interactive trade blocks to view more recent and higher probability insider trades to investigate.
They can click into each trade block to see the data on the trade such as when the trade was made,
how much was traded and the user information, so they can see why our algorithm flagged it as a high probable 
insider trade. Using our dashboard, they can quickly spot suspicious trades and patterns, investigating unusual
trades around certain markets so they can shorten investigation time and hunt down insider trades quicker and focus
on catching them.

Our site will also include visual timelines of trades for each market, comparing the popularity of a market
in a time series chart which could raise higher suspiciouns.We plan to also have network maps of user trades 
to see their patterns on trading throughout markets, and simple trade summaries on when and how much they traded, 
legal investigators to further conduct investigations and use the pattern data to further identify and predict 
insider trades.


## Webpage sub components

- Main component is the dashboard containing trade blocks and visual representations of trades thoughout time
for a given filter of market and timestamp

- Trade blocks for each trade that happens for the given filters, containing data on each trade which 
users can click into including who made the trade, how much, and the probability it was an insider trade.

- Each trade block contains a color coded probability icon showing the probability it is insider trade so that 
any user who just wants to quickly skim and identify suspicious trades can quickly scroll and investigate the 
higher probability insider trades

- this is the story
- lead with a conclusion, because this is what's important to the non-technical user (binary yes/no we found insider trading)
- We describe the features that we think are a part of trades insider trading
- Then, we show a table with the trades that have these features, with clear color coding of their result (for the skimmer)
- At the bottom lies a link to "methodology" which *Wise Investor* clicks to see a detailed report
