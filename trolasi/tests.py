# -*- coding: utf-8 -*-
import unittest
import mock
from datetime import datetime


FIXTURE = u"""
NAPOVED PRIHODOV ZA BAVARSKI DVOR (600012)
1 N BAVARSKI DVOR - VIŽMARJE: 04:50
1 N BAVARSKI DVOR - BROD: 23:40, 00:20, 02:50
1 N GAMELJNE - BAVARSKI DVOR: 23:36, 00:15
2 ZELENA JAMA - GARAŽA: 00:41
2 ZELENA JAMA - NOVE JARŠE: 14:40, 15:09, 15:39
3 N RUDNIK - BAVARSKI DVOR: 21:17, 21:37, 21:57
3 N BAVARSKI DVOR - ŠKOFLJICA: 04:50
3 N BAVARSKI DVOR - RUDNIK: 21:20, 21:40, 22:00
3 G BEŽIGRAD - GROSUPLJE: 16:34, 18:45, 20:50
5 N ŠTEPANJSKO NAS. - PODUTIK: 20:58, 21:27, 21:29
6 ČRNUČE - DOLGI MOST: n 14:53, 15:31, 15:51
6 ČRNUČE - GARAŽA: 00:51
6 B ČRNUČE - NOTRANJE GORICE: n 15:13, 15:28, 17:12
7 NOVE JARŠE - GARAŽA: 22:35, n 22:59
7 NOVE JARŠE - PRŽAN: 14:54, 15:24, n 15:55
7 L LETALIŠKA - PRŽAN: 05:54, 06:09, 06:26
8 BRNČIČEVA - GAMELJNE: 04:56, 05:15, 05:19
9 ŠTEPANJSKO NAS. - GARAŽA: 22:42, 23:03
9 ŠTEPANJSKO NAS. - TRNOVO: 14:42, 15:11, 15:41
11 JEŽICA - ZALOG: 05:06, 05:08, 05:27
11 BEŽIGRAD - ZALOG: 23:38, 00:17, 02:50
14 SAVLJE - VRHOVCI: n 14:44, n 15:44, n 16:44
14 SAVLJE - GARAŽA: n 22:31, n 22:57, 08:36
14 B SAVLJE - BOKALCE: n 15:14, n 16:13, 17:08
19 I TOMAČEVO - GARAŽA: 08:18, 08:58, 09:28
19 I TOMAČEVO - IG: 14:51, 16:51, 17:03
19 B TOMAČEVO - JEZERO: n 15:51, n 17:51, n 19:51
20 NOVE STOŽICE - FUŽINE: 05:12, 05:27, 05:42
20 Z NOVE STOŽICE - ZALOG: n 14:59, 15:29, 15:59
23 KOLODVOR - ZOO: n 16:01, n 17:01, 09:02
25 ZADOBROVA - GARAŽA: 23:26
25 ZADOBROVA - MEDVODE: n 14:53, 15:58, 17:03
27 K KOLOSEJ - GARAŽA: 00:11
27 K KOLOSEJ - BLEIWEISOVA: 16:41, 17:22, 18:17
27 LETALIŠKA - BTC - NS RUDNIK: 05:11, 05:33, 05:36
NAPOVED PRIHODOV ZA BAVARSKI DVOR (600011)
1 N MESTNI LOG - BAVARSKI DVOR - GAMELJNE: 22:33, 23:03
2 NOVE JARŠE - ZELENA JAMA: 14:47, 15:11, 15:16
2 NOVE JARŠE - GARAŽA: 00:31, 01:05
3 G GROSUPLJE - BEŽIGRAD : 16:13, 18:25, 20:33
5 N PODUTIK - ŠTEPANJSKO NAS.: 21:30, 22:00, 22:29
6 B NOTRANJE GORICE - DM - ČRNUČE: 16:31, 18:30, 20:21
6 B NOTRANJE GORICE - GARAŽA: 23:28
6 B NOTRANJE GORICE - ČRNUČE: 05:29, 05:58, 06:30
6 DOLGI MOST - ČRNUČE: n 14:52, 15:05, 15:10
6 DOLGI MOST - GARAŽA: 00:51
7 PRŽAN - NOVE JARŠE: 14:46, n 15:15, 15:45
7 L PRŽAN - LETALIŠKA: 05:14, 05:29, 05:44
8 GAMELJNE - BRNČIČEVA: 05:30, 05:40, 05:50
9 TRNOVO - ŠTEPANJSKO NAS.: 14:44, 15:11, 15:22
9 TRNOVO - GARAŽA: 22:33, 22:53
11 ZALOG - BEŽIGRAD: 22:49, 23:17, 00:02
11 ZALOG - JEŽICA: 05:28, 05:43, 06:03
11 ZALOG - GARAŽA: 23:35, 00:40, 01:19
13 SOSTRO - GARAŽA: 22:19, 23:18
13 SOSTRO - CENTER STOŽICE: 15:46, 17:16, 18:41
14 B BOKALCE - SAVLJE: n 15:05, n 16:05, n 17:06
14 VRHOVCI - SAVLJE: n 14:50, n 15:35, n 16:34
14 B BOKALCE - GARAŽA: 22:32
14 VRHOVCI - GARAŽA: n 22:58
19 I IG - TOMAČEVO: 15:58, 17:59, 19:58
19 B JEZERO - TOMAČEVO: n 15:13, n 17:13, n 19:14
19 B JEZERO - GARAŽA: 23:34
20 FUŽINE - NOVE STOŽICE: 05:14, 05:31, 05:46
20 Z ZALOG - NOVE STOŽICE: 14:51, 15:18, 15:49
23 ZOO - KOLODVOR: n 16:29, n 17:29, 19:30
25 MEDVODE - ZADOBROVA: 14:54, 15:16, n 15:59
27 NS RUDNIK - BTC - LETALIŠKA: 05:28, 05:52, 06:18
27 K BLEIWEISOVA - KOLOSEJ: 16:14, 16:55, 17:35
Napovedi so bile izračunane ob 14:38.
Časi, označeni s črko n , pomenijo prihode nizkopodnih avtobusov,
na katere je lažje vstopiti.
Nazaj
"""

FIXTURE2 = """
Postaje s tem imenom nismo našli, poizkusite znova!
Nazaj
"""


class stationTests(unittest.TestCase):

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    def test_station_multiple(self, mock_render_template, mock_post):
        from . import station, Station
        mock_post().text = FIXTURE

        station('bavarski')

        mock_render_template.assert_called_with(
            'station.html',
            letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            stations=[
                Station(number=u'600012',
                        name=u'BAVARSKI DVOR',
                        buses=[{'direction': u'Vi\u017emarje', 'bus_number': u'1N', 'times': u'Ni prihodov.'},
                               {'direction': u'Brod', 'bus_number': u'1N', 'times': u'Ni prihodov.'},
                               {'direction': u'Bavarski dvor', 'bus_number': u'1N', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'2', 'times': u'Ni prihodov.'},
                               {'direction': u'Nove jar\u0161e', 'bus_number': u'2', 'times': '2", 31", 61"'},
                               {'direction': u'Bavarski dvor', 'bus_number': u'3N', 'times': u'Ni prihodov.'},
                               {'direction': u'\u0160kofljica', 'bus_number': u'3N', 'times': u'Ni prihodov.'},
                               {'direction': u'Rudnik', 'bus_number': u'3N', 'times': u'Ni prihodov.'},
                               {'direction': u'Grosuplje', 'bus_number': u'3G', 'times': u'Ni prihodov.'},
                               {'direction': u'Podutik', 'bus_number': u'5N', 'times': u'Ni prihodov.'},
                               {'direction': u'Dolgi most', 'bus_number': u'6', 'times': '15", 53", 73"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'6', 'times': u'Ni prihodov.'},
                               {'direction': u'Notranje gorice', 'bus_number': u'6B', 'times': '35", 50"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'7', 'times': u'Ni prihodov.'},
                               {'direction': u'Pr\u017ean', 'bus_number': u'7', 'times': '16", 46", 77"'},
                               {'direction': u'Pr\u017ean', 'bus_number': u'7L', 'times': u'Ni prihodov.'},
                               {'direction': u'Gameljne', 'bus_number': u'8', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'9', 'times': u'Ni prihodov.'},
                               {'direction': u'Trnovo', 'bus_number': u'9', 'times': '4", 33", 63"'},
                               {'direction': u'Zalog', 'bus_number': u'11', 'times': u'Ni prihodov.'},
                               {'direction': u'Zalog', 'bus_number': u'11', 'times': u'Ni prihodov.'},
                               {'direction': u'Vrhovci', 'bus_number': u'14', 'times': '6", 66"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'14', 'times': u'Ni prihodov.'},
                               {'direction': u'Bokalce', 'bus_number': u'14B', 'times': '36"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'19I', 'times': u'Ni prihodov.'},
                               {'direction': u'Ig', 'bus_number': u'19I', 'times': '13"'},
                               {'direction': u'Jezero', 'bus_number': u'19B', 'times': '73"'},
                               {'direction': u'Fu\u017eine', 'bus_number': u'20', 'times': u'Ni prihodov.'},
                               {'direction': u'Zalog', 'bus_number': u'20Z', 'times': '21", 51", 81"'},
                               {'direction': u'Zoo', 'bus_number': u'23', 'times': '83"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'25', 'times': u'Ni prihodov.'},
                               {'direction': u'Medvode', 'bus_number': u'25', 'times': '15", 80"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'27K', 'times': u'Ni prihodov.'},
                               {'direction': u'Bleiweisova', 'bus_number': u'27K', 'times': u'Ni prihodov.'},
                               {'direction': u'Btc - ns rudnik', 'bus_number': u'27', 'times': u'Ni prihodov.'}]),
                Station(number=u'600011',
                        name=u'BAVARSKI DVOR',
                        buses=[{'direction': u'Bavarski dvor - gameljne', 'bus_number': u'1N', 'times': u'Ni prihodov.'},
                               {'direction': u'Zelena jama', 'bus_number': u'2', 'times': '9", 33", 38"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'2', 'times': u'Ni prihodov.'},
                               {'direction': u'Be\u017eigrad ', 'bus_number': u'3G', 'times': u'Ni prihodov.'},
                               {'direction': u'\u0160tepanjsko nas.', 'bus_number': u'5N', 'times': u'Ni prihodov.'},
                               {'direction': u'Dm - \u010drnu\u010de', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                               {'direction': u'\u010crnu\u010de', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                               {'direction': u'\u010crnu\u010de', 'bus_number': u'6', 'times': '14", 27", 32"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'6', 'times': u'Ni prihodov.'},
                               {'direction': u'Nove jar\u0161e', 'bus_number': u'7', 'times': '8", 37", 67"'},
                               {'direction': u'Letali\u0161ka', 'bus_number': u'7L', 'times': u'Ni prihodov.'},
                               {'direction': u'Brn\u010di\u010deva', 'bus_number': u'8', 'times': u'Ni prihodov.'},
                               {'direction': u'\u0160tepanjsko nas.', 'bus_number': u'9', 'times': '6", 33", 44"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'9', 'times': u'Ni prihodov.'},
                               {'direction': u'Be\u017eigrad', 'bus_number': u'11', 'times': u'Ni prihodov.'},
                               {'direction': u'Je\u017eica', 'bus_number': u'11', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'11', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'13', 'times': u'Ni prihodov.'},
                               {'direction': u'Center sto\u017eice', 'bus_number': u'13', 'times': '68"'},
                               {'direction': u'Savlje', 'bus_number': u'14B', 'times': '27", 87"'},
                               {'direction': u'Savlje', 'bus_number': u'14', 'times': '12", 57"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'14B', 'times': u'Ni prihodov.'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'14', 'times': u'Ni prihodov.'},
                               {'direction': u'Toma\u010devo', 'bus_number': u'19I', 'times': '80"'},
                               {'direction': u'Toma\u010devo', 'bus_number': u'19B', 'times': '35"'},
                               {'direction': u'Gara\u017ea', 'bus_number': u'19B', 'times': u'Ni prihodov.'},
                               {'direction': u'Nove sto\u017eice', 'bus_number': u'20', 'times': u'Ni prihodov.'},
                               {'direction': u'Nove sto\u017eice', 'bus_number': u'20Z', 'times': '13", 40", 71"'},
                               {'direction': u'Kolodvor', 'bus_number': u'23', 'times': u'Ni prihodov.'},
                               {'direction': u'Zadobrova', 'bus_number': u'25', 'times': '16", 38", 81"'},
                               {'direction': u'Btc - letali\u0161ka', 'bus_number': u'27', 'times': u'Ni prihodov.'},
                               {'direction': u'Kolosej', 'bus_number': u'27K', 'times': u'Ni prihodov.'}])])

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    def test_station_filter_station(self, mock_render_template, mock_post):
        from . import station, Station
        mock_post().text = FIXTURE

        station('bavarski', '6')

        mock_render_template.assert_called_with(
            'station.html',
            letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            stations=[Station(number=u'600012',
                              name=u'BAVARSKI DVOR',
                              buses=[{'direction': u'Dolgi most', 'bus_number': u'6', 'times': '15", 53", 73"'},
                                     {'direction': u'Gara\u017ea', 'bus_number': u'6', 'times': u'Ni prihodov.'},
                                     {'direction': u'Notranje gorice', 'bus_number': u'6B', 'times': '35", 50"'}]),
                      Station(number=u'600011',
                              name=u'BAVARSKI DVOR',
                              buses=[{'direction': u'Dm - \u010drnu\u010de', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                                     {'direction': u'Gara\u017ea', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                                     {'direction': u'\u010crnu\u010de', 'bus_number': u'6B', 'times': u'Ni prihodov.'},
                                     {'direction': u'\u010crnu\u010de', 'bus_number': u'6', 'times': '14", 27", 32"'},
                                     {'direction': u'Gara\u017ea', 'bus_number': u'6', 'times': u'Ni prihodov.'}])]
        )

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    def test_station_empty_results(self, mock_render_template, mock_post):
        from . import station
        mock_post().text = FIXTURE2

        station('booooooooo')

        mock_render_template.assert_called_with(
            'index.html',
            error=u'Postaje s tem imenom/številko ni.',
        )

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    @mock.patch('trolasi.sentry')
    def test_station_random_service_response(self, mock_sentry, mock_render_template, mock_post):
        from . import station
        mock_post().text = "RANDOM"

        station('bavarski')

        mock_render_template.assert_called_with(
            'index.html',
            error=u'Vir podatkov je spremenil format, administrator je bil obveščen.',
        )

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    @mock.patch('trolasi.sentry')
    def test_station_non_200_service_response(self, mock_sentry, mock_render_template, mock_post):
        from . import station
        from requests.exceptions import HTTPError
        mock_post().raise_for_status.side_effect = HTTPError

        station('bavarski')

        mock_render_template.assert_called_with(
            'index.html',
            error=u'Nekaj je šlo narobe, administrator je bil obveščen.',
        )

    @mock.patch('trolasi.requests.post')
    @mock.patch('trolasi.render_template')
    def test_station_service_timeout(self, mock_render_template, mock_post):
        from . import station
        from requests.exceptions import Timeout
        mock_post.side_effect = Timeout

        station('bavarski')

        mock_render_template.assert_called_with(
            'index.html',
            error=u'Podatki trenutno niso dosegljivi, poskusite kasneje.',
        )


class calculate_timesTests(unittest.TestCase):

    def _makeOne(self, dt, cur_time):
        from . import calculate_times
        return calculate_times(dt, cur_time)

    def test_ok(self):
        mins = self._makeOne(datetime(2012, 8, 8, 0, 1),
                             datetime(2012, 8, 8, 0, 0))
        self.assertEqual(mins, 1)

    def test_advanced_time_is_zero(self):
        mins = self._makeOne(datetime(2012, 8, 8, 0, 1),
                             datetime(2012, 8, 8, 0, 2))
        self.assertEqual(mins, 0)


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from . import app
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_index(self):
        r = self.client.get('/')
        self.assertTrue('Najdi postajo' in r.data)

    def test_index_redirect(self):
        r = self.client.get('/?station=123')
        self.assertTrue(r.location.endswith('/123'))

    def test_station(self):
        r = self.client.get('/bavarski')
        self.assertTrue('Dolgi most' in r.data)
        self.assertTrue('Brod' in r.data)

    def test_station_bus(self):
        r = self.client.get('/bavarski/6')
        self.assertTrue('Dolgi most' in r.data)
        self.assertTrue('Brod' not in r.data)
