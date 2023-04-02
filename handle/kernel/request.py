
import handle.support.func as func
import re
import handle.constant as constant
import os
import handle.running as running

class request:


    def __init__(self):
        pass


    def set_kv(self,key,value):
        # self.key = value
        self.__dict__[key] = value

        return True

    def merge(self,dict={}):
        """向下一跳中间件或控制器传递消息

        Args:
            dict (dict): 传入一个字典，将字典中的键值对合并到消息中

        Returns:
            bool: 返回True
        """
        for key in dict:
            # self.key = dict[key]
            self.__dict__[key] = dict[key]

        return True
    
    def template(self,template_file,dicts={}):
        """使用模板

        Args:
            template (string): 模板的路径

        Returns:
            bool: 返回True
        """
        template_file = template_file.replace('.','\\')

        REAL_TEMPLATE_FILE = constant.TEMPLATE_PATH + '\\' + template_file
        if os.path.exists(REAL_TEMPLATE_FILE) == False:
            return '未找到模板文件：' + REAL_TEMPLATE_FILE
        
        try:
            temp = running.temp_conf.get_template(template_file)

            # 将字典渲染到模板中
            temp_out = temp.render(dicts)
            return temp_out

            pass
        except Exception as e:
            return '模板渲染失败：' + str(e)