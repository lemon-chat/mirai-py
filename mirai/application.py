import json
from typing import Callable, NoReturn
import time, threading
import concurrent
from collections import defaultdict

from mirai.api import MiraiApi
from mirai.message.chain import MessageChain
from mirai.message.messages import Message
from mirai.event import BaseEvent, GroupMessageEvent, FriendMessageEvent
from mirai.sender import FriendSender

class Listener(object):
    def __init__(self, event: str, handler:Callable):
        self.event = event
        self.handler = handler

class MiraiApp(object):
    def __init__(self, host:str, authKey:str, account:str, logger=None):
        self.host = host
        self.authKey = authKey
        self.account = account
        self.api = MiraiApi(host, authKey)
        self.session = None
        self.listeners = defaultdict(list)

    @staticmethod
    def dispatch_event(app, event):
        event_type = event['type']
        for listener in app.listeners[event_type]:
            if event_type == 'GroupMessage':
                handler_event = GroupMessageEvent(MessageChain.parse_obj(event['messageChain']), event['sender'])
            elif event_type == 'FriendMessage':
                handler_event = FriendMessageEvent(MessageChain.parse_obj(event['messageChain']), FriendSender(**event['sender']))
            listener.handler(app, handler_event)
    
    def fn_message_thread(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            history = []
            quick_history_set = set()
            loop_count = 0
            while True:
                if loop_count % 1000 == 0:
                    quick_history_set = set([json.dumps(d) for d in history[50:]])

                ret = self.session.peekLatestMessage(count=50)
                for each_event in ret:
                    event_id = json.dumps(each_event)
                    if event_id not in quick_history_set:
                        history.append(each_event)
                        quick_history_set.add(event_id)
                        executor.submit(self.dispatch_event, self, each_event)

                time.sleep(1)
                loop_count += 1

    def blocking_start(self) -> NoReturn:
        self.fn_message_thread()

    def auth(self) -> NoReturn:
        self.session = self.api.get_session(self.account)
        self.session.auth()

    def leave(self) -> NoReturn:
        self.session.leave()
        self.session = None

    def __enter__(self):
        self.auth()
        return self

    def __exit__(self, type, value, trace) -> NoReturn:
        self.leave()

    def register(self, event: str, handler: Callable) -> NoReturn:
        self.listeners[event].append(Listener(event, handler))

    def sendGroupMessage(self, target: int, message: MessageChain) -> Message:
        return self.session.sendGroupMessage(target=target, messageChain=message)
    
    def sendFriendMessage(self, target: int, message: MessageChain) -> Message:
        return self.session.sendFriendMessage(target=target, messageChain=message)
