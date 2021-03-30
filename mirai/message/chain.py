
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
    Optional
)
import copy
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

    
    def subchain(self, item: slice, ignore_text_index: bool = False) -> "MessageChain":
        """对消息链执行分片操作

        Args:
            item (slice): 这个分片的 `start` 和 `end` 的 Type Annotation 都是 `Optional[MessageIndex]`

        Raises:
            TypeError: TextIndex 取到了错误的位置

        Returns:
            MessageChain: 分片后得到的新消息链, 绝对是原消息链的子集.
        """
        from .element import Plain

        result = copy.copy(self.messages)
        if item.start:
            first_slice = result[item.start[0] :]
            if item.start[1] is not None and first_slice:  # text slice
                if not isinstance(first_slice[0], Plain):
                    if not ignore_text_index:
                        raise TypeError(
                            "the sliced chain does not starts with a Plain: {}".format(
                                first_slice[0]
                            )
                        )
                    else:
                        result = first_slice
                else:
                    final_text = first_slice[0].text[item.start[1] :]
                    result = [
                        *([Plain(final_text)] if final_text else []),
                        *first_slice[1:],
                    ]
            else:
                result = first_slice
        if item.stop:
            first_slice = result[: item.stop[0]]
            if item.stop[1] is not None and first_slice:  # text slice
                if not isinstance(first_slice[-1], Plain):
                    raise TypeError(
                        "the sliced chain does not ends with a Plain: {}".format(
                            first_slice[-1]
                        )
                    )
                final_text = first_slice[-1].text[: item.stop[1]]
                result = [
                    *first_slice[:-1],
                    *([Plain(final_text)] if final_text else []),
                ]
            else:
                result = first_slice
        return MessageChain.create(result)
    
    def has(self, element_class: Element) -> bool:
        """判断消息链中是否含有特定类型的消息元素

        Args:
            element_class (T): 需要判断的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            bool: 判断结果
        """
        return element_class in [type(i) for i in self.messages]

    def get(self, element_class: Element) -> List[Element]:
        """获取消息链中所有特定类型的消息元素

        Args:
            element_class (T): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            List[T]: 获取到的符合要求的所有消息元素; 另: 可能是空列表([]).
        """
        return [i for i in self.messages if type(i) is element_class]

    def getOne(self, element_class: Element, index: int) -> Element:
        """获取消息链中第 index + 1 个特定类型的消息元素

        Args:
            element_class (Type[Element]): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.
            index (int): 索引, 从 0 开始数

        Returns:
            T: 消息链第 index + 1 个特定类型的消息元素
        """
        return self.get(element_class)[index]

    def getFirst(self, element_class: Element) -> Element:
        """获取消息链中第 1 个特定类型的消息元素

        Args:
            element_class (Type[Element]): 指定的消息元素的类型, 例如 "Plain", "At", "Image" 等.

        Returns:
            T: 消息链第 1 个特定类型的消息元素
        """
        return self.getOne(element_class, 0)

    def asDisplay(self) -> str:
        """获取以字符串形式表示的消息链, 且趋于通常你见到的样子.

        Returns:
            str: 以字符串形式表示的消息链
        """
        return "".join(i.asDisplay() for i in self.messages)
    
    def __getitem__(self, item: Union[Type[Element], slice]):
        if isinstance(item, slice):
            return self.subchain(item)
        elif issubclass(item, Element):
            return self.get(item)
        else:
            raise NotImplementedError(
                "{0} is not allowed for item getting".format(type(item))
            )