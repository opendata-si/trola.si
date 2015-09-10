# -*- coding: utf-8 -*-

import collections
import simplejson
import os
import re
import sys
from datetime import datetime

import requests
import mimerender
from flask import Flask, render_template, redirect, url_for
from raven.contrib.flask import Sentry


MAX_MINUTES = 90
SERVICE_URL = 'http://wbus.lpp.si/wap.aspx?__ufps=026447'
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

mimerender = mimerender.FlaskMimeRender(global_charset='utf-8')


def render_json(**args):
    del args['template']
    return simplejson.dumps(args)


def render_html(**args):
    template = args['template']
    del args['template']
    return render_template(template, **args)

app = Flask(__name__)
sentry = Sentry(dsn='https://2ebcb52af1b041e1a777fa02b3ee1b53:5ea300f455c'
                    '64741927fcf8f9c5ac965@app.getsentry.com/1928')


def calculate_arrivals(dt, cur_time):
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


def station(station, bus=None):
    u"""Search for station and return information about matched stations.

    :param station: Name or number of the station
    :param bus: Filter buses in stations by this parameter
    :returns:
        HTML (by default)

        JSON (if HTTP request "Accept" header is "application/json")

    Description of returned data:

    **stations**
        List of objects that describe a station
    **stations -> number**
        Unique number of the station
    **stations -> name**
        Name of the station (not unique!)
    **stations -> buses**
        List of buses arriving to station
    **stations -> buses -> direction**
        Name of direction that bus is driving
    **stations -> buses -> number**
        Number of the bus, might be "1" or "1N"
    **stations -> buses -> arrivals**
        List of minutes of upcoming arrivals
    **error**
        If given, something went wrong when gathering information

    Following errors are possible:

    * Podatki trenutno niso dosegljivi, poskusite kasneje.
    * Nekaj je šlo narobe, administrator je bil obveščen.
    * Postaje s tem imenom/številko ni.
    * Vir podatkov je spremenil format, administrator je bil obveščen.

    Example::

        $ curl -iH "Accept: application/json" http://www.trola.si/bavarski
        {
            "stations": [{
                "number": "600012",
                "name": "BAVARSKI DVOR",
                "buses": [{
                    "direction": "Brod",
                    "number": "1N",
                    "arrivals": []
                }, {
                    "direction": "Vi\u017emarje",
                    "number": "1N",
                    "arrivals": []
                }, {
                    "direction": "Bavarski dvor",
                    "number": "1N",
                    "arrivals": [0]
                }, {
                    "direction": "Nove jar\u0161e",
                    "number": "2",
                    "arrivals": []
                }, {
                    "direction": "Gara\u017ea",
                    "number": "2",
                    "arrivals": [18]
                }, {
                    "direction": "Btc - bleiweisova",
                    "number": "27B",
                    "arrivals": []
                }]
            }, {
                "number": "600011",
                "name": "BAVARSKI DVOR",
                "buses": [{
                    "direction": "Bavarski dvor - gameljne",
                    "number": "1N",
                    "arrivals": []
                }, {
                    "direction": "Gara\u017ea",
                    "number": "2",
                    "arrivals": [8, 42]
                }, {
                    "direction": "Zelena jama",
                    "number": "2",
                    "arrivals": []
                }, {
                    "direction": "Be\u017eigrad ",
                    "number": "3G",
                    "arrivals": []
                }, {
                    "direction": "Gara\u017ea",
                    "number": "27",
                    "arrivals": []
                }]
            }]
        }

        $ curl -iH "Accept: application/json" http://www.trola.si/bavarski/1
        {
            "stations": [{
                "number": "600012",
                "name": "BAVARSKI DVOR",
                "buses": [{
                    "direction": "Brod",
                    "number": "1N",
                    "arrivals": []
                }, {
                    "direction": "Vi\u017emarje",
                    "number": "1N",
                    "arrivals": []
                }, {
                    "direction": "Bavarski dvor",
                    "number": "1N",
                    "arrivals": [0]
                }]
            }, {
                "number": "600011",
                "name": "BAVARSKI DVOR",
                "buses": [{
                    "direction": "Bavarski dvor - gameljne",
                    "number": "1N",
                    "arrivals": []
                }]
            }]
        }

        $ curl -iH "Accept: application/json" http://www.trola.si/bavarski
        {"error": 'Podatki trenutno niso dosegljivi, poskusite kasneje.'}

    """

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
        r.raise_for_status()
    except requests.exceptions.Timeout:
        error = u'Podatki trenutno niso dosegljivi, poskusite kasneje.'
        return dict(template='index.html', error=error)
    except requests.exceptions.RequestException:
        sentry.captureException()
        error = u'Nekaj je šlo narobe, administrator je bil obveščen.'
        return dict(template='index.html', error=error)

    output = r.text

    if 'poizkusite znova' in output:
        error = u'Postaje s tem imenom/številko ni.'
        return dict(template='index.html', error=error)

    # get current time of application to compute relative times
    cur_time = RE_CUR_TIME.search(output)
    if not cur_time:
        sentry.captureMessage('Vir podatkov je spremenil format', extra={'html': output})
        error = u'Vir podatkov je spremenil format, administrator je bil obveščen.'
        return dict(template='index.html', error=error)
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
                arrival_times = map(lambda d: calculate_arrivals(d, cur_time),
                                    arrival_times)
                # filter out too big times
                arrival_times = filter(lambda i: i < MAX_MINUTES,
                                       arrival_times)

                if u'garaža' in direction.lower() and not arrival_times:
                    continue

                buses.append({
                    'number': bus_number + (bus_subnumber or ''),
                    'direction': direction.lower().capitalize(),
                    'arrivals': arrival_times,
                })
        stations.append(Station(name=name, number=number, buses=buses))

    return dict(template='station.html', stations=stations)

if 'test' not in sys.argv[0]:
    station = mimerender(default='html', html=render_html, json=render_json)(station)
station = app.route("/<station>")(station)
station = app.route("/<station>/<bus>")(station)

if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):  # pragma: nocover
    sentry.init_app(app)

if __name__ == "__main__":  # pragma: nocover
    app.run(debug=True)
