# Insider Trading
## Group Members
Aaron Kann, Ian Chang, Jonathan Grothe, Josh Tseng 
## Project Type
I'm thinking Data Analysis, in the form of a blog post or a static webpage with visualizatons.
However, depending on how far we go, this could be a data presentation that allows for interactivity.

## Questions of interest

1. How often do trades occur on Polymarket that have the same characteristics
as the viral trade that occured directly before the Maduro kidnapping?

2. Do trades that share these characteristics win more often than they lose?

3. Do the market odds shift directly after bets with these characteristics occur
before news breaks, suggesting that other traders are monitoring trades in the
same fashion that we are attempting to and trading accordingly?

4. Are there features, that we've idenitified as suspicious and otherwise,
tend to occur in trades that consistently beat the market?

5. [future plan - might not get to in 5 weeks]
Are traders going to get wise to the fact that montioring systems such as ours
are tracking deals that look like blatant insider trading, and can we use machine
learning to track potential drift?

## Project Goal
Test the hypothesis that insider trading occurs in the poorly regulated 
online prediction market space 
and that these trades happen in such a blatant fashion
that there exist identifiable features that we can use to identify them.

## Data Sources

[polymarket API](https://docs.polymarket.com/developers/CLOB/timeseries)

[Unofficial Google Trends API](https://github.com/GeneralMills/pytrends), 
which worked when I used it in August 2025 so I hope it still works now

second data source is still up for air, and if that API doesn't work 
we can potentially use [Reddit](https://www.reddit.com/dev/api/) for this goal

## Project Roadmap and Milestones

### Part 1 - Exploration

  1. Explore the [Timeseries API](https://docs.polymarket.com/developers/CLOB/timeseries) and build a function that
     takes the time and bet and returns the price point
  2. Explore the [Trades API](https://docs.polymarket.com/developers/CLOB/trades/trades) and build a function that
      takes the trade and returns all the bets, and the time
  3. Explore the [Unofficial Google Trends API](https://github.com/GeneralMills/pytrends) and make sure it still works.
     Build a function that takes the name of a trade and returns an index that determine if relevant searches have spiked
     in the day/hour before the trade.  Note that trade name -> search query is non-trivial

  **Milestone** - a database with all bets from the Maduro trade with relevant features

### Part 2 - Minimum Viable Product

  1. Brainstorm our hypothesis by defining what features we think consitutue a suspisious trade
  2. Creating a website with a front-end that visualizes the trades and if they won
  3. Linking this website to detailed documentation of our process, that links to the GitHub

  **Milestone** - a website that details all the bets of just the Maduro Trade

### Part 3 - Fleshing It Out

  1. Create a large database of relevant bets (rn: 2026, markets that we think are insider trade-able)
  2. Use the data we have to reconsider the features we think consitiute insider trading by either
     a. Using ML to identify features that win more often, and creating a (% insider trading score)
     b. Hardcoding a (% insider trading score) and then using our data to confirm or deny our hypothesis
  3. Updating our website to better document our conclusions based on the data we have

     **Milestone** - a website, with a conclusion and supporting data, good enough for a final project

### Part 4 - Nice to Haves
  *NOTE: We probably will not get here in the next five weeks, and that's okay!*

  1. Figure out a way to use cloud compute and the [trades API](https://docs.polymarket.com/developers/CLOB/trades/trades)
     to analyze trades as they happen
  2. Use some other technology to notify ourselves and users when suspicious trades happen
  3. Figure out if flagged trades rise in price immediately following, suggesting that someone out there is trading
     based on the characteristics of other bettors and has identified similar features to ourselves
  4. Consider other features and test if they
       a) appear in flagged bets at a disproportional rate
       b) when they appear in flagged bets, if they help predict winning
  5. Account for drift in any models, as insider traders might notice visibility and change patterns accordingly
