import requests
from datetime import date
import os


class Song:
    def __init__(self):
        self.artist = ''
        self.title = ''
        self.chart_pos = -1
        self.last_week = -1
        self.album_art_url = ''
        self.peak_pos = -1
        self.wks_on_chart = -1
        self.awards = []  # Not all songs will have awards

    def __str__(self):
        out = ''
        out += 'Chart position: ' + str(self.chart_pos) + os.linesep
        out += 'Title: ' + self.title + os.linesep
        out += 'Artist: ' + self.artist + os.linesep
        out += 'Last week: ' + str(self.last_week) + os.linesep
        out += 'Weeks on chart: ' + str(self.wks_on_chart) + os.linesep
        out += 'Peak: ' + str(self.peak_pos) + os.linesep
        out += 'Album Art url: ' + self.album_art_url + os.linesep
        out += 'Awards: ' + os.linesep
        for a in self.awards:
            out += '\t' + a + os.linesep
        return out


class Hot100Chart:
    def __init__(self):
        self.week = date.today()
        self.chart = []

    __URL = 'https://www.billboard.com/charts/hot-100/'

    __ARTICLE_TAG = '<article class="chart-row chart-row--'
    __CHART_POSITION = '<span class="chart-row__current-week">'
    __LAST_WEEK_POS = '<span class="chart-row__last-week">Last Week: '
    __ARTIST = 'class="chart-row__artist"'
    __TITLE = '<h2 class="chart-row__song">'
    __ALBUM_ART_URL = '<div class="chart-row__image" style="background-image: url('

    __LABEL = '<span class="chart-row__label">'
    __VALUE = '<span class="chart-row__value">'
    __PEAK = 'Peak Position'
    __WEEKS_ON_CHART = 'Wks on Chart'

    __AWARDS_UL = '<ul class="fa-ul chart-row__awards">'
    __AWARD_LI = '<li class="chart-row__awards-item">'
    __AWARD_LI_END = '</i> '

    def download(self):

        # Convert week to string format
        week_str = self.week.isoformat()
        chart_url = Hot100Chart.__URL + week_str

        # download html
        r = requests.get(chart_url)
        if r.status_code != 200:
            # Ensure that the day of the week is a Saturday
            if self.week.weekday() != 5:
                days = 5 - self.week.weekday()
                days = days % 7
                timedelta = date(day=days)
                self.week = self.week + timedelta
            else:
                raise ('unable to find chart for date ' + self.week.isoformat())

            # Convert week to string format
            week_str = self.week.isoformat()
            chart_url = Hot100Chart.__URL + week_str

            # download html
            r = requests.get(chart_url)
        html = r.text

        # compile chart
        for i in range(1, 101):
            tag = Hot100Chart.__ARTICLE_TAG + str(i)
            start = html.index(tag)
            end = html.index('</article>', start)
            song_raw = html[start:end]

            song = Song()

            # Verify Chart position
            start = song_raw.index(Hot100Chart.__CHART_POSITION) + len(Hot100Chart.__CHART_POSITION)
            end = song_raw.index('</', start)
            pos = int(song_raw[start:end])
            if pos != i:
                raise ('Chart position does not match. Parsed position was %(pos), expected was %(i)' % locals())
            song.chart_pos = pos

            # Get last weeks position
            start = song_raw.index(Hot100Chart.__LAST_WEEK_POS) + len(Hot100Chart.__LAST_WEEK_POS)
            end = song_raw.index('</', start)
            try:
                song.last_week = int(song_raw[start:end])
            except ValueError:
                song.last_week = -1

            # Get album art URL
            if song_raw.__contains__(Hot100Chart.__ALBUM_ART_URL):
                start = song_raw.index(Hot100Chart.__ALBUM_ART_URL) + len(Hot100Chart.__ALBUM_ART_URL)
                end = song_raw.index(')">', start)
                song.album_art_url = song_raw[start:end]

            # Get title
            start = song_raw.index(Hot100Chart.__TITLE) + len(Hot100Chart.__TITLE)
            end = song_raw.index('</h2>', start)
            song.title = song_raw[start:end]

            # Get artist
            start = song_raw.index(Hot100Chart.__ARTIST) + len(Hot100Chart.__ARTIST)
            start = song_raw.index('>', start) + 1
            end = song_raw.index('</', start)
            song.artist = song_raw[start:end].strip()

            # Get peak position
            label = song_raw.index(Hot100Chart.__LABEL + Hot100Chart.__PEAK)
            start = song_raw.index(Hot100Chart.__VALUE, label) + len(Hot100Chart.__VALUE)
            end = song_raw.index('</', start)
            song.peak_pos = int(song_raw[start:end])

            # Get weeks on chart
            label = song_raw.index(Hot100Chart.__LABEL + Hot100Chart.__WEEKS_ON_CHART)
            start = song_raw.index(Hot100Chart.__VALUE, label) + len(Hot100Chart.__VALUE)
            end = song_raw.index('</', start)
            song.wks_on_chart = int(song_raw[start:end])

            # Get awards
            if song_raw.__contains__(Hot100Chart.__AWARDS_UL):
                start = song_raw.index(Hot100Chart.__AWARDS_UL) + len(Hot100Chart.__AWARDS_UL)
                end = song_raw.index('</ul>', start)
                awards = song_raw[start:end].strip()
                lines = awards.split('\n')
                for line in lines:
                    if line.startswith(Hot100Chart.__AWARD_LI):
                        start = line.index(Hot100Chart.__AWARD_LI_END) + len(Hot100Chart.__AWARD_LI_END)
                        end = line.index('</li>', start)
                        song.awards.append(line[start:end])

            # Add song to chart
            self.chart.append(song)

        return self.chart
