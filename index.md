---
layout: index
---

PushItBot allows you to easily get notifications from your website or scripts on your Telegram window.

Just talk to [@PushItBot](https://telegram.me/pushitbot) on Telegram to check it out.

API Docs
=========

----

Getting Started
---------------

To start, please open your **Telegram** app and start a chat with [@PushItBot](https://telegram.me/pushitbot) to generate your API *token*.  
You can also start the chat by clicking [here](https://telegram.me/pushitbot?start=token).

Once you have the *token*, **keep it away from others**, it is just for you.

In this page, whenever you see `<YOUR_TOKEN>`, you should replace with the token you obtained here.

Pushing Messages
----------------

In order to push notifications to your **Telegram** account, you need to send HTTP requests to the following address:

    https://tgbots-fopina.rhcloud.com/pushit/<YOUR_TOKEN>


Field     | Type   | Description
:-------: | :----: | :-----------
msg       | string | **Required** The message text you want to send
format    | string | *Optional* Formatting options as supported by [Telegram Bot API](https://core.telegram.org/bots/api#formatting-options). Possible values: *(empty string)*, [*Markdown*](https://core.telegram.org/bots/api#markdown-style), [*HTML*](https://core.telegram.org/bots/api#html-style)

* The URL is case-**sensitive**.
* GET and POST HTTP methods are supported
* CORS headers are included so you can use the API in AJAX calls
* For passing parameters use on of the below ways:
  * [URL query string](https://en.wikipedia.org/wiki/Query_string) (for GET)
  * [application/x-www-form-urlencoded](https://en.wikipedia.org/wiki/Percent-encoding#The_application.2Fx-www-form-urlencoded_type) (for POST)
  * application/json (for POST)

Source - Host your own
======================

----

Check out the project in [Github](https://github.com/fopina/tgbot-pushitbot).  
[README](https://github.com/fopina/tgbot-pushitbot/blob/master/README.md) has instructions on how to quickly set up your own copy of @PushItBot in OpenShift!
