#!/usr/bin/env python
# coding=utf-8

from tgbot import plugintest
from tgbot.webserver import wsgi_app
import pushitbot
from webtest import TestApp


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

    def test_notify_invalid_token(self):
        res = self.webapp.post_json('/pushit/123', params={'msg': 'hello'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['code'], -1)
        self.assertEqual(res.json['description'], 'Invalid token')

    def test_notify_blocked(self):
        token = self.test_token()

        self.push_fake_result('...', status_code=403)
        res = self.webapp.post_json('/pushit/%s' % token, params={'msg': 'hello'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['code'], 403)
        self.assertEqual(res.json['description'], 'User blocked PushItBot')

    def test_notify_other_tg_error(self):
        token = self.test_token()

        self.push_fake_result('...', status_code=400)
        res = self.webapp.post_json('/pushit/%s' % token, params={'msg': 'hello'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['code'], 400)
        self.assertEqual(res.json['description'], '...')

    def test_notify_urlencoded(self):
        token = self.test_token()
        res = self.webapp.post('/pushit/%s' % token, params={'msg': 'hello'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], True)
        # assert message was sent
        self.assertReplied('hello')

    def test_notify_json(self):
        token = self.test_token()
        res = self.webapp.post_json('/pushit/%s' % token, params={'msg': 'world'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], True)
        # assert message was sent
        self.assertReplied('world')

    def test_notify_get(self):
        token = self.test_token()
        res = self.webapp.get('/pushit/%s' % token, params={'msg': '1 2 3'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], True)
        # assert message was sent
        self.assertReplied('1 2 3')

    def test_notify_broken(self):
        token = self.test_token()
        res = self.webapp.post('/pushit/%s' % token, params={'wrong': 'field'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['description'], 'Please check API documentation')
        # assert no messages were sent
        self.assertNoReplies()

if __name__ == '__main__':
    import unittest
    unittest.main()
