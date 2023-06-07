import threading
from app.kernel import kernel as kernel
import handle.running as running
import re
import handle.support.key as key
from handle.support.middleware import Middleware as Middleware


class handler:


    def __init__(self):
        pass


    """" 
        构建一个线程来处理消息
    
    """
    def childThread(self,instance):
        # 开始解析路由，来分发给中间件

        msg_type = instance.msg_type

        if msg_type == key.MESSAGE_MESSAGE:
            route = running.route
        else:
            route = running.event

        for rule in route:


            route_alias = rule['alias']
            route_reg = rule['reg']

            register_reg = []
            
            if len(route_alias) > 0:
                for alias in route_alias:
                    value = route_alias[alias]
                    value_split = value.split('|')
                    for single in value_split:
                        reg = route_reg.replace('<' + alias + '>',single)
                        register_reg.append(reg)

                    reg = route_reg.replace('<' + alias + '>',alias)
                    register_reg.append(reg)
            else:
                register_reg.append(route_reg)


            ifMessage = instance.message
            for reg in register_reg:
                matchs = re.match(reg,ifMessage)
                if matchs and instance.type == rule['type']:
                    # print(matchs.groups())
                    # break
                    instance.set_kv('match',matchs.groups())


                    # 中间件优先级：全局中间件 -> 分组中间件 -> 路由中间件

                    middleware_1 = running.middleware_global
                    if instance.type == key.MESSAGE_GROUP:
                        middleware_2 = running.middleware_group
                    else:
                        middleware_2 = running.middleware_private


                    middleware_3 = rule['middleware']

                    middlewareBak = middleware_1 + middleware_2 + middleware_3

                    middleware = []
                    middleware_name = []
                    for m in middlewareBak:
                        middName = m.__name__
                        if middName not in middleware_name:
                            middleware_name.append(middName)
                            middleware.append(m)

                    instance.set_kv('middleware',middleware)

                    next_middleware = middleware[0]
                    index = 0
                    instance.set_kv('middleware_load_index',index)
                    instance.set_kv('middleware_load_next',next_middleware)


                    instance.set_kv('controller',rule['controller'])
                    instance.set_kv('action',rule['action'])

                    Middleware().next(instance)

        pass

    """ 
        这里接收到了预处理的消息
    """
    def next(self,instance):
        # 加上锁，开发者可以自己选择是否加锁
        lock = threading.RLock()
        instance.set_kv('lock',lock)

        t = threading.Thread(target=self.childThread,args=(instance,))
        """ 
            这里使用daemon线程，主线程结束后，子线程也会结束
        """
        t.daemon = True
        t.start()



        return True


        pass