import mirai
import random
from mirai.api import MiraiApi
from mirai.application import MiraiApp
from mirai.message.chain import MessageChain
from mirai.message.element import Plain, Source
from mirai.event import GroupMessageEvent

import requests

import time


def onGroupMessage(app: MiraiApp, event: GroupMessageEvent):
    words = ['是的呢', '对', '对的', '说得好',
             '是这样的', 'TQL', '没错', '嗯', '的确', '确实']
    ret = requests.get('https://chp.shadiao.app/api.php')
    message = MessageChain.create([Plain(ret.text)])
    app.sendGroupMessage(target=1038774584, message=message)

def onFriendMessage(app: MiraiApp, event: GroupMessageEvent):
    words = ['是的呢', '对', '对的', '说得好',
             '是这样的', 'TQL', '没错', '嗯', '的确', '确实']
    message = MessageChain.create([Plain(random.choice(words))])
    sender_id = event.sender.id
    app.sendFriendMessage(target=sender_id, message=message)

if __name__ == "__main__":
    with MiraiApp('http://localhost:8080', '', '') as app:
        # app.register('GroupMessage', onGroupMessage)
        app.register('FriendMessage', onFriendMessage)
        app.blocking_start()
