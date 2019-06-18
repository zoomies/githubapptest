import hmac, hashlib, base64
import logging
import json
import time
import requests
from flask import current_app
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import jwt


log = logging.getLogger('percheck.sub')

class GitApp:

    def __init__(self):
        self.private_key =''
        self.github_app_id =''
        self.github_webhook_secret=''
        self.payload_raw=None
        self.payload=None

    def set_request_payload(self, request):
        self.payload_raw=request.get_data()
        self.payload=request.get_json()
        
    def verify_webhook_signature(self, request):
        
        incoming_sig_header = request.headers.get('X-Hub-Signature')

        if incoming_sig_header == None:
            log.error('No Github Webhook Signature')
            return None
        else:
            hash_type, incoming_sig = incoming_sig_header.split('=', 1)
            if hash_type != 'sha1':
                log.error('Unexpected hash type')
                return False
            else:
                # NOTE: The following hard codes the digest type into the call.  Some thought needs to
                # be put into whether this should allow any digest referenced by the header.  The
                # docs for Github specifically said SHA1 - so my thought is that any other should
                # not be allowed - at least for this test app.
                calculated_hmac = hmac.new(current_app.config['GITHUB_WEBHOOK_SECRET'].encode(), self.payload_raw, hashlib.sha1).hexdigest()
                log.info("Calculated HMAC: " + str(calculated_hmac))
                log.info("  Expected HMAC: " + incoming_sig)
                is_sig_verified = hmac.compare_digest(calculated_hmac, incoming_sig)
                log.info("Signature Match: " + str(is_sig_verified))
                return is_sig_verified

    def get_bearer_token(self):
        private_pem = current_app.config['PRIVATE_KEY']
        
        jwt_payload ={}
        jwt_payload['iat']=int(time.time())
        jwt_payload['exp']=int(time.time()) + (10 * 60)
        jwt_payload['iss']=current_app.config['GITHUB_APP_IDENTIFIER']

        rtn_token = jwt.encode(jwt_payload, private_pem, "RS256")

        return(rtn_token)

    def auth_github_app(self):

        token = self.get_bearer_token()

        auth_headers = {"Authorization": "Bearer {}".format(token.decode()), 
                        "Accept": "application/vnd.github.machine-man-preview+json"}

        resp = requests.get('https://api.github.com/app', headers=auth_headers)

        log.info('Code: ' + str(resp.status_code))
        log.info('Content: ' + resp.content.decode())

