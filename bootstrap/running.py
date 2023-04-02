import app.kernel
import route.register
import route.blackhole
import bootstrap.rungocq as rgcq
from handle.core.Log import Log as Log
import handle.running as running
import time
import handle.support.key as key
from handle.support.Cache import Cache as Cache
import threading


def run():
    Log.info('欢迎使用 MyCQBot 机器人框架')
    

    # 启动go-cqhttp
    rgcq.run()

    # 加载中间件
    from app.kernel import kernel as kernel
    middleware_1 = kernel().middleware
    running.middleware_global = [ running.middleware[middleware] for middleware in middleware_1 ]

    middleware_group = kernel().middlewareGroups[key.MESSAGE_GROUP]
    running.middleware_group = [ running.middleware[middleware] for middleware in middleware_group ]
    middleware_private = kernel().middlewareGroups[key.MESSAGE_PRIVATE]
    running.middleware_private = [ running.middleware[middleware] for middleware in middleware_private ]

    # 加载cache守护进程服务
    t = threading.Thread(target=Cache().daemon)
    t.setDaemon(True)
    t.start()

    # 加载计划任务
    import handle.kernel.crontab as crontab
    crontab.crontab().start()

    # 加载模板引擎
    import bootstrap.template

    # 加载flask后端服务
    import bootstrap.flaskService as flaskService


    # 加载测试模块
    import bootstrap.test as test

    pass