import requests
def PushBot(data,conf):
    url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+conf['bot_key']
    requests.post(url,json=data)
