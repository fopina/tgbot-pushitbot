#!/usr/bin/env python
# coding=utf-8

from tgbot import plugintest
from tgbot.webserver import wsgi_app
import pushitbot
from webtest import TestApp
from webtest.app import AppError


class BotTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.prepare_bot(pushitbot.PushItBot('botToken'))
        self.webapp = TestApp(pushitbot.extend_webapp(wsgi_app([self.bot]), self.bot))

    def test_ping(self):
            self.assertEqual(self.webapp.get('/ping/').text, '<b>Pong!</b>')

    def test_chat(self):
        self.receive_message('invalid')
        self.assertReplied(u'''\
I'm not really chatty. Give /help a try if you need something.''')

    def test_token(self):
        self.assertIsNone(self.bot.pushit.read_data(1, 'token'))

        self.receive_message('/token')

        token = self.bot.pushit.read_data(1, 'token')
        self.assertIsNotNone(token)
        self.assertIsNotNone(self.bot.pushit.read_data('token', token))

        self.assertReplied('''\
You can use the following token to access the HTTP API:

*%s*

Please send /help command if you have any problem''' % token)

        return token

    def test_revoke(self):
        token1 = self.test_token()

        self.receive_message('/revoke')
        self.assertIsNone(self.bot.pushit.read_data('token', token1))
        token2 = self.bot.pushit.read_data(1, 'token')
        self.assertIsNotNone(token2)
        self.assertReplied('''\
Your _old_ token has been revoked.
You can now use the following token to access the HTTP API:

*%s*

Please send /help command if you have any problem''' % token2)

if __name__ == '__main__':
    import unittest
    unittest.main()
