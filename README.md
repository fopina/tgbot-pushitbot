PushItBot allows you to easily get notifications from your website and scripts on your Telegram window.

Just reach [@PushItBot](http://telegram.me/pushitbot) on Telegram to try it or check out its [webpage](http://fopina.github.io/tgbot-pushitbot/) for more information.

[![Build Status](https://travis-ci.org/fopina/tgbot-pushitbot.svg?branch=master)](https://travis-ci.org/fopina/tgbot-pushitbot) [![Coverage Status](https://coveralls.io/repos/fopina/tgbot-pushitbot/badge.svg?branch=master&service=github)](https://coveralls.io/github/fopina/tgbot-pushitbot?branch=master)

PushItBot was developed using [TGBotPlug](http://fopina.github.io/tgbotplug).

This repository is ready for openshift (as the bot is running there), so you can easily host your own copy:

* Register in [OpenShift](https://www.openshift.com)  
* Install [rhc](https://developers.openshift.com/en/managing-client-tools.html), the command line tool  
* Run `rhc setup` to configure it  
* Talk to [@BotFather](http://telegram.me/botfather) to register your bot  
* And finally run these commands (replacing `<YOUR_BOT_TOKEN>` with the token provided by @BotFather)

    ```bash
    rhc app-create pushitbot python-2.7 postgresql-9.2 --from-code https://github.com/fopina/tgbot-pushitbot/
    cd pushitbot
    rhc env-set TGTOKEN=<YOUR_BOT_TOKEN>
    rhc ssh -- 'app-root/repo/pushitbot.py --db_url="postgresql://$OPENSHIFT_POSTGRESQL_DB_HOST:$OPENSHIFT_POSTGRESQL_DB_PORT/$PGDATABASE" --create_db'
    rhc app-restart
    ```

Have fun!
