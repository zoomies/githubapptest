import hmac, hashlib, base64
import logging
import json
from flask import current_app

log = logging.getLogger('percheck.sub')

class GitApp:

    def __init__(self):
        self.private_key =''
        self.github_app_id =''
        self.github_webhook_secret=''
        self.payload_raw=None
        self.payload=None

    def set_request_payload(self, request):
        #log.info("Loading payload into instance variables")
        self.payload_raw=request.get_data()
        self.payload=request.get_json()
        #log.info(str(self.payload))

    def verify_webhook_signature(self, request):
        incoming_sig_header = request.headers.get('HTTP_X_HUB_SIGNATURE')

        if incoming_sig_header == None:
            log.error('No Github Webhook Signature')
            return None
        else:
            hash_type, incoming_sig = incoming_sig_header.split('=', 1)
            if hash_type != 'sha1':
                log.info('Unexpected hash type')
                return False
            else:
                # NOTE: The following hard codes the digest type into the call.  Some thought needs to
                # be put into whether this should allow any digest referenced by the header.  The
                # docs for Github specifically said SHA1 - so my thought is that any other should
                # not be allowed - at least for this test app.
                calculated_hmac = hmac.new(current_app.config['GITHUB_WEBHOOK_SECRET'].encode('ascii'), self.payload_raw, hashlib.sha1).digest()
                hex_digest = base64.encodebytes(calculated_hmac).strip()
                log.info("Calculated HMAC: " + hex_digest.hex())
                log.info("  Expected HMAC: " + incoming_sig)
                is_sig_verified = hmac.compare_digest(hex_digest.hex(), incoming_sig)
                log.info("Signature Match: " + str(is_sig_verified))
                return is_sig_verified


