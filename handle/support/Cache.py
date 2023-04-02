import handle.running as running
import time
from handle.core.Log import Log as Log


""" 
    这个Cache是基于内存的，所以不适合存储大量数据，同时也不适合存储长期数据，在程序运行期间有效
"""
class Cache:

    def __init__(self):
        pass


    @staticmethod
    def set(key,value,expire=0):
        """设置缓存

        Args:
            key (str): 缓存键
            value (str): 缓存值
            expire (int, optional): 过期时间. Defaults to 0.

        Returns:
            bool: 返回True
        """        
        running.cache[key] = {
            'value':value,
            'expire':expire,
            'time':time.time()
        }

        return True
    

    @staticmethod
    def get(key):
        """获取缓存

        Args:
            key (str): 缓存键

        Returns:
            str: 返回缓存值
        """        
        if key not in running.cache:
            return None

        if running.cache[key]['expire'] != 0 and time.time() - running.cache[key]['time'] > running.cache[key]['expire']:
            return None

        return running.cache[key]['value']
    
    @staticmethod
    def delete(key):
        """删除缓存

        Args:
            key (str): 缓存键

        Returns:
            bool: 返回True
        """        
        if key not in running.cache:
            return True

        del running.cache[key]

        return True
    

    @staticmethod
    def flush():
        """清空缓存

        Returns:
            bool: 返回True
        """        
        running.cache = {}

        return True
    

    def daemon(self):
        while True:
            time.sleep(1)
            wait_del = []
            for key in running.cache:
                if running.cache[key]['expire'] != 0 and time.time() - running.cache[key]['time'] > running.cache[key]['expire']:
                    # del running.cache[key]
                    wait_del.append(key)


            for key in wait_del:
                Log.debug('删除缓存：' + key)
                del running.cache[key]