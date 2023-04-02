import requests
import handle.constant as constant


class API:
    def __init__(self):
        self.server = constant.HTTP_API + '/'

    def send_group_msg(self, group_id, message):
        data = {
            "group_id": group_id,
            "message": message
        }
        r = requests.post(self.server + 'send_group_msg', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        如果group_id为群号，则发送群临时消息
    """
    def send_private_msg(self, user_id, message,group_id=None):
        data = {
            "user_id": user_id,
            "message": message
        }
        if group_id:
            data['group_id'] = group_id
        r = requests.post(self.server + 'send_private_msg', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False


    """
        撤回消息
    """
    def delete_message(self,message_id):
        data = {
            "message_id": message_id
        }
        r = requests.post(self.server + 'delete_msg', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        踢人
        如果reject_add_request为True，那么在被踢的用户加群时，会被拒绝
    """
    def set_group_kick(self,group_id, user_id, reject_add_request=False):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        }
        r = requests.post(self.server + 'set_group_kick', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    
    """
        处理加好友请求
        如果approve为True，那么将会同意好友请求，否则拒绝
    """
    def set_friend_add_request(self,flag, approve=True, remark=''):
        data = {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }
        r = requests.post(self.server + 'set_friend_add_request', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        处理加群/邀请请求
        如果approve为True，那么将会同意请求，否则拒绝
        reason为拒绝理由
    """
    def set_group_add_request(self,flag, sub_type, approve=True, reason=''):
        data = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": lambda x: 'true' if x else 'false',
            "reason": reason
        }
        r = requests.post(self.server + 'set_group_add_request', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """

        获取好友列表
    """

    def get_friend_list(self):
        r = requests.post(self.server + 'get_friend_list').json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        获取单向好友
    """
    def get_unidirectional_friend_list(self):
        r = requests.post(self.server + 'get_unidirectional_friend_list').json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        检测链接安全性

        返回int  1: 安全 2: 未知 3: 危险
    """
    def check_url_safely(self,url) -> int:
        data = {
            "url": url
        }
        r = requests.post(self.server + 'check_url_safely', data=data).json()
        if r['retcode'] == 0:
            return r['data']['level']
        else:
            return False

    """
        获取精华消息

        group_id: 群号
    """
    def get_essence_msg_list(self,group_id):
        data = {
            "group_id": group_id
        }
        r = requests.post(self.server + 'get_essence_msg_list', data=data).json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        移除精华消息
        message_id: 消息id
    """
    def delete_essence_msg(self,message_id):
        data = {
            "message_id": message_id
        }
        r = requests.post(self.server + 'delete_essence_msg', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        设置精华消息
        message_id: 消息id
    """
    def set_essence_msg(self,message_id):
        data = {
            "message_id": message_id
        }
        r = requests.post(self.server + 'set_essence_msg', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False
        

    """
        发送群公告
        group_id: 群号
        content: 内容

        需要管理员或者群主
    """
    def send_group_notice(self,group_id, content):
        data = {
            "group_id": group_id,
            "content": content
        }
        r = requests.post(self.server + '_send_group_notice', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        获取群 @全体成员 剩余次数
    """
    def get_group_at_all_remain(self,group_id):
        data = {
            "group_id": group_id
        }
        r = requests.post(self.server + 'get_group_at_all_remain', data=data).json()
        if r['retcode'] == 0:
            if r['data']['can_at_all']:
                return r['data']['remain_at_all_count_for_uin']
            else:
                return False
        else:
            return False

    """

        @全体成员

    """
    def cq_at_all(self):
        return '[CQ:at,qq=all]'

    """
        删除群文件

    """
    def delete_group_file(self,group_id, file_id,busid):
        data = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        }
        r = requests.post(self.server + 'delete_group_file', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        上传群文件
    """
    def upload_group_file(self,group_id, file, name):
        data = {
            "group_id": group_id,
            "file": file,
            "name": name,   
        }
        r = requests.post(self.server + 'upload_group_file', data=data).json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        设置群头像
    """
    def set_group_portrait(self,group_id, file):
        data = {
            "group_id": group_id,
            "file": file
        }
        r = requests.post(self.server + 'set_group_portrait', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False
            
    """
        清理缓存
    """
    def clean_cache(self):
        r = requests.post(self.server + 'clean_cache').json()
        return True

    """
        获取群成员
    """
    def get_group_member_list(self,group_id):
        data = {
            "group_id": group_id
        }
        r = requests.post(self.server + 'get_group_member_list', data=data).json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        获取群成员信息
    """
    def get_group_member_info(self,group_id, user_id):
        data = {
            "group_id": group_id,
            "user_id": user_id
        }
        r = requests.post(self.server + 'get_group_member_info', data=data).json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False

    """
        删除好友
    """
    def delete_friend(self,user_id):
        data = {
            "user_id": user_id
        }
        r = requests.post(self.server + 'delete_friend', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        群打卡
    """
    def send_group_sign(self,group_id):
        data = {
            "group_id": group_id
        }
        r = requests.post(self.server + 'send_group_sign', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        设置头衔
    """
    def set_group_special_title(self,group_id, user_id, special_title, duration='-1'):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        }
        r = requests.post(self.server + 'set_group_special_title', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        退出群聊

        当is_dismiss为True时，退出并解散该群（需群主权限）
    """
    def set_group_leave(self,group_id,is_dismiss=False):
        data = {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }
        r = requests.post(self.server + 'set_group_leave', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        设置单人禁言

        如果duration为0，则取消禁言
    """
    def set_group_ban(self,group_id, user_id, duration):
        data = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        }
        r = requests.post(self.server + 'set_group_ban', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        开启全体禁言
        如果enable为False，则取消全体禁言
    """
    def set_group_whole_ban(self,group_id, enable=True):
        data = {
            "group_id": group_id,
            "enable": enable
        }
        r = requests.post(self.server + 'set_group_whole_ban', data=data).json()
        if r['retcode'] == 0:
            return True
        else:
            return False

    """
        获取用户信息
    """
    def get_stranger_info(self,user_id):
        data = {
            "user_id": user_id
        }
        r = requests.post(self.server + 'get_stranger_info', data=data).json()
        if r['retcode'] == 0:
            return r['data']
        else:
            return False