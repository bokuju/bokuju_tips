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

        for s in _baribari_strings: 
            if re.compile(s, re.MULTILINE).search(text):
                return True

        return False

    def tweet_is_my_tweet(self, tweet):
        """
        TODO
        if tweet.is_my() == true:
        とかしたいんだけど
        """
        if tweet.user.screen_name == self.__username:
            return True
        else:
            return False

    def tweet_in_N_minites(self, tweet, N=1):
        """
        TODO
        if tweet.in_N_minites() == true:
        とかしたいんだけど
        """
        _create_time = tweet.created_at_in_seconds
        _now = int(time.time())
        if (N* 60) >= (_now - _create_time):
            return True
        else:
            return False

if __name__ == '__main__':
    from baribari_yamete_conf import username, password

    bot = BaribariYameteBot(username, password)

    bot.post_refollow()

    bot.delete_refollow()

    tweetes = bot.get_follwing_timeline()
    for tweet in tweetes:
        #TODO 時間で重複を防いでいるが、もっとウマいやり方あると思う
        #if is_my_tweet(tweet) is False and search_baribari(tweet.text) is True:
        if bot.tweet_is_my_tweet(tweet) is False and bot.tweet_in_N_minites(tweet) is True and bot.tweet_search_baribari(tweet.text) is True:
            my_tweet = bot.post_retweet(u"やめて！", tweet)
