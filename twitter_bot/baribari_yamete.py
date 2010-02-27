#!/usr/bin/python
# -*- coding: utf-8 -*-

import twitter_bot

class BaribariYameteBot(twitter_bot.Bot):
    def __init__(self, username, password):
        twitter_bot.Bot.__init__(self, username, password)

"""
if tweet.search_baribari() == true:
とかしたいんだけど
"""
def search_baribari(text):
    import re
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

"""
TODO
if tweet.is_my() == true:
とかしたいんだけど
"""
def is_my_tweet(tweet):
    _me = "baribari_yamete" #TODO 固定値をやめる
    
    if tweet.user.screen_name == _me:
        return True
    else:
        return False

"""
TODO
if tweet.in_N_minites() == true:
とかしたいんだけど
"""
def in_N_minites(tweet, N=1):
    import time
    _create_time = tweet.created_at_in_seconds
    _now = int(time.time())
    if (N* 60) >= (_now - _create_time):
        return True
    else:
        return False

if __name__ == '__main__':
    username = "baribari_yamete"
    password = "baribari"

    bot = BaribariYameteBot(username, password)

    bot.post_refollow()

    bot.delete_refollow()

    tweetes = bot.get_follwing_timeline()
    for tweet in tweetes:
        #TODO 時間で重複を防いでいるが、もっとウマいやり方あると思う
        #if is_my_tweet(tweet) is False and search_baribari(tweet.text) is True:
        if is_my_tweet(tweet) is False and in_N_minites(tweet) is True and search_baribari(tweet.text) is True:
            my_tweet = bot.post_retweet(u"やめて！", tweet)
