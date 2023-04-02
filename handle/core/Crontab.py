import handle.running as running
from handle.core.Log import Log as Log
import re

class Crontab:

    def __init__(self):
        pass


    @staticmethod
    def set(controller,action,crontab_type='cron',day_of_week=None,month=None,day=None,hour=None,minute=None,second=None):
        """
            设置一个定时任务
        """
        if controller not in running.controller:
            Log.error('控制器 ' + controller + ' 不存在。')
            return False
        
        if crontab_type != 'cron' and crontab_type != 'interval':
            Log.error('定时任务类型错误。' + crontab_type)
            Log.error('程序停止运行。')
            exit()
            return False

        running.crontab.append({
            'controller' : running.controller[controller],
            'action' : action,
            'type' : crontab_type,
            'day_of_week' : day_of_week,
            'month' : month,
            'day' : day,
            'hour' : hour,
            'minute' : minute,
            'second' : second
        })