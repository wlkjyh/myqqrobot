
1、支持在控制器中使用return来发送消息
    如果你不想发送信息，你可以不返回任何信息或返回None
    如果你有返回，程序默认会为发送消息的群聊或个人发送消息

    小技巧：
        如果你想同时发多条消息，可以这样return
            return '消息1','消息2'

    

2、提供了几个新的工具函数
    - is_today （判断一个int时间戳是否是今天）
    - get_datetime （获取一个Y-m-d H:i:s格式的日期时间）
    - load_json （加载一个json文件）
    - write_json （写入一个json文件）

3、添加了模板的概念
    模板使用jinja2实现，所以模板是jinja2的一个超集

    你可以使用向控制器中传入的request实例中的template方法来使用模板。

    - 你可以这样使用

        def test(request)
            return request.template('code',{'name':'test'})