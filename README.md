# Billboard2017

## Project Goals

The aim of this project is to create a way to easily pull down a single Billboard chart for a given week so that data can be analyzed. Specifically, I want to be able to knew what position a song or album is on a chart for a specific date. The intent is to create a graph displaying all of the songs that hit number one throughout the year 2017 and what other weeks they were on the chart and at what positions.

## Plan

Billboard does not have an active API as far as I can tell. The best bet seems to be to parse the HTML on the Hot 100 page to get information about each song. To do this, I will use the Requests Python library to download the HTML for a given week by visiting the url `https://www.billboard.com/charts/hot-100/YYYY-MM-DD` where `YYYY-MM-DD` is the date of the week for that chart. Then, I will parse the HTML for `<Article>` tags with `class=chart-row-X` where `X` is a row number representing the song's location in the chart. From this tag, I will be able to parse out information about the song and store it in a data structure. 

## Dependencies

* [Python Requests](http://docs.python-requests.org/en/master/)
* [Plotly](https://plot.ly/)
