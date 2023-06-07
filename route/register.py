from handle.core.Route import Route as Route
import handle.core.load as load
import handle.support.event as Event


load.controller('Controller')

Route.any('^<helper>$','Controller','menu',alias={
    'helper' : '菜单|帮助|help|menu'
})


# 群文件上传
Route.event(Event.GROUP_UPLOAD,'Controller','upload_file')