from handle.core.Route import Route as Route
import handle.core.load as load



""" 
    服务提供者实例路由文件
    注意：服务提供者加载控制器切记不要和框架的控制器重名，否则会导致服务提供者无法加载
    如果有重名，建议在加载控制器或者中间件时候设置别名
"""
load.controller('Controller',alias='test_controller')

Route.any('^服务提供者$', 'test_controller','menu')
