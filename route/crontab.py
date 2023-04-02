import handle.core.load as load
from handle.core.Crontab import Crontab as Crontab

""" 
    计划任务

    你可以在这里设置计划任务，计划任务的类型有两种，一种是cron，一种是interval
    cron类型的计划任务是基于时间的，interval类型的计划任务是基于时间间隔的

    对于interval你只能设置second，对于cron你可以设置day_of_week,month,day,hour,minute,second


    例如你要实现整点报时、每日新闻推送都可以使用计划任务来实现
"""


# 10秒执行一次
# Crontab.set('Controller','crontab',crontab_type='interval',second=10)