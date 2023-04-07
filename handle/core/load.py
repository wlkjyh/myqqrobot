import handle.constant as constant
from handle.core.deny import deny as denyFunc
import os
from handle.core.Log import Log as log
import handle.running
import re
import json
import inspect

def controller(packageName,alias=None):
    # 获取谁调用了这个方法，具体文件名
    register_stack = inspect.stack()[1][1]

    is_provider = False
    if 'register.py' not in register_stack and 'provider' in register_stack:
        # 服务提供者需要加载控制器
        # print('服务提供者需要加载控制器')
        is_provider = True
        
    

    """加载控制器

    Args:
        packageName (string): 控制器名称
        alias (string): 为控制器设置别名，默认为None，不设置别名

    Returns:
        bool: 是否加载成功
    """    
    # /app/controller/{PackageName}.py
    if not is_provider:
        if os.path.exists(constant.APP_CONTROLLER_PATH + packageName + '.py'):
            # return __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)
            
            if alias is None:
                handle.running.controller[packageName] = __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)
            else:
                handle.running.controller[alias] = __import__(constant.APP_CONTROLLER_NAMESPACE + '.' + packageName, fromlist=True)

            return True
        else:
            log.error('不能加载控制器“' + packageName + '”，因为找不到：' + constant.APP_CONTROLLER_PATH + packageName + '.py' + "文件")
            log.error('程序停止运行')
            os._exit(0)
    else:
        # 获取register_stack的目录
        register_stack_dir = os.path.dirname(register_stack)
        split = register_stack_dir.replace('\\','.').replace('/','.').split('.provider.')
        if len(split) < 2:
            log.error('服务提供者加载控制器必须在provider\\提供者名称目录下')
            log.error('程序停止运行')
            os._exit(0)
        namespace = 'provider.' + split[1] + '.' + packageName
        real_packageName = packageName.replace('.','\\')
        if not os.path.exists(register_stack_dir + '\\' + real_packageName + '.py'):
            log.error('不能加载服务提供者“' + split[1] + '”所提供的控制器“' + packageName + '”，因为找不到：' + register_stack_dir + '\\' + real_packageName + '.py' + "文件")
            log.error('程序停止运行')
            os._exit(0)

        if alias is None:
            handle.running.controller[packageName] = __import__(namespace, fromlist=True)
        else:
            handle.running.controller[alias] = __import__(namespace, fromlist=True)

        return True





def middleware(packageName,alias=None):
    """加载中间件

    Args:
        packageName (string): 中间件名称
        alias (string): 为中间件设置别名，默认为None，不设置别名

    Returns:
        bool: 是否加载成功
    """    
    register_stack = inspect.stack()[1][1]

    is_provider = False
    if 'register.py' not in register_stack and 'provider' in register_stack:
        # 服务提供者需要加载控制器
        # print('服务提供者需要加载控制器')
        is_provider = True
    
    if not is_provider:
        # /app/middleware/{PackageName}.py
        if os.path.exists(constant.APP_MIDDLEWARE_PATH + packageName + '.py'):
            # return __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)
            if alias is None:
                handle.running.middleware[packageName] = __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)
            else:
                handle.running.middleware[alias] = __import__(constant.APP_MIDDLEWARE_NAMESPACE + '.' + packageName, fromlist=True)

            return True
        else:
            log.error('不能加载中间件“' + packageName + '”，因为找不到：' + constant.APP_MIDDLEWARE_PATH + packageName + '.py' + "文件")
            log.error('程序停止运行')
            os._exit(0)
    else:
        register_stack_dir = os.path.dirname(register_stack)
        split = register_stack_dir.replace('\\','.').replace('/','.').split('.provider.')
        if len(split) < 2:
            log.error('服务提供者加载中间件必须在provider\\提供者名称目录下')
            log.error('程序停止运行')
            os._exit(0)
        namespace = 'provider.' + split[1] + '.' + packageName
        real_packageName = packageName.replace('.','\\')
        if not os.path.exists(register_stack_dir + '\\' + real_packageName + '.py'):
            log.error('不能加载服务提供者“' + split[1] + '”所提供的中间件“' + packageName + '”，因为找不到：' + register_stack_dir + '\\' + real_packageName + '.py' + "文件")
            log.error('程序停止运行')
            os._exit(0)
        
        if alias is None:
            handle.running.middleware[packageName] = __import__(namespace, fromlist=True)
        else:
            handle.running.middleware[alias] = __import__(namespace, fromlist=True)

        return False



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