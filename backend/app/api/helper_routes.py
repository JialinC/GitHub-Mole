import requests
from flask import Blueprint, jsonify, current_app, request, redirect
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
)
from backend.app.database import db
from backend.app.models.user import User
import logging

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
        raise ValidationError(
            f"Invalid personal access token or enterprise API URL: {str(e)}"
        )
    return response.json()


def update_or_create_user(github_id, pat, api_url):
    user = User.query.filter_by(github_id=github_id).first()
    if user:
        user.personal_access_token = pat
        db.session.commit()
        return "Access token updated successfully"
    else:
        new_user = User(github_id=github_id, personal_access_token=pat, api_url=api_url)
        db.session.add(new_user)
        db.session.commit()
        return "New user created successfully"


@helper_bp.route("/helper/validate-pat", methods=["POST"])
def validate_pat():
    pat = request.json.get("pat")
    account_type = request.json.get("accountType")
    api_url = request.json.get("apiUrl")
    user_api_url = api_url + "/user"
    logging.info(f"Validating PAT for account type: {account_type}, API URL: {api_url}")

    try:
        user_data = validate_pat_and_api_url(pat, user_api_url)
        github_id = user_data["id"]
        update_or_create_user(github_id, pat, api_url)
        access_token = create_access_token(identity=github_id)
        return redirect(
            f"{current_app.config['FRONTEND_URL']}/dashboard?token={access_token}"
        )
    except ValidationError as e:
        logging.error(f"Validation error: {str(e)}")
        return jsonify({"valid": False, "error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
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
    print(github_id, pat, api_url)

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
