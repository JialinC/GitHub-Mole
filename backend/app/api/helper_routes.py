import logging
import requests
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from app.models import User, UserQuery


helper_bp = Blueprint("helper", __name__)


@helper_bp.route("/helper/sso", methods=["GET"])
def sso():
    config_value = current_app.config.get("GITHUB_CLIENT_ID")
    sso_config = False
    if config_value is not None and config_value != "":
        sso_config = True
    return jsonify({"sso_config": sso_config})


class ValidationError(Exception):
    pass


def validate_pat_and_api_url(pat, api_url):
    headers = {"Authorization": f"token {pat}"}
    try:
        response = requests.get(api_url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValidationError(str(e))
    return response.json()


def update_or_create_user(github_id, github_login, pat, api_url):
    user = User.query.filter_by(github_login=github_login).first()
    if user:
        user.update(personal_access_token=pat)
        return "Access token updated successfully"
    else:
        User.create(
            github_id=github_id,
            github_login=github_login,
            personal_access_token=pat,
            api_url=api_url,
        )
        return "New user created successfully"


@helper_bp.route("/helper/validate-pat", methods=["POST"])
def validate_pat():
    data = request.json
    pat = data.get("pat")
    account_type = data.get("accountType")
    api_url = data.get("apiUrl")
    user_api_url = api_url + "/user"
    logging.info(
        "Validating PAT for account type: %s, API URL: %s", account_type, api_url
    )

    try:
        user_data = validate_pat_and_api_url(pat, user_api_url)
        github_login = user_data["login"]
        github_id = str(user_data["node_id"])
        update_or_create_user(github_id, github_login, pat, api_url)
        access_token = create_access_token(identity=github_id)
        refresh_token = create_refresh_token(identity=github_id)
        return (
            jsonify(
                {
                    "valid": True,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            ),
            200,
        )
    except ValidationError as e:
        logging.error("Validation error: %s", str(e))
        return jsonify({"valid": False, "error": str(e)}), 400
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        return jsonify({"valid": False, "error": "An unexpected error occurred"}), 500


@helper_bp.route("/helper/user-info", methods=["GET"])
@jwt_required()
def user_info():
    # Get the user ID from the JWT
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    if not user:
        logging.error(f"User with GitHub ID {github_id} not found")
        return jsonify({"msg": "User not found"}), 404
    pat = user.personal_access_token
    api_url = user.api_url

    user_api_url = api_url + "/user"
    try:
        user_data = validate_pat_and_api_url(pat, user_api_url)
        return jsonify(user_data)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"valid": False, "error": "An unexpected error occurred"}), 500


@helper_bp.route("/helper/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@helper_bp.route("/helper/check-duplicate", methods=["GET"])
@jwt_required()
def check_duplicate():
    name = request.args.get("name")
    dstype = request.args.get("type")
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    existing_dataset = UserQuery.query.filter_by(
        ds_name=name, user_login=user.github_login, data_type=dstype
    ).first()
    if existing_dataset:
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200
