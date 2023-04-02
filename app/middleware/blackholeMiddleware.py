from handle.support.middleware import Middleware as Middleware
import handle.support.key as key
import handle.running as running
from handle.support.cq import cq as cq
import handle.support.func as func


def handle_message(request):
    group_id = request.group_id
    user_id = request.user_id

    if user_id != None:
        if user_id in running.deny_user:
            return Middleware.ignore(request,noInfo=True)
        
    if group_id != None:
        if group_id in running.deny_group:
            return Middleware.ignore(request,noInfo=True)
    
    return Middleware.next(request)
