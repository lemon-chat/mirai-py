import mirai
from mirai.api import MiraiHttpApi, MiraiApi
from mirai.message.chain import MessageChain
from mirai.message.element import Plain
if __name__ == "__main__":
    lowlevel_api = MiraiHttpApi('http://localhost:8080')
    api = MiraiApi('http://localhost:8080', '')

    with api.get_session('') as sess:
        message = MessageChain.create([Plain('测试')])
        sess.sendGroupMessage(8888, message)