# Riot API Win Rates

A project in which I wanted to use the data queried from Riot Games' API in order to generate win rates for a summoner's requested champion. My initial idea was to calculate their win rate from a large number of games with a quick search (unlike OP.GG which requires you to constantly load in more games one section at a time). However, this project is limited by Riot Games' API rate limits, so I can only query so many games at a time. It currently functions as intended within a certain limit. If I were to revisit this project to expand upon it, I would most-likely have to maintain my own database, or scrape information from a website like OP.GG to get all the data necessary. At the moment, this is how the program works:

![](https://i.imgur.com/jTZFGD5.png)

### Instructions:

This program requires you to input an API key from Riot Games. You can generate one on their developer website [here](https://developer.riotgames.com/). Then you simply need to provide:
- API key
- Server (Region)
- Summoner name
- Specific champion if desired
- Recent game to check up to a limit

You will then be provided with your desired win rate, alongside the number of remade games and total KDA for fun.

### Future Improvements:

If I am able to circumvent the rate limits in the future, I would add the following features:
- The ability to check which opponents you struggle most/least against (based on win rates, of course)
- Build paths that grant you the greatest success
- A functional UI. Maybe turn this into a web application
