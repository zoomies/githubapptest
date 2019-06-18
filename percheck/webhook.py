from flask import Blueprint, request, abort
from app_auth import GitApp
import logging
import requests

log = logging.getLogger('percheck.sub')

bp = Blueprint('webhook', __name__)

gitapp = GitApp()

@bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        gitapp.set_request_payload(request)
        is_valid = gitapp.verify_webhook_signature(request)
        gitapp.auth_github_app()
        gitapp.auth_github_installation()

        if is_valid:
            log.info("Return 200")
            return '', 200
        else:
            log.info("Return 401")
            abort(401)


        

#    else:
#        abort(400)
#        log.info("Return 400")
        #This is not required since the route will detect on unsupported
        #method.  But I don't know all the possible edge cases and it 
        #doesn't hurt to leave this in, although I can't test it.


