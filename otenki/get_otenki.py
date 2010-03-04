#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
import time
import re

import BeautifulSoup
import html5lib

class Otenki(object):
    def __init__(self):
        self._uri = self.get_uri()
        self._soup = self.get_soup_dom(self._uri)

    def get_today(self):
        _tm = time.localtime()
        _today = "%(year)d%(month)02d%(day)02d" % {"year":_tm.tm_year, "month":_tm.tm_mon, "day":_tm.tm_mday}
        return _today

    def get_uri(self):
        _today = self.get_today()
        _url="http://rd.yahoo.co.jp/rss/l/weather/days/*http://weather.yahoo.co.jp/weather/jp/13/4410.html?d=" + _today
        return _url

    def get_soup_dom(self, uri):
        source = urllib.urlopen(uri).read()
        try:
            # BeautifulSoupでパース
            soup = BeautifulSoup.BeautifulSoup(source)
        except:
            # エラーが発生したらhtml5libでパース
            parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
            soup = parser.parse(source)
        return soup

    def get_comment(self, text):
        _comment = self._soup.find(text=re.compile(text))
        return _comment

    def get_today_dom(self):
        _comment = self.get_comment("Today")
        return _comment.findNextSiblings()[2]

    def get_tomorrow_dom(self):
        _comment = self.get_comment("Tomorrow")
        return _comment.findNextSiblings()[1]

    def print_otenki(self):
        _td_dom = self.get_today_dom()
        _td_weather_info = self.get_weather_info(_td_dom)
        #_td_temp_info = self.get_temp_info(_td_dom)
        _td_rain_info = self.get_rain_info(_td_dom)
        _td_nature_info = self.get_nature_info(_td_dom)

        self.print_weather_info(_td_weather_info)
        #self.print_temp_info(_td_temp_info)
        self.print_rain_info(_td_rain_info)
        self.print_nature_info(_td_nature_info)

        """
        print "-"*12

        _tm_dom = self.get_tomorrow_dom()
        _tm_weather_info = self.get_weather_info(_td_dom)
        #_tm_temp_info = self.get_temp_info(_tm_dom)
        _tm_rain_info = self.get_rain_info(_tm_dom)
        _tm_nature_info = self.get_nature_info(_tm_dom)

        self.print_weather_info(_tm_weather_info)
        #self.print_temp_info(_tm_temp_info)
        self.print_rain_info(_tm_rain_info)
        self.print_nature_info(_tm_nature_info)
        """

        return True

    def print_weather_info(self, weather_info):
        print "- %s -" % "天気"
        print "%s : %s" % (weather_info["date"], weather_info["status"])
        return True

    def print_temp_info(self, temp_info):
        print "- %s -" % "気温"
        print u"最高 : %s" % (temp_info["high"])
        print u"最低 : %s" % (temp_info["low"])
        return True

    def print_rain_info(self, rain_info):
        print "- %s -" % "降水確率"
        for _n in range(len(rain_info)):
            print "%(time)-5s : %(probability)-3s" % rain_info[_n]
        return True

    def print_nature_info(self, nature_info):
        print "- %s -" % "その他"
        print u"風 : %s" % (nature_info["wind"])
        print u"波 : %s" % (nature_info["wave"])
        return True

    def get_weather_info(self, dom):
        _w_dom = dom.find("tr").findAll("table")[0].findAll("td")
        _w_date_dom = _w_dom[0]
        _w_status_dom = _w_dom[1]
        _w_info = {
            "date":self.get_plain_text(_w_date_dom),
            "status":self.get_plain_text(_w_status_dom),
            }
        return _w_info

    def get_temp_info(self, dom):
        _t_dom = dom.find("tr").findAll("table")[1].findAll("td")
        _t_high_dom = _t_dom[0]
        _t_low_dom = _t_dom[1]
        #import pdb;pdb.set_trace()
        _t_info = {
            "high":self.get_plain_text(_t_high_dom),
            "low":self.get_plain_text(_t_low_dom),
            }
        return _t_info

    def get_rain_info(self, dom):
        _r_dom = dom.find("tr").findAll("table")[2].findAll("tr")
        _r_time = _r_dom[1].findAll("td")
        _r_probability = _r_dom[0].findAll("td")
        _r_info = range(4)
        for _n in range(4):
            _r_info[_n] = { 
                "time":self.get_plain_text(_r_time[_n + 1]), 
                "probability":self.get_plain_text(_r_probability[_n + 1])
                }
        return _r_info

    def get_nature_info(self, dom):
        _n_dom = dom.find("tr").findAll("table")[3].findAll("td")
        _n_wind_dom = _n_dom[1]
        _n_wave_dom = _n_dom[3]
        _n_info = {
            "wind":self.get_plain_text(_n_wind_dom),
            "wave":self.get_plain_text(_n_wave_dom),
            }
        return _n_info

    def get_plain_text(self, dom):
        text_list = []
        for _d in dom:
            if _d.string:
                if _d.string != "\n":
                    text_list.append(_d.string.strip())    
            else:
                self.get_plain_text(_d)
        text = ''.join(text_list)
        ctug = re.compile('<!--.*?-->',re.DOTALL)
        text = ctug.sub('', text)
        return text

if __name__ == '__main__':
    o = Otenki()
    o.print_otenki()
