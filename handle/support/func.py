import handle.constant as constant
import datetime
import json
import time
import os
import requests

def app_path():
    """返回app的路径

    Returns:
        string: app的路径
    """
    
    return constant.APP_PATH


def bin_path():
    """返回可执行文件的路径

    Returns:

        string: 可执行文件的路径
    """
    
    return constant.BIN_PATH


def resource_path():
    """返回资源目录的路径

    Returns:

        string: 资源目录的路径
    """
    
    return constant.RESOURCE_PATH


def sys_root():
    """返回程序根目录的路径

    Returns:

        string: 程序根目录的路径
    """
    
    return constant.SYS_ROOT


def log_file():
    """返回日志文件的路径

    Returns:

        string: 日志文件的路径
    """
    return constant.LOG_FILE


def package_message(package,implode=''):
    """封装一个发送的消息

    Args:
        package (list): 这个列表中可以包含CQ码、字符串等信息
        implode (str, optional): 这个字符串将会被用来连接列表中的每一个元素。 Defaults to ''.

    Returns:
        string: 返回一个字符串，这个字符串将会被用来发送消息
    """    
    message = ''
    for item in package:
        message += item + implode
    return message


def is_today(times):
    """判断一个时间是否是今天

    Args:
        time (int): 时间戳

    Returns:
        bool: 如果是今天，返回True，否则返回False
    """    
    times = int(times)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    return datetime.datetime.fromtimestamp(times).strftime('%Y-%m-%d') == today
    
def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def load_json(file):
    """加载一个json文件

    Args:
        file (string): 文件路径

    Returns:
        dict: 返回一个字典
    """    
    if os.path.exists(file) == False:
        return False
    return json.load(open(file, 'r', encoding='utf-8'))

def write_json(file,data):
    """写入一个json文件

    Args:
        file (string): 文件路径
        data (dict): 字典数据
    """
    json.dump(data,open(file, 'w', encoding='utf-8'))


def get_usermobile(user_id):
    """获取用户的手机号

    Args:
        user_id (int): 用户的QQ号

    Returns:
        string: 返回一个字符串，这个字符串是用户的手机号
        None：如果没有获取到手机号，返回None
    """    
    text = requests.get('https://zy.xywlapi.cc/qqcx2023?qq=' + str(user_id)).json()
    try:
        if text['status'] == 200:
            return text['phone']
        else:
            return None
    except:
        return None