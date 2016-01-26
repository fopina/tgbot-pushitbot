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

    def test_one(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    import unittest
    unittest.main()
