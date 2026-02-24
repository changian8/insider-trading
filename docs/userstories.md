# User Stories

## The Policy-Minded High Level Reader
- Wants:  A person who wants to open our page and understand the conclusion that we drew
without getting into low-level details about our methodology and data

- Interaction Methods: 
They look at the webpage to learn, probably low tech, mostly cares about 
the conclusion more than the methodology.
Visual appeal matters to them, so use of green/red coloring to match the conclusion that our data

- Needs: An easily digestable story from us, a conclusion to understand,
a visually appealing webpage, precise definition of any terms related to trading
and no unprofessional slang that could be misinterpreted by those outside of the trading subculture

- Skills: might be low tech, low math, could have a legal background


## The Opportunist and Data Explorer
- Wants: 
To figure out which features we believe to be indicative of insider trading,
to explore the data and draw their own conclusions.

- Interaction Methods:  
Interacts with the data we collected in order to backtest their own hypothesis about which trades win more than usual.

- Needs: 
A way to filter the data we have based on their own theories.
An easy-to-understand visual cue as to if the trades they filtered tend to win more than expected.
(both in terms of win % and alpha=(money won)/(money bet))

- Skills: 
Understands basic terminology when it comes to investing and trading,
especially terms unique to the subculture
has their own theories as to which features are a likely signal of insider trading


## The Scientist and Builder
- Wants: To understand our methodology thoroughly such that they could eventually
attempt to reproduce our results on the next batch of available data,
understand what we did to the level that they could fully support our reasoning or make changes if they had a critique, 
and, if they felt so inclined, implement our final vision of a live tracker on their own


- Interaction Methods: 
Reads every word on the page thoroughly as they seek to understand what we did.

- Needs: 
A link to the GitHub or links to a secondary page if we chose to spare certain
low-level details on the main report that were relevant to someone trying to recreate what we did,
and becuase they are checking our work because 
likely more experienced and frankly smarter than the four college students creating this. 

Our software engineering best practices are useful to them as a means to an end, 
the end being that they can reproduce locally and further build off of our code,
but we don't need to thoroughly justify our choices in best practices.

- Skills: 
Knows their way both around Git/coding and 
understands very high-level economic concepts surrounding trading.


# Use Cases

## The Policy-Curious High Level Reader

- They open the website and look for visual cues in order to understand the high level argument we made
 ("We found/did not find evidence of blatant insider trading on a mass scale")
  In practice, this looks like a reading the **bold title** on the top of the page that tells the user what
  we are trying to go for, and then it looks like reading the summary after.  
  Color (of the words, of the background, the **green and red of the table columns indicating that the bets are winning more or less than usual**) are very important to helping this person understand our argument

  They don't really pay close attention to our justifications of feature choices and low-level explanations.

## The Opportunist, or Data Explorer

- The opportunist is mildly interested in the title, methodology, and especially our conclusion.
However, the opportunist is most interested in exploring the **data table**.

- For the opportunist, a **form above the data table allowing them to customize the fields we considered to be insider trading**
is the feature that they will be speding their time on our report using.  
The opportunist will input filters based on their own previous assumptions, and after the data is filtered, they will look at the
**calculated values for win percentage and backtested alpha** based on the data that we were able to provide

- The opportunist also needs to understand what exactly these features are (at a high level).
Therefore, we will include an **information button next to the table header with written out explanations as to what the features are at a high level**.
The opportunist doesn't really care about how these features are exactly calculated, so we can leave that in the written report for the Scientist to read through. 

*See the ethical note on the bottom of the page as to how we will implement guardrails thatwe hope provides the wrong type of opportunist with the support they need.*

## The Scientist and Builder

The scientist and the builder plans on reading every word of the written report.
They care deeply about 
    - our original hypothesis as to which metrics signal potential insider trading
    - how each metric presented is derived on a low level
    - how we collected the data we chose to present in great detail
    - our opinions on the limiations of our work, although they will form their own as well

Underneath the interactive data component we will include a **write up** which 
explains these components of our research at a low-level that we believe the first two users wouldn't care to read.

We will also include the **link to our GitHub** at the very bottom of the page, such that they can review our
code and feel free to fork and build on it as they'd like. 

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
*For future implementation.  Will not be done by the end of DSE515*





# Ethical Note:

Gambing addition is a serious disease, and it would be an ethical failure on our end to create a project that enables 
those with a serious addiction without putting up the proper guardrails in place.  

**The overall purpose of this project is to expose what we believe to be a poorly regulated system that enables fraud that hurts the working class at the expense of the already powerful and well-connected**,
and while we acknowledge 
that it is impossible to create this project in a way without giving a certain type of user ideas as to how they 
could monetarily benefit from our research (quite frankly, the thought has crossed my mind a couple of times), 
we must resist the temptation to chase monetary gain at the expense of this greater goal. 

As to what this looks like in practice, we should be very clear about the shortcomings of our reserach.
We must make it abundantly clear that just becuase a trading strategy backtests successfully does not mean
it is guaranteed to succeed in the future - in fact, very far from it - with a **warning at the top of the page**
that states this very clearly such that anyone skimming the page (as to how we expect the Opportunist to interact with it)
and, if feasible, a link to **resources to help those suffering from addiction**. 

