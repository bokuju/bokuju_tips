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
        _tm_dom = self.get_tomorrow_dom()
        print self.get_plain_text(_td_dom)
        #print self.get_plain_text(_tm_dom)
        return True

    def get_plain_text(self, dom):
        text = ''.join([ s.string if s.string else self.get_plain_text(s) for s in dom ])
        ctug = re.compile('<!--.*?-->',re.DOTALL)
        text = ctug.sub('', text)
        return text

if __name__ == '__main__':
    o = Otenki()
    o.print_otenki()
