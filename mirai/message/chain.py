
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
from .element import Element, InternalElement, ExternalElement

from pydantic import BaseModel

class MessageChain(BaseModel):
    messages: Sequence[Element]

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

    @classmethod
    def parse_obj(cls: Type["MessageChain"], obj: List[Element]) -> "MessageChain":
        """内部接口, 会自动将作为外部态的消息元素转为内部态.

        Args:
            obj (List[T]): 需要反序列化的对象

        Returns:
            MessageChain: 内部承载有尽量有效的内部态消息元素的消息链
        """
        handled_elements = []
        for i in obj:
            if isinstance(i, InternalElement):
                handled_elements.append(i)
            elif isinstance(i, ExternalElement):
                for ii in InternalElement.__subclasses__():
                    if ii.__name__ == i.__class__.__name__:
                        handled_elements.append(ii.fromExternal(i))
            elif isinstance(i, dict) and "type" in i:
                for ii in ExternalElement.__subclasses__():
                    if ii.__name__ == i["type"]:
                        for iii in InternalElement.__subclasses__():
                            if iii.__name__ == i["type"]:
                                handled_elements.append(
                                    iii.fromExternal(ii.parse_obj(i))
                                )
        return cls(messages=tuple(handled_elements))  # 默认是不可变型

    def dict(self):
        return [m.dict() for m in self.messages]