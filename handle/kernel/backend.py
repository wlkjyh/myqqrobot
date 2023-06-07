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
        app.run(host=constant.LISTEN[0],port=constant.LISTEN[1],debug=constant.DEBUG)

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
                
                instance.set_kv('nickname',message['sender']['nickname'])

                instance.set_kv('msg_type',key.MESSAGE_MESSAGE)
                instance.set_kv('self_id',message['self_id'])


                
                handler().next(instance=instance)

                pass

            # 等下需要实现的事件消息
            elif message['post_type'] == 'notice':
                # print(message)
                sub_type = message['notice_type']


                instance = requests()
                for k,v in message.items():
                    instance.set_kv(k,v)

                instance.set_kv('msg_type',key.MESSAGE_EVENT)
                instance.set_kv('type','event')
                instance.set_kv('event_time',time.time())
                instance.set_kv('message',sub_type)


                # print(instance.__dict__)

                handler().next(instance=instance)

            





            return 'OK'




        backend.startWithFlask(app)