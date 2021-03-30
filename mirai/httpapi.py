
import json
from functools import partial
from typing import Optional

import requests
from urllib.parse import urljoin
from urllib.parse import quote
from tenacity import retry


class MiraiHttpApi(object):
    '''
    底层HTTP接口
    文档地址：https://github.com/project-mirai/mirai-api-http/blob/master/docs/API.md
    '''

    def __init__(self, host: str):
        self.host = host

    def check_code(self, code: int):
        if not isinstance(code, int):
            code = int(code)

        if code == 0:
            return
        elif code == 1:
            raise Exception("错误的auth key")
        elif code == 2:
            raise Exception("指定的Bot不存在")
        elif code == 3:
            raise Exception("Session失效或不存在")
        elif code == 4:
            raise Exception("Session未认证(未激活)")
        elif code == 5:
            raise Exception("发送消息目标不存在(指定对象不存在)")
        elif code == 6:
            raise Exception("指定文件不存在，出现于发送本地图片")
        elif code == 10:
            raise Exception("无操作权限，指Bot没有对应操作的限权")
        elif code == 20:
            raise Exception("Bot被禁言，指Bot当前无法向指定群发送消息")
        elif code == 30:
            raise Exception("消息过长")
        elif code == 400:
            raise Exception("错误的访问，如参数错误等")
        return

    # low level apis
    def query_get(self, api_name: str, **kwargs):
        url = urljoin(self.host, '/' + api_name)
        params = [k + "=" + quote(str(v)) for k, v in kwargs.items()]
        if len(params) > 0:
            url = url + '?' + '&'.join(params)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("异常状态码" + str(response.status_code))
        obj = json.loads(response.text)
        if "code" in obj:
            self.check_code(obj["code"])

        return obj

    def query_post(self, api_name: str, **kwargs):
        req_params = kwargs
        url = urljoin(self.host, '/' + api_name)
        response = requests.post(url, json=req_params)
        if response.status_code != 200:
            raise Exception("异常状态码" + str(response.status_code))
        obj = json.loads(response.text)
        if "code" in obj:
            self.check_code(obj["code"])

        return obj

    @retry
    def __getattr__(self, name: str):
        get_list = ['about', 'fetchMessage', 'fetchLatestMessage', 'peekMessage',
                    'peekLatestMessage', 'friendList', 'groupList', 'memberList']
        if name in get_list:
            return partial(self.query_get, name)
        else:
            return partial(self.query_post, name)
