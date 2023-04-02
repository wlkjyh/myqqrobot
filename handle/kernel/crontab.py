import route.crontab as crontab_config
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
import handle.running as running
from handle.core.Log import Log as Log
import os
def debug():
    print(1)
class crontab:


    def __init__(self):
        pass

    @staticmethod
    def call(controller,action):
        try:
            getattr(controller,action)()
        except Exception as e:
            Log.error('计划任务调度出错：' + str(e))
        pass

    @staticmethod
    def running():
        try:
            scheduler = BlockingScheduler()
            for task in running.crontab:
                controller = task['controller']
                action = task['action']
                

                if task['type'] == 'interval':
                    scheduler.add_job(crontab.call,'interval',seconds=task['second'],args=(controller,action))

                if task['type'] == 'cron':
                    scheduler.add_job(crontab.call,'cron',day_of_week=task['day_of_week'],month=task['month'],day=task['day'],hour=task['hour'],minute=task['minute'],second=task['second'],args=(controller,action))


            
            Log.info('计划任务守护进程已启动。')
            scheduler.start()
        except Exception as e:
            Log.error('计划任务启动失败：' + str(e))
            Log.error('程序停止运行。')
            os._exit(0)


    def start(self):
        t = threading.Thread(target=self.running)
        t.setDaemon(True)
        t.start()
        pass