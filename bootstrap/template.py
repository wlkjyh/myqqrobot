import jinja2
import handle.running as running
import handle.constant as constant
from handle.core.Log import Log as Log


running.temp_conf = jinja2.Environment(loader=jinja2.FileSystemLoader(constant.TEMPLATE_PATH))
Log.info('模板引擎加载完成')
