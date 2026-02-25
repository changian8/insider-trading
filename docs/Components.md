## Components 

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
