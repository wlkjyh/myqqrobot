# myQQbot

## 环境要求
建议使用conda虚拟环境，python版本>=``3.8``，go-cqhttp latest

## 如何安装
```
pip install -r requirement.txt
```
### 更新信息
- 2023-04-07
    
    1、加入了服务提供者等功能
    2、更新了相关提示信息

## 基本用法
### 消息路由
你需要在``route/register.py``中注册一个消息路由
例如：

```py
Route.group('^菜单$','Controller','menu')
```

消息路由分为三种，分别为``group``、``private``、``any``分别代表``群聊``、``私聊``、``任意``

值得注意的是，你传入的控制器必须使用``handle.core.load``模块进行注册

例如：

```py
import handle.core.load as load
load.controller('Controller',alias=None)
```

上述代码注册了``Controller``控制器，提示：load模块对注册``controller``、``middleware``支持设置别名。例如

```py
load.controller('Controller','Ctrl')
Route.group('^菜单$','Ctrl','menu')
```

注册的消息，采用正在表达式来进行匹配，所以匹配参数必须是一个合法的正则表达式。

同时，在注册消息路由时候，支持配置中间件，匹配别名等。

例如：

```py
load.middleware('default')
Route.group('^<test> (.*?)$','Controller','test',middleware=['default'],alias={
    'test' : '测试|debug'
})
```
上述代码加载了```default```中间件，并在消息路由中进行了应用。同时为test设置了别名，注意：设置别名的字段，必须使用``<>``进行包裹。那么上述代码使用``test 1``、``debug 1``、``测试 1``均能够被匹配到

### 黑名单（blackhole）
黑名单，顾名思义就是拒绝上某人或某群拒绝服务，它基本原理是通过全局中间件实现的，如果你不希望使用该功能，可以在``app/kernel.py``文件中删除``blackhole``的注册


配置黑名单其实非常简单，你可以在控制器或者``route/blackhole.py``中配置黑名单。不同的是，在``route/blackhole.py``中配置的黑名单会随着程序启动而作用。

配置黑名单，可以通过``handle.core.deny``模块中的``deny``类来进行配置。（以下所有的操作都是在``route/blackhole.py``中完成的


- 配置10001为QQ黑名单
    ```py
    deny.user(user_id=10001)
    ```
- 配置123456为群黑名单
    ```py
    deny.group(group_id=123456)
    ```
- 将QQ：10001和群：123456移除黑名单
    ```py
    deny.user(user_id=10001,remove=True)
    deny.group(group_id=123456,remove=True)
    ```
-  基于文件来加载黑名单
    
    这里我们需要用到load模块中的blackhole方法

    ```py
    load.blackhole('resource/blackhole.json')
    ```

    在```resource/blackhole.json```文件中基本格式如下

    ```json
    {
        "user":[],
        "group":[]
    }
    ```
- 将黑名单信息保存到文件
    ```py
    deny.user(user_id=10001,write_file=True)
    deny.user(user_id=10001,write_file=True,remove=True)
    deny.group(group_id=123456,write_file=True)
    deny.group(group_id=123456,write_file=True,remove=True)
    ```

### 中间件

使用中间件，需要在```app/middleware```目录中进行实现

基本格式如下

```py
from handle.support.middleware import Middleware as Middleware
def handle_message(request):

    return Middleware.next(request)
```

在上述代码中，有一个``Middleware``类，里面提供了``next``和``ignore``方法，``next``方法可以将该消息传递给下一个中间件或者控制器，而``ignore``方法可以忽略这个请求

上述代码中，有一个``request``参数，是消息的实例，你可以使用``print(request)``来查看具体的细节


如果你这个中间件希望让所有的消息作用，你需要在``app/kernel.py``中，在middleware属性中加入你这个中间件，并且使用``load.middleware``方法来加载这个中间件

中间件支持路由级别的、分类级别的，路由级别的已经在上文中讲述过了。

分类级别的，将中间件分为了``group``和``private``类，分别代表了群聊消息和私聊消息，意味着只会在群聊消息或者私聊消息中进行加载，你需要在``app/kernel.py``middlewareGroups``load.middleware``方法来加载这个中间件


### 控制器
控制器概念和其他框架概念相同，值得注意的是，你需要在``app/controller``目录下进行实现。

### 控制器方法

实现控制器方法，基本格式如下

```py
def test(request):

    return 'OK'
```

必须包含一个request参数来接受消息实例
你可以选择不return，如果选择了return，那么默认会向发送消息的人或者发送消息的群来发送你return的内容

对于参数来说，如果你在正则表达式中使用的``(.*)``、``(\d+)``等可以匹配出内容的正则表达式，你需要创建额外的参数

例如:

```py
# 路由部分
Route.any('^ping (.*)$','Controller','ping')

# 控制器方法部分
def ping(request,domain):


    return '你正在ping：' + str(domain)
```



如果你希望同时发送多条消息，你可以返回一个元组

例如：
```py
def test(request):

    return '消息1','消息2','消息3'
```

同时你也可以使用``模板``进行返回

模板采用jinja2实现的，所以myQQBot的模板实际上是jinja2的一个超集

使用模板前，你需要在``resource/template``中定义一个模板，模板是没有任何扩展名的。

例如：
```python
#模板：code

你好：{{ name }}

# 控制器方法

def test(request):

    return request.template('code',{
        'name' : 'wlkjyy'
    })

```

上述示例发送出的内容为``你好：wlkjyy``


### API模块
在API模块中我们实现了许多的QQ操作，你需要自己阅读。


### 服务提供者
服务提供者类似于其他框架中所说的```插件```，你可以在```provider```目录中创建一个子目录实现服务提供者。


基本要求：
- 必须包含info.py文件
```python
# 服务名称
SERVICE_NAME = 'test'
# 服务版本
SERVICE_VERSION = '1.0.0'
# 服务描述
SERVICE_DESCRIPTION = '这是一个测试服务提供者，服务提供者可以加载其他开发者编写的控制器和中间件，以用来扩展框架的功能'
# 服务提供者
SERVICE_PROVIDER = 'MyCQBot'
# 服务提供者网址
SERVICE_PROVIDER_URL = 'http://example.com'
# 服务提供者邮箱
SERVICE_PROVIDER_EMAIL = 'mail@example.com'
```
- 必须包含route.py文件
```py
from handle.core.Route import Route as Route
import handle.core.load as load
""" 
    服务提供者实例路由文件
    注意：服务提供者加载控制器切记不要和框架的控制器重名，否则会导致服务提供者无法加载
    如果有重名，建议在加载控制器或者中间件时候设置别名
"""
load.controller('Controller',alias='test_controller')

Route.any('^服务提供者$', 'test_controller','menu')

```


总的来说，开发服务提供者和直接在框架中开发是相同的，你只是需要配置route.py和info.py文件。

值得注意的是，加载控制器和中间件，名称不能和框架中开发的名称相同，如果存在相同，建议设置alias别名。

如果你的控制器和中间件实现在子目录，请使用``.``来代替``\``，并且必须设置别名，注意：框架中开发不支持该写法。

例如我的控制器在provider\\test\\controller\\Test.py
那么代码应该这样写
```py
load.controller('controller.Test',alias='Test')
```

其他开发流程和框架中开发是相同的。
