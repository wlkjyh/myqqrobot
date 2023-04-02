from handle.core.Route import Route as Route
import handle.core.load as load



load.controller('Controller')

Route.any('^菜单$','Controller','menu')