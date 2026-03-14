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
~~which worked when I used it in August 2025 so I hope it still works now~~
which works as of deployment (3/12/2026); if it ceases to work, we discussed other
alternatives in our [tech review](docs\technology-review\technology_review.md).

## Running Our Code

### Backend (Python)

### Frontend (HTML/JSS/CS)
The frontend itself has no dependancies, however there are dev dependancies if you wanted to
run either the linter (eslint) or the testing (jest).

In order to install the dependances, tun the following:

```
cd src 
npm install
```

and then 
```
npx lint
```

to run the linter and/or 

```
npm test
```

to run the tests.  
