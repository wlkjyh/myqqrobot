from handle.support.middleware import Middleware as Middleware

"""
    这是一个例子中间件，用于对包含指定关键词的消息进行忽略，这个消息不会被转发到控制器
"""

def handle_message(request):


    message = request.message


    noise = [
        'SB','NMSL'
    ]

    for noise_word in noise:
        if noise_word in message:
            return Middleware.ignore(request)
        

    request.merge({
        'msg' : 'test'
    })

    return Middleware.next(request)