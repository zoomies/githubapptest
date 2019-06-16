from flask import Blueprint, request, abort
from app_auth import GitApp
import logging

log = logging.getLogger('percheck.sub')

bp = Blueprint('webhook', __name__)

gitapp = GitApp()

@bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        gitapp.get_request_payload(request)
        return '', 200
    else:
        abort(400)
        #This is not required since the route will detect on unsupported
        #method.  But I don't know all the possible edge cases and it 
        #doesn't hurt to leave this in, although I can't test it.


