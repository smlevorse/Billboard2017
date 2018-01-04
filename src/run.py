from Billboard import Hot100Chart, Song
from datetime import date, timedelta
import html

from plotly import __version__
from plotly import offline
from plotly import graph_objs

# download all charts for 2017
charts = []
lists = []

d = date(month=1, day=7, year=2017)
delta = timedelta(days=7)

while d.year == 2017:
    c = Hot100Chart()
    c.week = d
    chart = c.download()
    charts.append(c)
    lists.append(chart)
    d = d + delta

# Get a list of the number 1 songs
top_songs = []
for i in range(len(lists)):
    title = lists[i][0].title
    if title not in top_songs:
        top_songs.append(title)

song_positions = {}

for t in top_songs:
    chart_pos = []
    for i in range(len(lists)):
        pos = None
        for s in lists[i]:
            if s.title == t:
                pos = s.chart_pos
                break;
        chart_pos.append(pos)
    song_positions[html.unescape(t)] = chart_pos

# Get the weeks the charts were pulled from
weeks = [chart.week for chart in charts]

traces = []
colorind = 0
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#34495e', '#27ae60']
for title, positions in song_positions.items():
    trace = graph_objs.Scatter(
        x=weeks,
        y=positions,
        mode='lines+markers',
        name=title,
        line=dict(
            color=colors[colorind % len(colors)]
        )
    )
    traces.append(trace)
    colorind += 1

layout = graph_objs.Layout(
    yaxis=dict(
        range=[100, 0],
        zeroline=False,
        title='Chart position',
        titlefont=dict(
            family='"Open Sans", sans-serif',
            size=14
        )
    ),
    xaxis=dict(
        title='Week',
        titlefont=dict(
            family='"Open Sans", sans-serif',
            size=18
        )
    ),
    title="Top Tracks of 2017",
    titlefont=dict(
        family='"Open Sans", sans-serif',
        size=36
    )
)

fig = graph_objs.Figure(data=traces, layout=layout)

offline.plot(fig, filename='Hot100TopTracks.html')
print('done!')
