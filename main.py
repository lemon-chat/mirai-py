import mirai
import random
from mirai.api import MiraiApi
from mirai.application import MiraiApp
from mirai.message.chain import MessageChain
from mirai.message.element import Plain, Source
from mirai.event import GroupMessageEvent, FriendMessageEvent, BotUnmuteEvent

import requests

import time


def onGroupMessage(app: MiraiApp, event: GroupMessageEvent):
    words = ['是的呢', '对', '对的', '说得好',
             '是这样的', 'TQL', '没错', '嗯', '的确', '确实']
    # ret = requests.get('https://chp.shadiao.app/api.php')
    message = MessageChain.create([Plain(random.choice(words))])
    if event.sender.group.id == 667481568:
        app.sendGroupMessage(target=event.sender.group.id, message=message)

def onFriendMessage(app: MiraiApp, event: FriendMessageEvent):
    words = ['是的呢', '对', '对的', '说得好',
             '是这样的', 'TQL', '没错', '嗯', '的确', '确实']
    message = MessageChain.create([Plain(random.choice(words))])
    sender_id = event.sender.id
    app.sendFriendMessage(target=sender_id, message=message)

def onBotUnmute(app: MiraiApp, event: BotUnmuteEvent):
    message = MessageChain.create([Plain('嘻嘻我被放出来了')])
    group_id = event.operator.group.id
    app.sendGroupMessage(target=group_id, message=message)

if __name__ == "__main__":
    with MiraiApp('http://localhost:8080', '', '') as app:
        # 显示所有好友
        for f in app.friendList():
            print(f.nickname)
        # 事件响应注册
        app.register('GroupMessage', onGroupMessage)
        app.register('FriendMessage', onFriendMessage)
        app.register(BotUnmuteEvent, onBotUnmute)
        app.blocking_start()
