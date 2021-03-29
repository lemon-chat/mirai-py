import mirai
from mirai.api import MiraiApi
from mirai.application import MiraiApp
from mirai.message.chain import MessageChain
from mirai.message.element import Plain

import time

if __name__ == "__main__":
    with MiraiApp('http://localhost:8080', '', '') as app:
        def onGroupMessage(event):
            message = MessageChain.create([Plain('是的呢')])
            app.session.sendGroupMessage(target=1038774584, messageChain=message)
        app.register('GroupMessage', onGroupMessage)
        app.blocking_start()