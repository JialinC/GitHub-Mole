from flask import Blueprint, jsonify, request
# Import service methods
from backend.app.services.github_graphql_services import get_current_user_login, get_specific_user_login

github_bp = Blueprint('api', __name__)

@github_bp.route('/graphql/current-user-login', methods=['GET'])
def current_user_login():
    data = get_current_user_login()
    return jsonify(data)

@github_bp.route('/graphql/user-login/<username>', methods=['GET'])
def specific_user_login(username):
    data = get_specific_user_login(username)
    return jsonify(data)
