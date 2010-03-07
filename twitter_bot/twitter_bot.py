#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def get_follwing_timeline(self):
        """
        フォローされているユーザーのタイムラインを取得する
        """
        _tweetes = self._api.GetFriendsTimeline()
        return _tweetes

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
        print "tweet (%s) at (%s)" % (_tweet.text, _tweet.created_at)

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
        print "follow (%s)" % (_user.screen_name)
        return _user

    def delete_follow(self, username):
        """
        フォローを解除する
        """
        #TODO フォローしていないかチェック
        _user = self._api.DestroyFriendship(username)
        print "un follow (%s)" % (_user.screen_name)
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


if __name__ == '__main__':
    pass
