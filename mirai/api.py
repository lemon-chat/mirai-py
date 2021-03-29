
import os
import json
from functools import partial
from typing import Optional

import requests
from urllib.parse import urljoin
from urllib.parse import quote
from tenacity import retry

from .httpapi import MiraiHttpApi
from .session import MiraiSession
from .message.chain import MessageChain
from .message.messages import Message


class MiraiApi(object):
    def __init__(self, host: str, authKey: str):
        self.host = host
        self.authKey = authKey
        self.llapi = MiraiHttpApi(host)

    def get_session(self, account: str):
        return MiraiSession(self.llapi, account, self.authKey)
