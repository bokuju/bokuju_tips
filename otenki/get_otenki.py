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
        self._soup = self.get_soup(self._uri)

    def get_uri(self):
        _today = self.get_today()
        _url="http://rd.yahoo.co.jp/rss/l/weather/days/*http://weather.yahoo.co.jp/weather/jp/13/4410.html?d=" + _today
        return _url

    def get_today(self):
        _tm = time.localtime()
        _today = "%(year)d%(month)02d%(day)02d" % {"year":_tm.tm_year, "month":_tm.tm_mon, "day":_tm.tm_mday}
        return _today

    def get_soup(self, uri):
        source = urllib.urlopen(uri).read()
        try:
            # BeautifulSoupでパース
            soup = BeautifulSoup.BeautifulSoup(source)
        except:
            # エラーが発生したらhtml5libでパース
            parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
            soup = parser.parse(source)
        return soup

    def get_otenki(self):
        _td_comment = self.get_today_comment()
        _tm_comment = self.get_today_comment()
        #import pdb;pdb.set_trace()
        print _td_comment.findNext()
        print _tm_comment.findNext()
        return _td_comment, _tm_comment

    def get_comment(self, text):
        _comment = self._soup.find(text=re.compile(text))
        return _comment

    def get_today_comment(self):
        _comment = self.get_comment("Today")
        return _comment

    def get_tomorrow_comment(self):
        _comment = self.get_comment("Tomorrow")
        return _comment

if __name__ == '__main__':
    o = Otenki()
    print o.get_otenki()
