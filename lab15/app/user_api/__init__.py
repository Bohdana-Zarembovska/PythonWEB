from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from .views import UserApi, UsersApi

user_api_bp = Blueprint('user_api', __name__)
api = Api(user_api_bp)

api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/users/<int:id>')

@user_api_bp.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400  