from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import User


def id_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        user_id = None

        if 'x-access-id' in request.headers:
            user_id = request.headers['x-access-id'].split(' ')[1]
        if not user_id:
            return jsonify({'message': 'ID is missing.'}), 401
        
        try:
            current_user_id = User.query.filter_by(user_id = user_id).first()
            print(user_id)
            print(current_user_id)
        except:
            owner = User.query.filter_by(user_id = user_id).first()
            print("error")

            if user_id != owner.user_id and secrets.compare_digest(user_id, owner.user_id):
                return jsonify({'message': 'Token is invalid'})
        print(current_user_id)
        return our_flask_function(current_user_id, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)