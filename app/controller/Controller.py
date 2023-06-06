from handle.support.Cache import Cache as Cache
from handle.support.API import API as API
from handle.support.cq import cq as cq
import handle.support.func as func
import handle.support.key as key
from handle.support.DB import DB as DB


def menu(request):
    text = func.package_message([
        cq().at(request.user_id),
        '这是myQQRobot默认提供的菜单函数，该函数位于app\controller\Controller.py，你可以在这里编写你的菜单函数'
    ])

    # if request.type == key.MESSAGE_PRIVATE:
    #     API().send_private_msg(request.user_id,text)
    # else:
    #     API().send_group_msg(request.group_id,text)

    if request.is_type('GROUP'):
        # 群聊消息
        pass

    # user_info = DB().table('user').where('qq',request.user_id).find()


    """ 
        你可以通过以下三种方式发送消息：

        1、request.send(消息内容)
        2.1（私聊消息）、API().send_private_msg(用户QQ,消息内容)
        2.2（群聊消息）、API().send_group_msg(群号,消息内容)
        3、return 消息内容

        其中，1和3是自动判断消息类型。
    """
    # request.send(text)

    # 如果返回布尔类型或者None，这里第3方法是不会发送消息的
    return True