## Project Roadmap and Milestones

## Part 1 - Exploration

  1. Explore the [Timeseries API](https://docs.polymarket.com/developers/CLOB/timeseries) and build a function that
     takes the time and bet and returns the price point
  2. Explore the [Trades API](https://docs.polymarket.com/developers/CLOB/trades/trades) and build a function that
      takes the trade and returns all the bets, and the time
  3. Explore the [Unofficial Google Trends API](https://github.com/GeneralMills/pytrends) and make sure it still works.
     Build a function that takes the name of a trade and returns an index that determine if relevant searches have spiked
     in the day/hour before the trade.  Note that trade name -> search query is non-trivial

  **Milestone** - a database with all bets from the Maduro trade with relevant features

## Part 2 - Minimum Viable Product

  1. Brainstorm our hypothesis by defining what features we think consitutue a suspisious trade
  2. Creating a website with a front-end that visualizes the trades and if they won
  3. Linking this website to detailed documentation of our process, that links to the GitHub

  **Milestone** - a website that details all the bets of just the Maduro Trade

## Part 3 - Fleshing It Out

  1. Create a large database of relevant bets (rn: 2026, markets that we think are insider trade-able)
  2. Use the data we have to reconsider the features we think consitiute insider trading by either
     a. Using ML to identify features that win more often, and creating a (% insider trading score)
     b. Hardcoding a (% insider trading score) and then using our data to confirm or deny our hypothesis
  3. Updating our website to better document our conclusions based on the data we have

     **Milestone** - a website, with a conclusion and supporting data, good enough for a final project

## Part 4 - Nice to Haves
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

  **Milestone** - we make billions of dollars trading, go viral, get Polymarket banned for good and some traders thrown in jail, etc.  
  still probably would't get a summer internship tho
