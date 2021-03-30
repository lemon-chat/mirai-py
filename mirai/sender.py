from typing import NoReturn, Any, Dict


class BaseSender(object):
    pass


class Group(object):
    def __init__(self, id: int, name: str, permission: str):
        self.id = id
        self.name = name
        self.permission = permission


class GroupMessageSender(object):
    def __init__(self: 'GroupMessageSender', id: int, memberName: str, permission: str, group: Group) -> NoReturn:
        self.id = id
        self.memberName = memberName
        self.permission = permission
        self.group = group

    @classmethod
    def parse_obj(cls, obj: Dict) -> "GroupMessageSender":
        return GroupMessageSender(
            id=obj['id'],
            memberName=obj['memberName'],
            permission=obj['permission'],
            group=Group(**obj['group'])
        )


class FriendMessageSender(object):
    def __init__(self: 'FriendMessageSender', id: int, nickname: str, remark: str) -> NoReturn:
        self.id = id
        self.nickname = nickname
        self.remark = remark

    @classmethod
    def parse_obj(cls, obj: Dict) -> "FriendMessageSender":
        return FriendMessageSender(
            id=obj['id'],
            nickname=obj['nickname'],
            remark=obj['remark'])
