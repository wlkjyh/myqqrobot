import handle.constant as constant
import datetime


class Log:
    def __init__(self):
        pass

    @staticmethod
    def getdatetime():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def info(message):
        info = '[INFO] [' + Log.getdatetime() + '] ' + message
        print(info)
        with open(constant.LOG_FILE , 'a',encoding='utf-8') as f:
            f.write(info + '\n')
            

    @staticmethod
    def error(message):
        info = '[ERROR] [' + Log.getdatetime() + '] ' + message
        print(info)
        with open(constant.LOG_FILE , 'a',encoding='utf-8') as f:
            f.write(info + '\n')
            

    @staticmethod
    def debug(message):
        info = '[DEBUG] [' + Log.getdatetime() + '] ' + message
        print(info)
        with open(constant.LOG_FILE , 'a',encoding='utf-8') as f:
            f.write(info + '\n')
            

    @staticmethod
    def warning(message):
        info = '[WARNING] [' + Log.getdatetime() + '] ' + message
        print(info)
        with open(constant.LOG_FILE , 'a',encoding='utf-8') as f:
            f.write(info + '\n')
            

    @staticmethod
    def critical(message):
        info = '[CRITICAL] [' + Log.getdatetime() + '] ' + message
        print(info)
        with open(constant.LOG_FILE , 'a',encoding='utf-8') as f:
            f.write(info + '\n')
            
    

    