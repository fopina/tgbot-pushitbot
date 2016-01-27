#!/usr/bin/env python
# coding=utf-8

from tgbot import TGBot, botapi
from tgbot.pluginbase import TGPluginBase, TGCommandBase
from tgbot.webserver import wsgi_app
import argparse
import os


class PushItPlugin(TGPluginBase):
    def list_commands(self):
        return (
            TGCommandBase('token', self.token, 'view your API token'),
            TGCommandBase('revoke', self.revoke, 'revoke your API token and create a new one'),
            TGCommandBase('help', self.help, 'more information'),
            TGCommandBase('start', self.help, '', printable=False),
        )

    def token(self, message, text):
        token = self.read_data(message.chat.id, 'token')
        if not token:
            token = self._new_token(message.chat.id)

        return self.bot.return_message(message.chat.id, '''\
You can use the following token to access the HTTP API:

*%(token)s*

Your API URL: https://tgbots-fopina.rhcloud.com/pushit/%(token)s
Your WebPush URL: http://fopina.github.io/tgbot-pushitbot/webpush/#%(token)s

Please send /help command if you have any problem''' % {'token': token}, parse_mode='Markdown')

    def revoke(self, message, text):
        token = self._new_token(message.chat.id)

        return self.bot.return_message(message.chat.id, '''\
Your _old_ token has been revoked.
You can now use the following token to access the HTTP API:

*%(token)s*

Your API URL: https://tgbots-fopina.rhcloud.com/pushit/%(token)s
Your WebPush URL: http://fopina.github.io/tgbot-pushitbot/webpush/#%(token)s

Please send /help command if you have any problem''' % {'token': token}, parse_mode='Markdown')

    def help(self, message, text):
        return self.bot.return_message(message.chat.id, u'''\
I'm PushIt Bot and I can help you integrate your scripts or website with Telegram.
Please read this manual before we begin:

 📖 http://fopina.github.com/tgbot-pushitbot/api-docs

Here is the commands list:

/token - view your API token
/revoke - revoke your API token and create a new one
''', parse_mode='Markdown')

    def chat(self, message, text):
        return self.bot.return_message(message.chat.id, u'''\
I'm not really chatty. Give /help a try if you need something.''')

    # entry point for webserver call
    def notify(self, chat_token, data):
        chat_id = self.read_data('token', chat_token)

        if not chat_id:
            return dict(
                ok=False,
                code=-1,
                description='Invalid token'
            )

        if 'msg' not in data:
            return dict(
                ok=False,
                code=-999,
                description='Please check API documentation'
            )

        parse_mode = data.get('format')
        if parse_mode and parse_mode not in ['Markdown', 'HTML']:
            return dict(
                ok=False,
                code=-999,
                description='Please check API documentation'
            )

        ret = self.bot.send_message(chat_id, data['msg'], parse_mode=parse_mode).wait()

        res = {'ok': True}
        if isinstance(ret, botapi.Error):
            res['ok'] = False
            res['code'] = ret.error_code
            if ret.error_code == 403:
                res['description'] = 'User blocked PushItBot'
            else:
                res['description'] = ret.description

        return res

    def _new_token(self, chat_id):
        # revoke old
        token = self.read_data(chat_id, 'token')
        if token:
            self.save_data('token', token)

        # generate new one
        token = os.urandom(16).encode('hex')
        self.save_data(chat_id, 'token', token)
        self.save_data('token', token, chat_id)
        return token


class PushItBot(TGBot):
    def __init__(self, token, db_url=None):
        self.pushit = PushItPlugin()
        TGBot.__init__(
            self,
            token, db_url=db_url,
            plugins=[self.pushit],
            no_command=self.pushit
        )

    def notify(self, chat_token, data):
        return self.pushit.notify(chat_token, data)


def setup(db_url=None, token=None):
    tg = PushItBot(token, db_url=db_url)
    return tg


def openshift_app():
    import os

    bot = setup(
        db_url='postgresql://%s:%s/%s' % (
            os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
            os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
            os.environ['PGDATABASE']
        ),
        token=os.environ['TGTOKEN']
    )
    bot.set_webhook('https://%s/update/%s' % (os.environ['OPENSHIFT_APP_DNS'], bot.token))

    return extend_webapp(wsgi_app([bot]), bot)


def extend_webapp(app, bot):
    from bottle import request, response

    @app.route('/pushit/<token>', method=['GET', 'POST'])
    def pushit(token):
        # support CORS!
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'
        return bot.notify(token, request.json or request.query or request.forms)

    return app


def main(args=None):
    args = parse_args(args)

    tg = setup(db_url=args.db_url, token=args.token)

    if args.list:
        tg.print_commands()
        return

    if args.create_db:
        tg.setup_db()
        print 'DB created'
        return

    tg.set_webhook('%s/update/%s' % (args.webhook[0], tg.token))
    extend_webapp(wsgi_app([tg]), tg).run(host='0.0.0.0', port=int(args.webhook[1]))


def parse_args(args):
    parser = argparse.ArgumentParser(description='Run PushItBot')

    parser.add_argument('--db_url', '-d', dest='db_url', default='sqlite:///pushitbot.sqlite3',
                        help='URL for database (default is sqlite:///pushitbot.sqlite3)')
    parser.add_argument('--list', '-l', dest='list', action='store_const',
                        const=True, default=False,
                        help='print commands (for BotFather)')
    parser.add_argument('--webhook', '-w', dest='webhook', nargs=2, metavar=('hook_url', 'port'),
                        help='use webhooks (instead of polling) - requires bottle')
    parser.add_argument('--create_db', dest='create_db', action='store_const',
                        const=True, default=False,
                        help='setup database')
    parser.add_argument('--token', '-t', dest='token',
                        help='token provided by @BotFather')
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
