
import handle.running as ri
from handle.core.Log import Log as Log

class Route:
    def __init__(self):
        pass



    """
        私聊消息注册
    """
    @staticmethod
    def private(reg,controller,action,middleware=[],alias=[]):
        """私聊消息注册

        Args:
            reg (string): 正则表达式匹配消息规则
            controller (string): 控制器名称，必须是已经加载的控制器
            action (string): 控制器中的方法名称
            middleware (list): 中间件列表，必须是已经加载的中间件
            alias (list): 匹配别名列表，在reg中必须使用<>包裹，那么被包裹的字符可以设置别名

        Returns:
            bool: 是否注册成功
        """        
        if controller not in ri.controller:
            Log.error('控制器 ' + controller + ' 不存在。')
            return False
        
        for i in middleware:
            if i not in ri.middleware:
                Log.error('中间件 ' + i + ' 不存在。')
                return False
            

        
        ri.route.append({
            'type' : 'private',
            'reg' : reg,
            'controller' : ri.controller[controller],
            'action' : action,
            'middleware' : [ri.middleware[i] for i in middleware],
            'alias' : alias
        })

        return True
            
        

        pass


    @staticmethod
    def group(reg,controller,action,middleware=[],alias=[]):
        """群聊消息注册

        Args:
            reg (string): 正则表达式匹配消息规则
            controller (string): 控制器名称，必须是已经加载的控制器
            action (string): 控制器中的方法名称
            middleware (list): 中间件列表，必须是已经加载的中间件
            alias (list): 匹配别名列表，在reg中必须使用<>包裹，那么被包裹的字符可以设置别名

        Returns:
            bool: 是否注册成功
        """     
        if controller not in ri.controller:
            Log.error('控制器 ' + controller + ' 不存在。')
            return False
        
        for i in middleware:
            if i not in ri.middleware:
                Log.error('中间件 ' + i + ' 不存在。')
                return False
        
        ri.route.append({
            'type' : 'group',
            'reg' : reg,
            'controller' : ri.controller[controller],
            'action' : action,
            'middleware' : [ri.middleware[i] for i in middleware],
            'alias' : alias
        })
        return True

        pass

    @staticmethod
    def any(reg,controller,action,middleware=[],alias=[]):
        """任意消息注册

        Args:
            reg (string): 正则表达式匹配消息规则
            controller (string): 控制器名称，必须是已经加载的控制器
            action (string): 控制器中的方法名称
            middleware (list): 中间件列表，必须是已经加载的中间件
            alias (list): 匹配别名列表，在reg中必须使用<>包裹，那么被包裹的字符可以设置别名

        Returns:
            bool: 是否注册成功
        """


        # 注册任意消息其实就是注册私聊消息和群聊消息
        
        Route.private(reg,controller,action,middleware,alias)
        Route.group(reg,controller,action,middleware,alias)

        return True

        pass