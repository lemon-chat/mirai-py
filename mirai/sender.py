from typing import NoReturn
class BaseSender(object):
    pass


class FriendSender(object):
    def __init__(self: 'FriendSender', id: int, nickname: str, remark: str) -> NoReturn:
        self.id = id
        self.nickname = nickname
        self.remark = remark
