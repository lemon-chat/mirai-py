

import os
import json
from functools import partial
from typing import Optional

from .httpapi import MiraiHttpApi
from .message.chain import MessageChain
from .message.messages import Message

class MiraiSession(object):
    def __init__(self, api: MiraiHttpApi, account: str, authKey: str):
        self.llapi = api
        self.authKey = authKey
        self.account = account
        self.sessionKey = None

    def auth(self):
        sess_response = self.llapi.auth(authKey=self.authKey)
        self.sessionKey = sess_response['session']
        verify_response = self.llapi.verify(
            sessionKey=self.sessionKey, qq=self.account)
        if verify_response['msg'] != "success":
            raise Exception(verify_response['msg'])

    def leave(self):
        release_response = self.llapi.release(
            sessionKey=self.sessionKey, qq=self.account)
        self.sessionKey = None

        if release_response['msg'] != "success":
            raise Exception(release_response['msg'])

    def __enter__(self):
        self.auth()
        # print(f'打开session: {self.sessionKey}')
        return self

    def __exit__(self, type, value, trace):
        # print(f'关闭session: {self.sessionKey}')
        self.leave()
    
    def recall(self, target:int):
        '''
        sessionKey	String	已经激活的Session
        target	    Int	需要撤回的消息的messageId
        '''
        return self.llapi.recall(sessionKey=self.sessionKey, target=target)

    def sendGroupMessage(self, target:int, messageChain: MessageChain, quote:Optional[int]=None):
        '''
        sessionKey	    String	已经激活的Session
        target	        Long	可选，发送消息目标群的群号
        group	        Long	可选，target与group中需要有一个参数不为空，当target不为空时group将被忽略，同target
        quote	        Int	    引用一条消息的messageId进行回复
        messageChain	Array	消息链，是一个消息对象构成的数组
        '''
        if quote is None:
            ret = self.llapi.sendGroupMessage(
                sessionKey=self.sessionKey,
                target=target,
                messageChain=messageChain.dict()
            )
        else:
            ret = self.llapi.sendGroupMessage(
                sessionKey=self.sessionKey,
                target=target,
                quote=quote,
                messageChain=messageChain.dict()
            )
        
        return Message(ret['messageId'], messageChain)
        
    def peekLatestMessage(self, count:int):
        '''
        sessionKey	你的session key
        count   	获取消息和事件的数量
        '''
        ret = self.llapi.peekLatestMessage(sessionKey=self.sessionKey, count=count)
        data = ret['data']
        return data
