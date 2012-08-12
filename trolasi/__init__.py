# -*- coding: utf-8 -*-

import re
import os
import string
import collections
from datetime import datetime

import requests
from flask import Flask, render_template, redirect, url_for
from raven.contrib.flask import Sentry


MAX_MINUTES = 90
SERVICE_URL = 'http://wbus.talktrack.com/wap.aspx?__ufps=026447'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) '
                         'Gecko/20090910 Ubuntu/9.04 (jaunty) Shiretoko/3.5.3'}
Station = collections.namedtuple('Station', 'number name buses')

# NAPOVED PRIHODOV ZA Bavarski dvor (058)
RE_STATION = re.compile(r'ZA\s*(.+?)\s*\((\d+)\)')
# ob 19:40.
RE_CUR_TIME = re.compile(r'ob (\d+:\d+)\.')
# 14 Vrhovci-Savlje:
RE_INFO_LINE = re.compile(r'(\d+)\s+(?:([A-Z])\s)?[^-]+-\s*([^:]+):')
# 14 Vrhovci-Savlje: n 19:01, n 19:22, n 19:41
RE_TIME = re.compile(r'[\sn]+(\d+:\d+),?')

app = Flask(__name__)
sentry = Sentry(dsn='https://2ebcb52af1b041e1a777fa02b3ee1b53:5ea300f455c'
                    '64741927fcf8f9c5ac965@app.getsentry.com/1928')


def calculate_times(dt, cur_time):
    """Sometimes a bus is behind the clock, make sure it should 0mins then"""
    mins = (dt - cur_time).seconds / 60
    # about 23 hours, this means bus is behind the clock
    if mins > 1400:
        return 0
    return mins


@app.route("/")
def index():
    from flask import request
    station = request.args.get('station', '')
    if station:
        # we redirect for GET with station info
        return redirect(url_for('station', station=station))
    return render_template('index.html')


@app.route("/<station>")
@app.route("/<station>/<bus>")
def station(station, bus=None):
    # cleanup
    station = station.strip()\
                     .replace('\n', '')\
                     .replace('\r', '')\
                     .encode('utf-8')

    payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'tb_postaja': station,
        'b_send': u'Prikaži',
    }

    try:
        r = requests.post(SERVICE_URL,
                          data=payload,
                          timeout=5,
                          headers=HEADERS)
    except requests.exceptions.RequestException:
        sentry.captureException()
        error = u'Podatki trenutno niso dosegljivi, poskusite kasneje.'
        return render_template('index.html', error=error)

    output = r.text

    if 'poizkusite znova' in output:
        error = u'Postaje s tem imenom/številko ni.'
        return render_template('index.html', error=error)

    # get current time of application to compute relative times
    cur_time = RE_CUR_TIME.search(output)
    if not cur_time:
        sentry.captureMessage(output)
        error = u'Vir podatkov je spremenil format, administrator je bil obveščen.'
        return render_template('index.html', error=error)
    else:
        cur_time = datetime.strptime(cur_time.groups()[0], '%H:%M')

    stations = []

    for part in output.split(u'NAPOVED PRIHODOV'):
        station_info = RE_STATION.search(part)
        if not station_info:
            continue
        buses = []
        name, number = station_info.groups()

        # get bus time arrivals
        for line in part.split('\n'):
            info = RE_INFO_LINE.search(line)
            if info:
                bus_number, bus_subnumber, direction = info.groups()
                if bus and bus_number != bus:
                    continue

                # parse arrival times into datetime
                arrival_times = map(lambda d: datetime.strptime(d, '%H:%M'),
                                    RE_TIME.findall(line))
                # calculate relative times
                arrival_times = map(lambda d: calculate_times(d, cur_time),
                                    arrival_times)
                # filter out too big times
                arrival_times = filter(lambda i: i < MAX_MINUTES,
                                       arrival_times)

                buses.append({
                    'bus_number': bus_number + (bus_subnumber or ''),
                    'direction': direction.lower().capitalize(),
                    'times': ', '.join(map(lambda s: str(s) + '"',
                                       arrival_times)) or u'Ni prihodov.',
                })
        stations.append(Station(name=name, number=number, buses=buses))

    return render_template('station.html',
                           stations=stations,
                           letters=string.letters)


if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):  # pragma: nocover
    sentry.init_app(app)

if __name__ == "__main__":  # pragma: nocover
    app.run(debug=True)
