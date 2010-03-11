#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

import xmpp
import xmpp.debug

class Bot(object):
    """
    受け取ったメッセージをオウム返しするBOT
    """

    def __init__(self, user, password, server=localhost, debug=False):
        self._user = user
        self._password = password
        self._server = server
        if debug == False:
            xmpp.debug.Debug = xmpp.debug.NoDebug

    def _connect(self):
        self._conn = xmpp.Client(self._server)

        _resp = self._conn.connect()

        if not _resp:
            print "Unable to connect to server %s!" % self._server
            sys.exit(1)

        if _resp <> 'tls':
            print "TLS failed!"
            sys.exit(1)

    def _auth(self):
        _resp = self._conn.auth(self._user, self._password)

        if not _resp:
            print "Login failed!"
            sys.exit(1)

        if _resp <> 'sasl':
            print "SASL failed!"
            sys.exit(1)

    def handler(self, conn, mess):
        txt = mess.getBody()
        reply = mess.buildReply(txt)
        conn.send(reply)

    def _setting(self):
        self._conn.RegisterHandler('message', self.handler)
        self._conn.sendInitPresence()

    def _step_on(self):
        try:
            self._conn.Process(1)
        except KeyboardInterrupt:
            return 0
        return 1

    def _go_on(self):
        while self._step_on():
            pass

    def run(self):
        self._connect()
        self._auth()
        self._setting()
        print "Bot started."
        self._go_on()

if __name__ == '__main__':
    import xmpp_bot_config as config

    bot = Bot(config.username, config.password, config.server)
    bot.run()
