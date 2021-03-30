
from typing import Dict

from mirai.message.chain import MessageChain
from mirai.message.messages import Message
from mirai.sender import BaseSender, Friend, GroupMessageSender


class BaseEvent(object):
    pass


class MemberCardChangeEvent(BaseEvent):
    name = 'MemberCardChangeEvent'

    def __init__(self, origin: str, new: str, current: str, member: GroupMessageSender, operator: None):
        self.origin = origin
        self.new = new
        self.current = current
        self.member = member
        self.operator = operator


class BotMuteEvent(BaseEvent):
    name = 'BotMuteEvent'

    def __init__(self, durationSeconds: int, operator: GroupMessageSender):
        self.durationSeconds = durationSeconds
        self.operator = operator

    @classmethod
    def parse_obj(cls, obj: Dict) -> "BotMuteEvent":
        return BotMuteEvent(
            durationSeconds=obj['durationSeconds'],
            operator=GroupMessageSender.parse_obj(obj['operator']))


class BotUnmuteEvent(BaseEvent):
    name = 'BotUnmuteEvent'

    def __init__(self, operator: GroupMessageSender):
        self.operator = operator

    @classmethod
    def parse_obj(cls, obj: Dict) -> "BotUnmuteEvent":
        return BotUnmuteEvent(
            operator=GroupMessageSender.parse_obj(obj['operator']))


class BotReloginEvent(BaseEvent):
    name = 'BotReloginEvent'

    def __init__(self, qq: int):
        self.qq = qq

    @classmethod
    def parse_obj(cls, obj: Dict) -> "BotReloginEvent":
        return BotReloginEvent(qq=obj['qq'])


class BotOnlineEvent(BaseEvent):
    name = 'BotOnlineEvent'

    def __init__(self, qq: int):
        self.qq = qq

    @classmethod
    def parse_obj(cls, obj: Dict) -> "BotOnlineEvent":
        return BotOnlineEvent(qq=obj['qq'])


class BotOfflineEventDropped(BaseEvent):
    name = 'BotOfflineEventDropped'

    def __init__(self, qq: int):
        self.qq = qq

    @classmethod
    def parse_obj(cls, obj: Dict) -> "BotOfflineEventDropped":
        return BotOfflineEventDropped(qq=obj['qq'])


class GroupMessageEvent(BaseEvent):
    name = 'GroupMessage'

    def __init__(self, messageChain: MessageChain, sender: GroupMessageSender):
        self.messageChain = messageChain
        self.sender = sender

    @classmethod
    def parse_obj(cls, obj: Dict) -> "GroupMessageEvent":
        return GroupMessageEvent(
            messageChain=MessageChain.parse_obj(obj['messageChain']),
            sender=GroupMessageSender.parse_obj(obj['sender']))


class FriendMessageEvent(BaseEvent):
    name = 'FriendMessage'

    def __init__(self, messageChain: MessageChain, sender: Friend):
        self.messageChain = messageChain
        self.sender = sender

    @classmethod
    def parse_obj(cls, obj: Dict) -> "FriendMessageEvent":
        return FriendMessageEvent(
            messageChain=MessageChain.parse_obj(obj['messageChain']),
            sender=Friend.parse_obj(obj['sender']))
