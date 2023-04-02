"""
    生成CQ码
"""
import re
import os

class cq:
    def __init(self):
        pass


    def clearCQ(self,text):
        # 将at的cq码换成qq
        reg = re.compile(r'\[CQ:at,qq=(.*?)\]')
        text = reg.sub(r'\1',text)

        reg = re.compile(r'\[CQ:.*?\]')
        return reg.sub('',text)
    
    
    def at(self,qq):
        if qq == 'all':
            cqcode = '[CQ:at,qq=all]'
            return cqcode

        cqcode = '[CQ:at,qq=' + str(qq) + ']'
        return cqcode

    def face(self,id):
        if id > 221:
            id = 221
        if id < 0:
            id = 0

        cqcode = '[CQ:face,id=' + str(id) + ']'
        return cqcode
    
    def video(self,file):
        cqcode = '[CQ:video,file='+self.file(file)+']'
        return cqcode

    def text_to_voice(self,text):
        cqcode = '[CQ:tts,text='+text+']'
        return cqcode


    """
        一种xml的图片消息（装逼大图）
    """
    def cardimage(self,file,min_width=400,min_height=400,max_width=400,max_height=400):
        cqcode = '[CQ:cardimage,file='+self.file(file)+',min_width='+str(min_width)+',min_height='+str(min_height)+',max_width='+str(max_width)+',max_height='+str(max_height)+']'
        return cqcode

    """
        json消息
    """
    def json_message(self,json):
        # json中的字符需要转义
        json = json.replace(',','&#44;').replace('&','&amp;').replace('[','&#91;').replace(']','&#93;')
        cqcode = '[CQ:json,data='+json+']'
        return cqcode

    """
        xml消息
    """
    def xml_message(self,xml):
        cqcode = '[CQ:xml,data='+xml+']'
        return cqcode


    """
        戳一戳
    """
    def poke(self,qq):
        cqcode = '[CQ:poke,qq='+str(qq)+']'
        return cqcode
    
    """
        礼物
    """
    def gift(self,qq,gift_id):
        if gift_id > 13:
            gift_id = 13
        if gift_id < 1:
            gift_id = 1
        cqcode = '[CQ:gift,qq='+str(qq)+',id='+str(gift_id)+']'
        return cqcode

    """
        图片

        type: show是普通图片，flash是闪照
    """
    def image(self,file,type='show'):
        if type != 'show' and type != 'flash':
            type = 'show'

        cqcode = '[CQ:image,file='+self.file(file)+',type='+type+']'
        return cqcode

    """
        链接分享
    """
    def share(self,url,title,content=None,image=None):
        other = ''
        if content != None:
            other += ',content='+content
        if image != None:
            other += ',image='+image

        cqcode = '[CQ:share,url='+url+',title='+title+ other +']'
        return cqcode

    """
        语音
    """
    def record(self,file):
        return '[CQ:record,file='+self.file(file)+']'

    """
        如果是本地文件就用file，如果是网络文件就用url
    """
    def file(self,file):
        if 'http' in file:
            return file
        else:
            return 'file:///'+os.path.abspath(file)

