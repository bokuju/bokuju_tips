#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

import twitter_bot

class BaribariYameteBot(twitter_bot.Bot):
    def __init__(self, username, password):
        twitter_bot.Bot.__init__(self, username, password)

    def tweet_search_baribari(self, text):
        """
        if tweet.search_baribari() == true:
        とかしたいんだけど
        """
        _baribari_strings = (
            u"ばりばり",
            u"バリバリ",
            u"バリばり",
            u"ばりバリ",
            u"ﾊﾞﾘﾊﾞﾘ"
        )

        for _s in _baribari_strings: 
            if re.compile(_s, re.MULTILINE).search(text):
                return True

        return False

    def tweet_search_makasero(self, text):
        _strings = (
            u"俺に任せろ",
            u"俺にまかせろ",
            u"おれに任せろ",
            u"オレに任せろ",
            u"おれにまかせろ"
        )

        for _s in _strings: 
            if re.compile(_s, re.MULTILINE).search(text):
                return True

        return False

if __name__ == '__main__':
    import baribari_yamete_conf as conf

    bot = BaribariYameteBot(conf.username, conf.password)

    bot.post_refollow()

    bot.delete_refollow()

    #TODO 時間で重複を防いでいるが、もっとウマいやり方あると思う
    tweetes = bot.get_recently_follwing_timeline()
    print "get tweetes (%d) at (%s)" % (len(tweetes), time.ctime())

    for tweet in tweetes:
        if bot.tweet_search_baribari(tweet.text) is True:
            bot.post_retweet(u"やめて！", tweet)
        elif bot.tweet_search_makasero(tweet.text) is True:
            bot.post_retweet(u"バリバリ(ﾟωﾟ)", tweet)
        else:
            pass
