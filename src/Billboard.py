import requests
from datetime import date

class Song:
    def __init__(self):
        self.artist = ''
        self.title = ''
        self.chart_pos = -1
        self.last_week = -1
        self.album_art_url = ''
        self.peak_pos = -1
        self.wks_on_chart = -1
        self.awards = []         # Not all songs will have awards

class Chart:
    def __init__(self):
        self.week = date.today()
        self.chart = []

    URL = 'https://www.billboard.com/charts/hot-100/'

    ARTICLE_TAG = '<article class="chart-row chart-row--'
    CHART_POSITION = '<span class="chart-row__current-week">'
    LAST_WEEK_POS = '<span class="chart-row__last-week">Last Week: '
    ARTIST = '<span class="chart-row__artist">'
    TITLE = '<h2 class="chart-row__song">'
    ALBUM_ART_URL = '<div class="chart-row__image" style="background-image: url('

    LABEL = '<span class="chart-row__label">'
    VALUE = '<span class="chart-row__value">'
    PEAK = 'Peak Position'
    WEEKS_ON_CHART = 'Wks on Chart'

    AWARDS_UL = '<ul class="fa-ul chart-row__awards">'
    AWARD_LI = '<li class="chart-row__awards-item">'
    AWARD_LI_END = '</i> '

    def download(self):

        # Convert week to string format
        week_str = self.week.isoformat()
        chart_url = Chart.URL + week_str

        # download html
        r = requests.get(week_str)
        if r.response_code != 200:
            # Ensure that the day of the week is a Saturday
            if self.week.weekday() != 5:
                days = 5 - self.week.weekday()
                days = days % 7
                timedelta = date(day=days)
                self.week = self.week + timedelta
            else:
                raise('unable to find chart for date ' + self.week.isoformat())

            # Convert week to string format
            week_str = self.week.isoformat()
            chart_url = Chart.URL + week_str

            # download html
            r = requests.get(week_str)
        html = r.text

        # compile chart
        for i in range(1, 101):
            tag = Chart.ARTICLE_TAG + str(i)
            start = html.index(tag)
            end = html.index('</article>', start)
            song_raw = html[start:end]

            song = Song()

            # Verify Chart position
            start = song_raw.index(Chart.CHART_POSITION) + len(Chart.CHART_POSITION)
            end = song_raw.index('</', start)
            pos = int(song_raw[start:end])
            if pos != i:
                raise('Chart position does not match. Parsed position was %(pos), expected was %(i)' % locals())
            song.chart_pos = pos

            # Get last weeks position
            start = song_raw.index(Chart.LAST_WEEK_POS) + len(Chart.LAST_WEEK_POS)
            end = song_raw.index('</', start)
            song.last_week = int(song_raw[start:end])

            # Get album art URL
            start = song_raw.index(Chart.ALBUM_ART_URL) + len(Chart.ALBUM_ART_URL)
            end = song_raw.index(')">', start)
            song.album_art_url = song_raw[start:end]

            # Get title
            start = song_raw.index(Chart.ARTIST) + len(Chart.ARTIST)
            end = song_raw.index('</h2>', start)
            song.artist = song_raw[start:end]

            # Get artist
            start = song_raw.index(Chart.ARTIST) + len(Chart.ARTIST)
            end = song_raw.index('</span>', start)
            song.artist = song_raw[start:end].strip()

            # Get peak position
            label = song_raw.index(Chart.LABEL + Chart.PEAK)
            start = song_raw.index(Chart.VALUE, label) + len(Chart.VALUE)
            end = song_raw.index('</', start)
            song.peak_pos = int(song_raw[start:end])

            # Get weeks on chart
            label = song_raw.index(Chart.LABEL + Chart.WEEKS_ON_CHART)
            start = song_raw.index(Chart.VALUE, label) + len(Chart.VALUE)
            end = song_raw.index('</', start)
            song.wks_on_chart = int(song_raw[start:end])

            # Get awards
            start = song_raw.index(Chart.AWARDS_UL) + len(Chart.AWARDS_UL)
            end = song_raw.index('</ul>', start)
            awards = song_raw[start:end].strip()
            lines = awards.split('\n')
            for line in lines:
                if line.startswith(Chart.AWARD_LI):
                    start = line.index(Chart.AWARD_LI_END) + len(Chart.AWARD_LI_END)
                    end = line.index('</li>', start)
                    song.awards.append(line[start:end])

            # Add song to chart
            self.chart.append(song)

        return self.chart
