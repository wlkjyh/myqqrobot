"""
    加载服务提供者
"""


import os
from handle.core.Log import Log as Log


provider_dir = os.path.dirname(os.path.dirname(__file__)) + '/provider'
for dirs in os.listdir(provider_dir):
    real_provider_dir = provider_dir + '/' + dirs

    try:
        # check route and info
        if not os.path.exists(real_provider_dir + '/route.py') or not os.path.exists(real_provider_dir + '/info.py'):
            Log.warning('无法加载服务提供者“' + dirs + '”，因为服务提供者的路由文件和信息文件都不存在')

        provider_info = __import__('provider.' + dirs + '.info', fromlist=True)
        NAME = provider_info.SERVICE_NAME
        VERSION = provider_info.SERVICE_VERSION
        SERVICE_PROVIDER = provider_info.SERVICE_PROVIDER
        DESCRIPTION = provider_info.SERVICE_DESCRIPTION
        BOOT = provider_info.BOOT
        if not BOOT:
            continue

        Log.info('正在加载服务提供者：' + NAME + '\n版本：' + VERSION + '\n描述：' + DESCRIPTION + '\n提供者：' + SERVICE_PROVIDER + '\n')

        __import__('provider.' + dirs + '.route', fromlist=True)
        Log.info('服务提供者“' + NAME + '”加载完成')

    except Exception as e:
        Log.error('无法加载服务提供者“' + dirs + '”，因为‘' + str(e) + '’')
    

