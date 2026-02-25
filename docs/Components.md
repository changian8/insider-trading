# Components 

## The Webpage

Our webpage is our main software component. This is what we present our story with. In our website, 
we turn a multitude of complex trading disclosures into a clear and detailed presentation for any audience to view. 
Our dashboard will contain information on trades in specified markets that we have determined may have demonstrative value. 
The user can select any market that they are interested in and scroll through a number of trades made in that market.
For each trade, we have a icon showing the probability that the trade can be identified as an insider trade,
as well as information on the trade such as the trade amount, what time the trade was made, the market that the trade was made in, 
as well as user information and any other factor that might show the possibility of an insider trade.
Our site has the capability of being expanded to include real time alerts as trades get processed on our website to prioritize recent trades
that were flagged by our algorithm. 

This way users such as legal workers can utilize the dashboard by filtering specific times and markets, 
using the interactive trade blocks to view more recent and higher probability insider trades to investigate.
They can click into each trade block to see the data on the trade such as when the trade was made,
how much was traded and the user information, so they can see why our algorithm flagged it as a high probable 
insider trade. Using our dashboard, they can quickly spot suspicious trades and patterns, investigating unusual
trades around certain markets so they can shorten investigation time and hunt down insider trades quicker and focus
on catching them.

Our site will also include visual timelines of trades for each market, comparing the popularity of a market as according to Google trends
in a time series chart which could raise higher suspiciouns. We plan to also have network maps of select user trades 
to see their patterns on trading throughout markets, and simple trade summaries on when and how much they traded, 
legal investigators to further conduct investigations and use the pattern data to further identify and predict 
insider trades.

More specifically, our webpage will consist of the following subcomponents: 

### Market Information

First we will use the Polymarket markets API to filter markets to find the ones we are most interested in, and storing their market slugs so we can access their histories. We will ensure that all markets are of a certain total value (we want to use high value markets to demonstrate our tool), are relatively recently closed, and can be insider traded on (we will use our discretion for the purposes of this project).

From here we will use the Polymarket Gamma API to get information about the market such as the definitions of each outcome (what constitutes winning or losing the bet), the time the market was opened, the time the market was closed, and the total volume traded in the market. As well as the general information that would be helpful to the user, the Gamma API also gives us access to the CLOB ID and the market's condition ID, both of which will be helpful later on. 

We will then use the Polymarket CLOB API to fetch the price history for the trade time within a specified time period. We will allow the user to choose from a small set of specified time periods around significant events, such as the price history over the entire time the market was open, the week before and after a spike, and the day before and after a price spike. Because we will choose a few relevant informational events for our final delivarble for this class, we will define the dates of 'spikes' oursleves, for demonstrative purposes. We will communicate the price history using a line plot, which will offer an easy visual comparison to the Google trends plots we will produce. 

Inputs: The specified market slug (via market API), the market's CLOB ID (via Gamma API), a timestamp (polymarket uses unix timestamps, which can be easily converted from mm/dd/YY using the datetime package)

Outputs: Fundamental market information (start date, end date, rules, total volume, etc.) and line plot of price history over multiple time intervals.

### Market History - Flag Suspicious trades

After looking at the market information, we can see when the market changes notably, which we can use to flag suspicious trades. We will define a suspicious trade as a very large buy order before any large shift in the market that is ultimately succesful. We intend for this to flag many trades that are not insider trading, as a type II error (a failure to catch an insider trader) is much worse than a type I error (incorrectly flagging a legal trader as an insider trader). 

To search for trades within the market, we will use the trades API, which allows us to filter by market, size of trade, and date. After we have a list of trades that meet these conditions, we will iterate through the list and remove all trades which are not succesful.  

Inputs: Market condition ID (this is different from the CLOB ID, but also available from the Gamma API), date (unix, we will pre define the dates as mentioned earlier), size of trade (we will define this relatively, as the largest 1% of trades in the market), and the outcome of the market (we will know this).

Outputs: A list of trades that may be insider trading, stored in a JSON object which will contain the size of the trade, the date of the trade, and the user who made the trade, among other things. 

### User History - Determine if a User Shows Behavior That Might Indicate Insider Trading

With the list of flagged trades from the previous step, we will now use the trades API to fetch all trades for the specified user. We hypothesize that an insider trader is most likely to only make high value trades when they know what the outcome of the market will be, and are less likely to trade in general. For each user, we will estimate a suspicion score using these criteria. This suspicion score will be based only on our intuition, unfortunately, as the trades we were most interested in when we began this project are not accessible because the accounts that made them have been deleted. For efficiency, and because we do not want to create an involved metric that is not empirical, we will only use simple checks, such as the number of trades the user has made in total, the number of trades before the suspicious trade, and the number of trades of size 90% or higher than the suspicious trade. For each trade we will note each of these metrics and store them in a list, which we will then store in a data frame with rows as unique trades.

Inputs: Our JSON of suspicious trades, from which we will fetch each suspicious user.

Outputs: A dataframe which contains how the user who placed each trade scores on each metric. 

### Google Trends - Track Outside World's Attention to the Market

Google trends will allow us to contextualize the behavior of the market beyond what we can see in the price history. For each market, we will define a set of relevant search terms that we think best indicate the general popularity (as defined by the amount of times it shows up in Google searches) of the essential elements of the market. We will then plot this on a line plot which we can display next to the price history. Since the scale of Google trends is relative to the maximum popularity of the topic, we will scale the line plot as visually appropriate (and make a note to users to avoid confusion). 

Inputs: Pre defined search terms for each market.

Outputs: A line plot of the popularity of those search terms over the time the market was open. 

### Suspicion Score - Combining The Previous Elements to Report Trades We Think Are Suspicious

From the dataframe obtained in the user history step, we will filter trades that meet certain criteria and report them as suspicious. For simplicity, we will aim to report the most suspicious five to ten trades for each market. This will allow us to create a clear report for our users who are most intersted in the results, and will allow us to clearly explain our methodology to our users who want to expand on our project themselves.

Once we have selected our suspicious trades we will write a short report on why we arrived on that conclusion. This will walk through the aforementioned crietria in the user history and market history steps.

Inputs: Our data frame of user suspicion levels.

Outputs: A small set of suspicious trades

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
