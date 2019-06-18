from flask import (Blueprint)
import logging

log = logging.getLogger('percheck.sub')

bp = Blueprint('hello', __name__,url_prefix='/')

@bp.route('/hello')
def hello():
    log.info('Hello Route')
    return 'Hello, World!'


