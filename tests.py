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

        self.assertReplied(_TOKEN_TEXT % {'token': token})

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

*%(token)s*

Your API URL: https://tgbots-fopina.rhcloud.com/pushit/%(token)s
Your WebPush URL: http://fopina.github.io/tgbot-pushitbot/webpush/#%(token)s

Please send /help command if you have any problem''' % {'token': token2})

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
        # assert message was sent and no format
        r = self.pop_reply()[1]
        self.assertEqual(r['text'], 'world')
        self.assertNotIn('parse_mode', r)

    def test_notify_get(self):
        token = self.test_token()
        res = self.webapp.get('/pushit/%s' % token, params={'msg': '1 2 3', 'format': 'Markdown'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], True)
        # assert message was sent with markdown format
        # assert message was sent and no format
        r = self.pop_reply()[1]
        self.assertEqual(r['text'], '1 2 3')
        self.assertEqual(r['parse_mode'], 'Markdown')

    def test_notify_broken(self):
        token = self.test_token()
        res = self.webapp.post('/pushit/%s' % token, params={'wrong': 'field'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['description'], 'Please check API documentation')
        # assert no messages were sent
        self.assertNoReplies()

        res = self.webapp.post(
            '/pushit/%s' % token,
            params={'msg': 'corrent', 'format': 'wrong'}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['ok'], False)
        self.assertEqual(res.json['description'], 'Please check API documentation')
        # assert no messages were sent
        self.assertNoReplies()

    def test_stats(self):
        token = self.test_token()

        self.receive_message('/stats')
        self.assertReplied('`Pushed messages so far:` *0*')

        res = self.webapp.post_json('/pushit/%s' % token, params={'msg': 'world'})
        self.assertEqual(res.json['ok'], True)

        self.receive_message('/stats')
        self.assertReplied('`Pushed messages so far:` *1*')

    def test_start_token(self):
        self.receive_message('/start token')

        token = self.bot.pushit.read_data(1, 'token')
        self.assertIsNotNone(token)

        self.assertReplied(_TOKEN_TEXT % {'token': token})
        self.assertReplied(_HELP_TEXT)

    def test_help(self):
        self.receive_message('/help')
        self.assertReplied(_HELP_TEXT)

        self.receive_message('/start')
        self.assertReplied(_HELP_TEXT)

    def test_no_new_token(self):
        import mock

        with mock.patch('os.urandom', return_value='1' * 16):
            self.test_token()
            self.receive_message('/revoke')
            self.assertReplied('Failed to generate a token... Please try again.')
            self.receive_message('/token', sender={'id': 2, 'first_name': 'Paul'})


class OtherTest(plugintest.PluginTestCase):
    def test_openshift(self):
        import os
        import mock

        orig_setup = pushitbot.setup

        def new_setup(*args, **kwargs):
            self.bot = self.prepare_bot(orig_setup(*args, **kwargs))
            return self.bot

        os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'] = 'localhost'
        os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'] = '123'
        os.environ['PGDATABASE'] = 'test'
        os.environ['TGTOKEN'] = 'fakeToken'
        os.environ['OPENSHIFT_APP_DNS'] = 'something.rhcloud.com'

        with mock.patch('pushitbot.setup', new_setup):
            pushitbot.openshift_app()

        r = self.pop_reply()
        self.assertEqual(r[0], 'setWebhook')
        self.assertEqual(r[1]['url'], 'https://something.rhcloud.com/update/fakeToken')

    def test_main(self):
        import mock

        orig_setup = pushitbot.setup

        def new_setup(*args, **kwargs):
            self.bot = self.prepare_bot(orig_setup(*args, **kwargs))
            return self.bot

        bottle_run = mock.Mock()

        with mock.patch('pushitbot.setup', new_setup):
            with mock.patch('bottle.Bottle.run', bottle_run):
                pushitbot.main([
                    '-t', 'fakeToken',
                    '-w', 'http://localhost:1234', '8000',
                ])

        bottle_run.assert_called_with(host='0.0.0.0', port=8000)
        r = self.pop_reply()
        self.assertEqual(r[0], 'setWebhook')
        self.assertEqual(r[1]['url'], 'http://localhost:1234/update/fakeToken')


_TOKEN_TEXT = '''\
You can use the following token to access the HTTP API:

*%(token)s*

Your API URL: https://tgbots-fopina.rhcloud.com/pushit/%(token)s
Your WebPush URL: http://fopina.github.io/tgbot-pushitbot/webpush/#%(token)s

Please send /help command if you have any problem'''

_HELP_TEXT = u'''\
I'm PushIt Bot and I can help you integrate your scripts or website with Telegram.
Please read this manual before we begin:

 📖 http://fopina.github.io/tgbot-pushitbot/#api-docs

Here is the commands list:

/token - view your API token
/revoke - revoke your API token and create a new one
'''

if __name__ == '__main__':
    import unittest
    unittest.main()
