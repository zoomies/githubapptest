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
        token = gitapp.get_bearer_token()

        log.info("Webook: " + token.decode())

        auth_headers = {"Authorization": "Bearer {}".format(token.decode()),
           "Accept": "application/vnd.github.machine-man-preview+json"}

        log.info(auth_headers)

        resp = requests.get('https://api.github.com/app', headers=auth_headers)

        log.info('Code: ' + str(resp.status_code))
        log.info('Content: ' + resp.content.decode())


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


