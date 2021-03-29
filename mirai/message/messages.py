
from .chain import MessageChain

class Message(object):
    def __init__(self, messageId:int, messageChain: MessageChain):
        self.messageId = messageId
        self.chain = messageChain