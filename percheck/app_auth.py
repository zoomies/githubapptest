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
        log.info('Generating Bearer Token')
        private_pem = current_app.config['PRIVATE_KEY']
        private_pem_nl = private_pem.replace('\n',"\n")
        cert_bytes = private_pem.encode()
        private_key = default_backend().load_pem_private_key(cert_bytes, None)
        log.info(private_key)

#        private_key = serialization.load_pem_private_key(
#            private_pem.encode('utf-8'),
#            password = None,
#            backend = default_backend()
#        )


        #Generate JSON Web Token for GitHub Authentication
        #jwt_payload = {
        #    # issued at time
        #    iat: int(time.time()),
        #    # JWT expiration time (10 minute maximum)
        #    exp: int(time.time()) + (10 * 60),
        #    # GitHub App's identifier
        #    iss: current_app.config['GITHUB_APP_IDENTIFIER']
        #}
        
        jwt_dict ={}
        jwt_dict['iat']=int(time.time())
        jwt_dict['exp']=int(time.time()) + (10 * 60)
        jwt_dict['iss']=current_app.config['GITHUB_APP_IDENTIFIER']

        jwt_payload = json.dumps(jwt_dict)

        log.info(str(jwt_payload))

        rtn_token = jwt.encode(jwt_dict, private_pem, "RS256")

        log.info(rtn_token)

        return(rtn_token)
