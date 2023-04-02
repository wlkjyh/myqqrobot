from flask import Flask
from handle.kernel.backend import backend as backend
import logging


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


backend().run(app)
