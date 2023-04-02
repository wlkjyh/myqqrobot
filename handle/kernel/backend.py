from flask import Flask,request
import handle.constant as constant
from handle.core.Log import Log as Log
import handle.running as running
from handle.kernel.request import request as requests
import handle.support.key as key
from handle.support.cq import cq as cq
from handle.kernel.handler import handler as handler
import time


class backend:
    def __init__(self):
        pass


    @staticmethod
    def startWithFlask(app):
        Log.info('Flask 后端服务已启动。')
        app.run(host=constant.LISTEN[0],port=constant.LISTEN[1],debug=False)

    def run(self,app):

        @app.route('/',methods=['GET','POST'])
        def index():
            

            """
                封装接收到的消息为实例
            """
            message = request.get_json()
            if message['post_type'] == 'message':

                instance = requests()

                if message['message_type'] == 'group':
                    instance.set_kv('type',key.MESSAGE_GROUP)
                    instance.set_kv('group_id',message['group_id'])
                    instance.set_kv('user_id',message['user_id'])
                else:
                    instance.set_kv('type',key.MESSAGE_PRIVATE)
                    instance.set_kv('group_id',None)
                    instance.set_kv('user_id',message['user_id'])

                # instance.set_kv('message',message['message'])
                instance.set_kv('message',cq().clearCQ(message['message']))
                instance.set_kv('source_message',message['message'])
                instance.set_kv('event_time',time.time())


                
                handler().next(instance=instance)

                pass



            return 'OK'




        backend.startWithFlask(app)
        


    
    
    
    
