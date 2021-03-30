

class BaseEvent(object):
    pass


class GroupMessageEvent(object):
    def __init__(self, messageChain, sender):
        self.messageChain = messageChain
        self.sender = sender

class FriendMessageEvent(object):
    def __init__(self, messageChain, sender):
        self.messageChain = messageChain
        self.sender = sender