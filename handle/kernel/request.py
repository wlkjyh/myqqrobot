
import handle.support.func as func
import re
import handle.constant as constant
import os
import handle.running as running
import handle.support.key as key
from handle.support.API import API as API



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
        
    def send(self,text):
        """发送消息

        Args:
            text (str): 消息内容
        """
        send_type = self.type

        if send_type == key.MESSAGE_GROUP:
                            
            if isinstance(text, str) or isinstance(text, int):
                API().send_group_msg(self.group_id, text)
        elif send_type == key.MESSAGE_PRIVATE:
                            
            if isinstance(text, str) or isinstance(text, int):
                API().send_private_msg(self.user_id, text)

    def is_type(self,typename):
        """判断消息类型

        Args:
            typename (string): 消息类型

        Returns:
            bool: 返回True或False
        """
        typename = typename.upper()
        if typename == 'GROUP':
            typename = key.MESSAGE_GROUP
        elif typename == 'PRIVATE':
            typename = key.MESSAGE_PRIVATE

        if self.type == typename:
            return True
        else:
            return False