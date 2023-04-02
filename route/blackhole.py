from handle.core.deny import deny as deny
import handle.core.load as load
import handle.constant as constant


"""
    可以使用json文件的形式来加载黑名单，这样有助于你在程序运行的时候动态的添加黑名单
"""
load.deny(constant.DENY_FILE)


"""
    拒绝对某群或者某人的响应，这个方法支持在任何地方调用，只不过在这里调用的话，会在程序启动的时候执行


    如果remove为True，那么就是取消黑名单
"""


deny.group(group_id=12345678,remove=False)
deny.user(user_id=10001,remove=False)