#!/usr/bin/env python
# coding=utf-8

from tgbot import TGBot
from tgbot.pluginbase import TGPluginBase, TGCommandBase
import argparse


class PushItPlugin(TGPluginBase):
    def list_commands(self):
        return (
            TGCommandBase('token', self.token, 'Get your API token'),
        )

    def token(self, message, text):
        return self.bot.return_message(message.chat.id, 'done')


def setup(db_url=None, token=None):
    tg = TGBot(
        token,
        plugins=[PushItPlugin()],
        db_url=db_url,
    )
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

    from tgbot.webserver import wsgi_app
    return wsgi_app([bot])


def main():
    parser = build_parser()
    args = parser.parse_args()

    tg = setup(db_url=args.db_url, token=args.token)

    if args.list:
        tg.print_commands()
        return

    if args.create_db:
        tg.setup_db()
        print 'DB created'
        return

    tg.run_web(args.webhook[0], host='0.0.0.0', port=int(args.webhook[1]))


def build_parser():
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
    return parser


if __name__ == '__main__':
    main()
