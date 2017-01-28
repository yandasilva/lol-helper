# League Of Legends Helper Script
This script was created on Python 2.7.10. It uses Beautiful Soup 4 to scrape web pages in order to quickly fetch champion matchup info and builds.

## Info
- Matchup info is scraped from [League Of Legends Counter](http://www.lolcounter.com/), while builds are scraped from [Champion.GG](http://champion.gg/);
- The script presents the 10 best and 10 worst pics against the target champion;
- By default, the script fetches the most popular build (Runes, Masteries, Summoner Spells, Starting Items and Core Build) for the target champion.

## Usage
The `playing.py` file should be run as follows:
```
./playing.py [--against] [--winrate] <champion name>
```

- `--against`: use this argument if you are playing against the desired champion and want their matchup info (best and worst pics) according to [League Of Legends Counter](http://www.lolcounter.com/);
- `--winrate`: use this argument if you want the best win rate build for a champion instead of their most popular one;
- `<champion name>`: type in the name of the target champion, whithout the `< >` simbols. Spaces, special characters and capitalization are ignored, but, aside from those, a mistyped champion name will result in an error message.
