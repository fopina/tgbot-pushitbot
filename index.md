---
layout: index
---

PushItBot allows you to easily get notifications from your website or scripts on your Telegram window.

Just talk to [@PushItBot](https://telegram.me/pushitbot) on Telegram to check it out.

- [API Docs](#api-docs)
  - [Getting Started](#getting-started)
  - [Pushing Messages](#pushing-messages)
- [API Usage Examples](#api-usage-examples)
  - [Any browser](#any-browser)
  - [cURL](#curl)
  - [JavaScript](#javascript)
  - [Python](#python)
  - [PHP](#php)
- [Source - Host your own](#source---host-your-own)

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
* [CORS](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) headers are included so you can use the API in AJAX calls
* For passing parameters use on of the below ways:
  * [URL query string](https://en.wikipedia.org/wiki/Query_string) (for GET)
  * [application/x-www-form-urlencoded](https://en.wikipedia.org/wiki/Percent-encoding#The_application.2Fx-www-form-urlencoded_type) (for POST)
  * application/json (for POST)

API Usage Examples
==================

---

Remember to replace the sample token `105e48ff92b92263f3397ed55f275a81` with your own!

### Any browser

Just load the URL (using GET)

    https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81?msg=testing+1+2+3


### cURL

```bash
curl -d 'msg=*testing* _1_ `2` 3' \
     -d "format=Markdown" \
     https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81
```

### JavaScript

With jQuery

```javascript
$.ajax("https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81", {
    type:"POST",
    data: {"msg": "*testing* _1_ `2` 3", "format": "Markdown"},
    dataType: 'json',
    success:function(data, textStatus, jqXHR) {
      if (data.ok) {
        alert("Message sent!");
      }
      else {
        alert("Failed (" + data.code + "): " + data.description);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {alert("API Failure");}
});
```

### Python

With urllib2

```python
import urllib
import urllib2
import json

r = urllib2.urlopen(
  'https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81',
  data=urllib.urlencode({
    'msg': '<b>testing</b> <i>1</i> <code>2</code> 3',
    'format': 'HTML'
  })
)
print json.loads(r.read())
```

With requests

```python
import requests

r = requests.post(
  'https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81',
  data={
    'msg': '<b>testing</b> <i>1</i> <code>2</code> 3',
    'format': 'HTML'
  }
)
print r.json()
```

### PHP

With cURL

```php
<?php
$params = array(
	'msg' => "testing 1 2 3"
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
$result = curl_exec($ch);
curl_close($ch);

print_r($result);
?>
```

With `file_get_contents()`

```php
<?php
$params = array(
	'msg' => "testing 1 2 3"
);
$post = http_build_query($params);

$context = stream_context_create(array(
                'http' => array(
                    'method' => 'POST',
                    'header' => "Content-type: application/x-www-form-urlencoded\r\n",
                    'content' => $post,
                    'timeout' => 10,
                ),
            ));

$response = file_get_contents("https://tgbots-fopina.rhcloud.com/pushit/105e48ff92b92263f3397ed55f275a81", false, $context);
print $response
?>
```

Source - Host your own
======================

----

Check out the project in [Github](https://github.com/fopina/tgbot-pushitbot).  
[README](https://github.com/fopina/tgbot-pushitbot/blob/master/README.md) has instructions on how to quickly set up your own copy of @PushItBot in OpenShift!
