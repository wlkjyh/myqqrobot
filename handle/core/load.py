import handle.constant as constant
from handle.core.deny import deny as denyFunc
import os
from handle.core.Log import Log as log
import handle.running
import re
import json


def controller(packageName,alias=None):
    """加载控制器

    Args:
        packageName (string): 控制器名称
        alias (string): 为控制器设置别名，默认为None，不设置别名

    Returns:
        bool: 是否加载成功
    """    
    # /app/controller/{PackageName}.py
    if os.path.exists(constant.APP_CONTROLLER_PATH + packageName + '.py'):
        # return __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)
        
        if alias is None:
            handle.running.controller[packageName] = __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)
        else:
            handle.running.controller[alias] = __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)

        return True
    else:
        log.error('控制器 "' + packageName + '" 不存在。')
        log.error('程序停止运行')
        os._exit(0)

def middleware(packageName,alias=None):
    """加载中间件

    Args:
        packageName (string): 中间件名称
        alias (string): 为中间件设置别名，默认为None，不设置别名

    Returns:
        bool: 是否加载成功
    """    
    # /app/middleware/{PackageName}.py
    if os.path.exists(constant.APP_MIDDLEWARE_PATH + packageName + '.py'):
        # return __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)
        if alias is None:
            handle.running.middleware[packageName] = __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)
        else:
            handle.running.middleware[alias] = __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)

        return True
    else:
        log.error('中间件 "' + packageName + '" 不存在。')
        log.error('程序停止运行')
        os._exit(0)


def deny(json_file):
    """加载黑名单

    Args:
        json_file (string): 黑名单文件路径
    """    
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r',encoding='utf-8') as f:
                data = json.load(f)
                for group in data['group']:
                    denyFunc.group(group_id=group, remove=False)
                for user in data['user']:
                    denyFunc.user(user_id=user, remove=False)


        except Exception as e:
            log.warning(str(e))

    else:
        log.warning('找不到指定的黑名单文件，未能完成黑名单加载。')