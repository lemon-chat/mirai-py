
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NoReturn,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    Optional,
)
from .element import Element

class MessageChain(object):
    def __init__(self, messages: Optional[Iterable]=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    @classmethod
    def create(cls, elements: Sequence[Element]) -> "MessageChain":
        """从传入的序列(可以是元组 tuple, 也可以是列表 list) 创建消息链.

        Args:
            elements (Sequence[T]): 包含且仅包含消息元素的序列

        Returns:
            MessageChain: 以传入的序列作为所承载消息的消息链
        """
        if not isinstance(elements, Sequence):
            raise Exception("参数必须是序列类型")
        return cls(messages=elements)

    def dict(self):
        return [m.dict() for m in self.messages]
    