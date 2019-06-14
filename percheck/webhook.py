from flask import Blueprint, request, abort

bp = Blueprint('webhook', __name__)

@bp.route('/webhook', methods=['POST'])
def webhook():
    print(request.method)
    if request.method == 'POST':
        print(request.json)
        return '', 200
    else:
        abort(400)
        #This is not required since the route will detect on unsupported
        #method.  But I don't know all the possible edge cases and it 
        #doesn't hurt to leave this in, although I can't test it.


