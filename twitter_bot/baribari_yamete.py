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

    def get_tweet_list(self):
        _text_list = [
            u"誰もバリバリ言わないお(´・ ω・`)ｼｮﾎﾞｰﾝ",
            #u"( ﾟωﾟ　)支払いは俺に任せろーﾊﾞﾘﾊﾞﾘ",
            #u"( ﾟωﾟ　)でもこれがポーターの財布だとしたら？",
            #u"(　ﾟωﾟ )このセーター マジックテープ式だったんだ　しまむら。。",
            #u"お前が払う？",
            #u"( ﾟωﾟ　)クーポンもあるぜーﾍﾟﾘﾍﾘﾟ",
            #u"( ﾟωﾟ　)とどめは携帯クーポンで10％OFFだー！！ﾋﾟﾎﾟﾊﾟﾎ",
            #u"(　ﾟωﾟ )……なんてね この指輪、受け取ってくれるかい？ｷﾗｯ",
            #u"(　ﾟωﾟ )宝石の部分だけ外れるのさーﾊﾞﾘﾊﾞﾘ",
        ]
        return _text_list

    def get_retweet_list(self):
        _text_list = [
            u"やめて！",
            u"ふしぎ！抱いて！",
            u"まじでやめて！",
        ]
        return _text_list

    def post_random_tweet(self):
        _tweet_list = self.get_tweet_list()
        _tweet = twitter_bot.Bot.post_random_tweet(self, text_list=_tweet_list)
        return _tweet
        
    def post_random_retweet(self, tweet):
        _retweet_list = self.get_retweet_list()
        _tweet = twitter_bot.Bot.post_random_retweet(self, tweet, text_list=_retweet_list)
        return _tweet
        
    def run(self):
        self.post_refollow()

        self.delete_refollow()

        self.post_random_tweet()

        #TODO 時間で重複を防いでいるが、もっとウマいやり方あると思う
        _tweetes = self.get_recently_follwing_timeline()
        print "get tweetes (%d) at (%s)" % (len(_tweetes), time.ctime())

        _ret_tweet = None
        for _tweet in _tweetes:
            if self.tweet_search_baribari(_tweet.text) is True:
                _ret_tweet = self.post_random_retweet(_tweet)
            elif self.tweet_search_makasero(_tweet.text) is True:
                _ret_tweet = self.post_retweet(u"ﾊﾞﾘﾊﾞﾘ", _tweet)
            else:
                pass
        return _ret_tweet

if __name__ == '__main__':
    import baribari_yamete_conf as conf

    bot = BaribariYameteBot(conf.username, conf.password)
    bot.run()

