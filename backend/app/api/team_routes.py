"""This file defines the URLs for various GraphQL endpoints."""

# from k_means_constrained import KMeansConstrained
# import numpy as np
import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required

# import random
from ..services.team_formation.team_formation import form_teams

team_bp = Blueprint("team", __name__)


@team_bp.route("/team/form-team", methods=["POST"])
@jwt_required()
def form_team():
    """
    Form teams based on the provided data.

    Returns:
        JSON response with the formed teams and optionally left over members.
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


# def label_to_type(label: int) -> str:
#     """Convert a numeric label to a human-readable type."""
#     return f"Type {label + 1}"


# def normalize_data(columns: dict) -> np.ndarray:
#     """Normalize the numerical data."""
#     keys = list(columns.keys())
#     numerical_data = np.array([columns[key] for key in keys[1:]], dtype=float).T
#     means = np.mean(numerical_data, axis=0)
#     std_devs = np.std(numerical_data, axis=0)
#     return (numerical_data - means) / std_devs


# def create_clusters(identifiers: list, labels: np.ndarray, team_size: int) -> list:
#     """Create clusters from the labels."""
#     clusters = [[] for _ in range(team_size)]
#     for identifier, label in zip(identifiers, labels):
#         human_readable_label = label_to_type(label)
#         clusters[label].append([identifier, human_readable_label])
#     for cluster in clusters:
#         random.shuffle(cluster)
#     return clusters


# @team_bp.route("/team/form-team", methods=["POST"])
# @jwt_required()
# def form_team():
#     """
#     Form teams based on the provided data.

#     Returns:
#         JSON response with the formed teams and optionally left over members.
#     """
#     data = request.get_json()
#     columns = data.get("columns")
#     team_size = data.get("teamSize")
#     allow_exceed = data.get("allowExceed")

#     if not columns or not isinstance(columns, dict):
#         return make_response(jsonify({"error": "Invalid data format"}), 400)

#     if not isinstance(team_size, int) or team_size <= 0:
#         return make_response(jsonify({"error": "Invalid team size"}), 400)

#     if not isinstance(allow_exceed, bool):
#         return make_response(jsonify({"error": "Invalid allow exceed value"}), 400)

#     try:
#         identifiers = columns[list(columns.keys())[0]]
#         normalized_data = normalize_data(columns)
#         size_min = len(normalized_data) // team_size
#         size_max = size_min + 1 if len(normalized_data) % team_size > 0 else size_min

#         kmeans = KMeansConstrained(
#             n_clusters=team_size,
#             size_min=size_min,
#             size_max=size_max,
#             random_state=0,
#         )
#         kmeans.fit(normalized_data)
#         labels = kmeans.labels_

#         clusters = create_clusters(identifiers, labels, team_size)
#         teams = {}
#         left_over = []
#         for i in range(size_min):
#             team_key = f"Team {i + 1}"
#             teams[team_key] = []
#             for j in range(team_size):
#                 teams[team_key].append(
#                     {"id": clusters[j][i][0], "type": clusters[j][i][1]}
#                 )
#         over_size_team = len(normalized_data) % team_size
#         if over_size_team > 0:
#             for c in clusters:
#                 if len(c) > size_min:
#                     if allow_exceed:
#                         team_key = f"Team {over_size_team + 1}"
#                         teams[team_key].append(
#                             {"id": c[size_min][0], "type": c[size_min][1]}
#                         )
#                         over_size_team -= 1
#                     else:
#                         left_over.append({"id": c[size_min][0], "type": c[size_min][1]})

#         if allow_exceed:
#             return make_response(jsonify({"teams": teams}), 200)
#         else:
#             return make_response(jsonify({"teams": teams, "left_over": left_over}), 200)

#     except Exception as e:
#         logging.error("Error forming teams: %s", e)
#         return make_response(
#             jsonify({"error": "An error occurred while forming teams"}), 500
#         )
