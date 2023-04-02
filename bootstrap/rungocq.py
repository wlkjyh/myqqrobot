import sys
import os
import handle.constant as constant
from handle.core.Log import Log as Log

def startwithgocq():
    if sys.platform == 'win32':
        F = constant.GOCQ_FILE.replace('/','\\')
        if os.path.exists(F) == False:
            Log.error('未找到go-cqhttp文件，请检查配置文件中的路径是否正确。')
            os._exit(0)

        command = 'start cmd /K "' + F + '"'
        os.system(command)
    else:
        command = 'nohup ' + constant.GOCQ_FILE + ' > /dev/null 2>&1 &'
        os.system(command)
    


def run():
    if constant.AUTO_START_GOCQ == True:
        startwithgocq()
        Log.info('go-cqhttp 已完成自动启动。')
    else:
        Log.warning('现在你需要手动启动go-cqhttp。')
