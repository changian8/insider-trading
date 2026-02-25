# User Stories

## The Policy-Curious High Level Reader
- Wants:  A person who wants to quickly glance at the page and understand the conclusion that we drew
without getting into low-level details about our methodology and data

- Interaction Methods: They look at the webpage to learn, probably low tech, mostly cares about 
the conclusion more than the methodology.
Visual appeal matters to them, so use of green/red coloring to match the conclusion that our data

- Needs: An easily digestable story from us, a conclusion to understand

- Skills: might be low tech, low math, could have a legal background


## The Degenerate Tailer - Jordan B
- Wants: To know when insder trades happen as they happen, so that they could tail and make money

- Interaction Methods: some sort of live notification so he knows what's going down even
when not actively on the app

- Needs: our methodology to be accurate

- Skills: making money


## The Smart Investor - Warren B
- Wants: To make money, to understand our methodology so that he can build on it and maintain it

- Interaction Methods: not only a live notification, but also to interact with the data
as well as a detailed report about our methodology and a way to build on it (link to GitHub)

- Needs: a detailed explanation of what we did, our methods, live updates to see if our methods
are working in the real world, a way for him to interact the data to test his own hypothesis

- Skills: Making even more money, Math and Code and Basic Economics


# Use Cases

## The Legislator

- Opens the website and reads the story
- They then try to understand our argument, although they might skim and only read titles and pictures
- He then sends the website to his friends so they can read it

## The Degen

- He might read the website, or he might not

- He gets a notification on his phone
- He then reads it, only to understand what to bet on.  Details are not that important to him,
although he might want to know
- He then goes to a trading site of choice and makes a bet based on what we said would work
(possibly we link to polymarket to this easier for them)

(we probably should warn him about the dangers of a gambling addiction)

## The Wise Investor

- He reads the website thoroughly, and he does so to understand our methodology
- He looks at the data so that he can make his own hypotheses about what might be trading

- He gets a notification, but he questions our reasoning before he bets
- So, we redirect him to somewhere he can make his own opinon based on all the available data
- We could (time dependant) make a report, or we can just him to Polymarket if they show the relevant
data in one page 

# Components

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

## Methodolgy
- detailed, good writing, maybe a link to the repo

## The Notification

- We have to stick to one, how TBD
Ideas: 
- email
- discord bot
- twitter bot

- The Notification is not very detailed! A red flag, and the thing we think is gonna happen at most
- The link goes to our app, which gives the user a more detailed view on the features of this bet and our analysis

