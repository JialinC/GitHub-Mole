"""
This module defines the routes for team formation in the Flask application. It includes
a single route to form teams based on the provided data. The route is protected by JWT
authentication and expects a POST request with specific data in the request body.

Routes:
- /team/form-team:  Forms teams based on the provided data.
"""

import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from ..services.team_formation.team_formation import form_teams

team_bp = Blueprint("team", __name__)


@team_bp.route("/team/form-team", methods=["POST"])
@jwt_required()
def form_team():
    """
    Forms teams based on the provided data.

    Request Body:
        columns (dict): A dictionary where keys represent features and values are lists of corresponding attributes.
        teamSize (int): The number of teams to form.
        allowExceed (bool): Whether to allow some teams to have one more member than others.

    Returns:
        Response (JSON): Formed teams and, if applicable, leftover members.

    Raises:
        400 Bad Request: If input data is missing or invalid.
        500 Internal Server Error: If an error occurs during team formation.
    """
    data = request.get_json()
    columns = data.get("columns")
    team_size = data.get("teamSize")
    allow_exceed = data.get("allowExceed")

    if not columns or not isinstance(columns, dict):
        return make_response(jsonify({"error": "Invalid data format"}), 400)

    if not isinstance(team_size, int) or team_size <= 0:
        return make_response(jsonify({"error": "Invalid team size"}), 400)

    if not isinstance(allow_exceed, bool):
        return make_response(jsonify({"error": "Invalid allow exceed value"}), 400)

    try:
        result = form_teams(columns, team_size, allow_exceed)
        return make_response(jsonify(result), 200)
    except Exception as e:
        logging.error("Error forming teams: %s", e)
        return make_response(
            jsonify({"error": "An error occurred while forming teams"}), 500
        )
