from handle.core.Log import Log as Log
import handle.support.key as key
from handle.support.API import API as API

class Middleware:
    def __init__(self):
        pass



    
    @staticmethod
    def next(request):
        """将消息转发到下一个中间件或控制器

        Args:
            request (instance): 已经被中间件处理过的消息
        """        


        index = request.middleware_load_index
        middleware = request.middleware
        next_middleware = request.middleware_load_next

        if index == None or next_middleware == None:
            controller = request.controller
            action = request.action
            match = request.match


            try:
                # 有可能控制器返回多个值，将他全部获取出，在循环所有的返回值
                if len(match) == 0:
                    getreturn = getattr(controller, action)(request)
                else:
                    getreturn = getattr(controller, action)(request, *match)
                

                if getreturn != None:
                    send_type = request.type
                    if isinstance(getreturn, tuple):
                        if send_type == key.MESSAGE_GROUP:
                            for i in getreturn:
                                # 只能是字符串或者整数
                                if isinstance(i, str) or isinstance(i, int):
                                    API().send_group_msg(request.group_id, i)
                        elif send_type == key.MESSAGE_PRIVATE:
                            for i in getreturn:
                                if isinstance(i, str) or isinstance(i, int):
                                    API().send_private_msg(request.user_id, i)
                    else:
                        if send_type == key.MESSAGE_GROUP:
                            
                            if isinstance(getreturn, str) or isinstance(getreturn, int):
                                API().send_group_msg(request.group_id, getreturn)
                        elif send_type == key.MESSAGE_PRIVATE:
                            
                            if isinstance(getreturn, str) or isinstance(getreturn, int):
                                API().send_private_msg(request.user_id, getreturn)

                return True
            except Exception as e:
                Log.error('控制器“' + controller.__name__ + '”执行失败：' + str(e))
                # 获取错误位置
                print(e.__traceback__.tb_lineno)
                return False
                pass

            return True


        # 现在需要执行的中间件
        try:
            # request.middleware_load_index = index + 1
            # # print(len(middleware))
            # request.middleware_load_next = middleware[index + 1]

            # 判断是否是最后一个中间件，如果是就设置next和index为None
            if index + 1 == len(middleware):
                request.middleware_load_index = None
                request.middleware_load_next = None
            else:
                request.middleware_load_index = index + 1
                request.middleware_load_next = middleware[index + 1]



            next_middleware.handle_message(request)
            return True
        except Exception as e:
            Log.error('中间件“' + next_middleware.__name__ + '”执行失败：' + str(e))
            return False
            pass


        
        pass


    @staticmethod
    def ignore(request,noInfo=False):
        """丢弃这个消息不再处理，这个消息不会被转发到控制器或者下一个中间件

        Params:
            noInfo (bool): 是否不显示日志信息，默认为False，显示日志信息

        Args:
            request (instance): 已经被中间件处理过的消息
        """

        if noInfo == False:
            Log.info('消息“' + request.message + '”被中间件丢弃。')

        return False

        pass