from flask import (Blueprint)

bp = Blueprint('install', __name__,url_prefix='/')

@bp.route('/install')
def install():
    return 'Thank you for installing P2 DF Test'


