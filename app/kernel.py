import handle.core.load as load
import handle.support.key as key

"""
    必须要先加载中间件，才能调用中间件
"""
load.middleware(packageName='NoiseMiddleware')
load.middleware(packageName='blackholeMiddleware',alias='blackhole')

class kernel:
    """
        全局中间件
    """
    middleware = [
        # blackhole是黑名单中间件，用于对黑名单用户和群组进行拦截
        'blackhole'
    ]


    """
        指定消息类型的中间件组
    """
    middlewareGroups = {
        # 群聊消息中间件
        key.MESSAGE_GROUP : [
            'NoiseMiddleware'
        ],
        # 私聊消息中间件
        key.MESSAGE_PRIVATE : [
        
        ]
    }