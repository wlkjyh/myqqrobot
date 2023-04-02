import handle.running as running
import handle.constant as constant
from handle.core.Log import Log as Log
import json

class deny:
    
    def __init__(self):
        pass

    @staticmethod
    def group(group_id,write_file=False,remove=False):
        """设置群黑名单

        Args:
            group_id (int): 群号
            write_file (bool, optional): 是否将他保存到文件中，这样可以在程序重启的时候保留。 默认为False
            remove (bool, optional): 是否取消黑名单。 默认为False（添加黑名单）

        Returns:
            bool: 是否设置成功
        """        

        if remove:
            if group_id in running.deny_group:
                running.deny_group.remove(group_id)
            
            if write_file:
                try:
                    with open(constant.DENY_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if group_id in data['group']:
                            data['group'].remove(group_id)
                            with open(constant.DENY_FILE, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                Log.info('黑名单文件已更新。')

                except Exception as e:
                    Log.error(str(e))
                    return False
                
            
            return True
        else:
            if group_id not in running.deny_group:
                running.deny_group.append(group_id)
            
            if write_file:
                try:
                    with open(constant.DENY_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if group_id not in data['group']:
                            data['group'].append(group_id)
                            with open(constant.DENY_FILE, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                Log.info('黑名单文件已更新。')
                except Exception as e:
                    Log.error(str(e))
                    return False
                
            
            return True


    @staticmethod
    def user(user_id,write_file=False,remove=False):
        """设置用户黑名单

        Args:
            user_id (int): 用户QQ号
            write_file (bool, optional): 是否将他保存到文件中，这样可以在程序重启的时候保留。 默认为False
            remove (bool, optional): 是否取消黑名单。 默认为False（添加黑名单）

        Returns:
            bool: 是否设置成功
        """        
        if remove:
            if user_id in running.deny_user:
                running.deny_user.remove(user_id)
            
            if write_file:
                try:
                    with open(constant.DENY_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if user_id in data['user']:
                            data['user'].remove(user_id)
                            with open(constant.DENY_FILE, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                Log.info('黑名单文件已更新。')

                except Exception as e:
                    Log.error(str(e))
                    return False
                
            
            return True
        else:
            if user_id not in running.deny_user:
                running.deny_user.append(user_id)
            
            if write_file:
                try:
                    with open(constant.DENY_FILE, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if user_id not in data['user']:
                            data['user'].append(user_id)
                            with open(constant.DENY_FILE, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                Log.info('黑名单文件已更新。')

                except Exception as e:
                    Log.error(str(e))
                    return False
                
            
            return True


