import sys
from handle.helper import *

# 是否开启调试模式（开启DEBUG模式会在修改文件后自动重启程序） 
DEBUG = env('DEBUG',True)
# 系统根目录
SYS_ROOT = sys.path[0]
# 应用命名空间
APP_NAMESPACE = 'app'
# 控制器命名空间
APP_CONTROLLER_NAMESPACE = APP_NAMESPACE + '.controller'
# 中间件命名空间
APP_MIDDLEWARE_NAMESPACE = APP_NAMESPACE + '.middleware'
# 可执行文件文件夹
BIN_PATH = SYS_ROOT + '/bin/'
# 应用文件夹
APP_PATH = SYS_ROOT + '/' + APP_NAMESPACE + '/'
# 控制器文件夹
APP_CONTROLLER_PATH = APP_PATH + 'controller/'
# 中间件文件夹
APP_MIDDLEWARE_PATH = APP_PATH + 'middleware/'
# 资源文件夹
RESOURCE_PATH = SYS_ROOT + '/resource/'
# 日志文件
LOG_FILE = RESOURCE_PATH + '/log/runnning.log'
# 缓存目录
CACHE_PATH = RESOURCE_PATH + '/cache/'

# 加载外部的黑名单文件
DENY_FILE = RESOURCE_PATH + '/blackhole.json'
# 如果在程序启动的时候自动启动go-cqhttp，那么请将这个值设置为True
AUTO_START_GOCQ = False
GOCQ_FILE = BIN_PATH + 'gocqhttp.exe'

TEMPLATE_PATH = RESOURCE_PATH + '/template/'

# go-cqhttp的HTTP API地址
HTTP_API = env('HTTP_API','http://127.0.0.1:35351')
# 机器人框架监听信息
LISTEN = [
    '127.0.0.1',
    5701
]


DB_OPEN = env('DB_OPEN',False)
DB_HOST = env('DB_HOST','localhost')
DB_PORT = env('DB_PORT',3306)
DB_USERNAME = env('DB_USERNAME',None)
DB_PASSWORD = env('DB_PASSWORD',None)
DB_DATABASE = env('DB_DATABASE',None)