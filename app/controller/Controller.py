from handle.support.Cache import Cache as Cache
from handle.support.API import API as API
from handle.support.cq import cq as cq
import handle.support.func as func
import handle.support.key as key


def menu(request):
    text = func.package_message([
        cq().at(request.user_id),
        '这是myQQRobot默认提供的菜单函数，该函数位于app\controller\Controller.py，你可以在这里编写你的菜单函数'
    ])

    if request.type == key.MESSAGE_PRIVATE:
        API().send_private_msg(request.user_id,text)
    else:
        API().send_group_msg(request.group_id,text)
