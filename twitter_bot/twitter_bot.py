#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random

import twitter

"""
TODO
まるっとpython_twitterを隠蔽したい
入力値と戻り値を隠蔽
"""
class Bot(object):
    """
    Twitter用BOTクラス
    テンプレート的に使う
    """
    def __init__(self, username, password):
        """
        コンストラクタ
        """
        self._username = username
        self._password = password
        self._api = twitter.Api(username=self._username, password=self._password)

    def get_timeline(self, user=None):
        """
        ユーザーのタイムラインを取得する
        """
        _tweetes = self._api.GetUserTimeline(user)
        return _tweetes

    def get_follwing_timeline(self, user=None):
        """
        フォローされているユーザーのタイムラインを取得する
        """
        _tweetes = self._api.GetFriendsTimeline(user)
        _ret_tweetes = []
        for _tweet in _tweetes:
            if self.tweet_is_my_tweet(_tweet) is False:
                _ret_tweetes.append(_tweet)
        return _ret_tweetes

    def get_recently_follwing_timeline(self, time=1):
        """
        フォローされているユーザーの最近のタイムラインを取得する
        """
        _tweetes = self.get_follwing_timeline()
        _ret_tweetes = []
        for _tweet in _tweetes:
            if self.tweet_in_N_minites(_tweet, time) is True:
                _ret_tweetes.append(_tweet)
        return _ret_tweetes

    def get_replies(self):
        """
        リプライ（自分宛のツイート）を取得する
        """
        _tweetes = sefl._api.GetReplies()
        return _tweetes

    def post_tweet(self, text):
        """
        ツイートする
        """
        _tweet = self._api.PostUpdate(text)
        print "tweet (%s) at (%s)" % (_tweet.text, time.ctime())

        return _tweet

    def post_retweet(self, text, tweet):
        """
        RTする
        """
        _rt_text = tweet.text
        _rt_user = tweet.user.GetScreenName()
        _text = "%s RT @%s: %s" % (text, _rt_user, _rt_text)
        _tweet = self.post_tweet(_text)
        return _tweet

    def get_following(self):
        """
        フォローされているユーザーを取得する
        """
        _users = self._api.GetFriends()
        return _users

    def get_follower(self):
        """
        フォローしているユーザーを取得する
        """
        _users = self._api.GetFollowers()
        return _users

    def post_follow(self, username):
        """
        フォローする
        """
        #TODO フォローしているかチェック
        _user = self._api.CreateFriendship(username)
        print "follow (%s) at (%s)" % (_user.screen_name, time.ctime())
        return _user

    def delete_follow(self, username):
        """
        フォローを解除する
        """
        #TODO フォローしていないかチェック
        _user = self._api.DestroyFriendship(username)
        print "un follow (%s) at (%s)" % (_user.screen_name, time.ctime())
        return _user

    def post_refollow(self):
        """
        フォローしていないユーザーをフォローする
        """
        _users = self.get_not_following()

        _follow_users = []
        for _user in _users:
            _follow_user = self.post_follow(_user.screen_name)
            _follow_users.append(_follow_user)

        return _follow_users

    def delete_refollow(self):
        """
        フォローされていないユーザーのフォローを解除する
        """
        _users = self.get_not_follower()

        _un_follow_users = []
        for _user in _users:
            _un_follow_user = self.delete_follow(_user.screen_name)
            _un_follow_users.append(_un_follow_user)

        return _un_follow_users

    def get_not_following(self):
        """
        フォローしていないユーザーを取得する
        """
        _following_users = self.get_following()
        _follower_users = self.get_follower()

        _not_following_users = []
        for _follower_user in _follower_users:
            if _follower_user not in _following_users:
                _not_following_users.append(_follower_user)

        return _not_following_users

    def get_not_follower(self):
        """
        フォローされていないユーザーを取得する
        """
        _following_users = self.get_following()
        _follower_users = self.get_follower()

        _not_follower_users = []
        for _following_user in _following_users:
            if _following_user not in _follower_users:
                _not_follower_users.append(_following_user)

        return _not_follower_users

    def tweet_is_my_tweet(self, tweet):
        """
        TODO
        if tweet.is_my() == true:
        とかしたいんだけど
        """
        if tweet.user.screen_name == self._username:
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
        if (N * 60) >= (_now - _create_time):
            return True
        else:
            return False

    def post_random_tweet(self, persent=40, time=180, text_list=[]):
        """
        ランダムなツイートする。ツイートする頻度もランダム。
        TODO: ツイートする頻度にパーセントでばらつきをもたせる
        """
        _recently_my_tweet = self.get_recently_my_tweet()
        _random_text = self.get_random_text(text_list)
        _tweet = None
        if self.tweet_in_N_minites(_recently_my_tweet, time) == False:
            _tweet = self.post_tweet(_random_text)
        return _tweet

    def post_random_retweet(self, tweet, text_list=[]):
        """
        ランダムにRTする
        TODO:引数のならびの検討
        """
        _random_text = self.get_random_text(text_list)
        _tweet = self.post_retweet(_random_text, tweet)
        return _tweet

    def get_recently_my_tweet(self):
        """
        自分の最近のツイートを取得する
        """
        _tweetes = self.get_timeline()
        _ret_tweet = None
        _create_time = 0
        for _tweet in _tweetes:
            if _create_time < _tweet.created_at_in_seconds:
                _ret_tweet = _tweet
                _create_time = _tweet.created_at_in_seconds
        return _ret_tweet

    def get_random_text(self, text_list=[]):
        """
        ランダムなテキストを取得する。
        """
        if len(text_list) > 0:
            _text_list = text_list
        else:
            _text_list = self.get_text_list()
        _random_number = random.randrange(0, len(_text_list))
        _random_text = _text_list[_random_number]
        return _random_text

    def get_text_list(self):
        """
        テキストのリストを取得する。
        """
        _text_list = [
            "おはようございます。",
            "こんにちは。",
            "こんばんは。",
            "私の名前は、%sです。" % (self._username),
        ]
        return _text_list

if __name__ == '__main__':
    import baribari_yamete_conf as conf

    #bot = Bot(conf.username, conf.password)
    #print bot.get_recently_my_tweet().text
    #print bot.post_random_tweet()
