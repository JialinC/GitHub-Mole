from typing import List, Dict, Any
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import (
    User,
    UserQuery,
    GithubContributionData,
    CommitComment,
    IssueComment,
    GistComment,
    RepositoryDiscussionComment,
    Gist,
    Issue,
    PullRequest,
    RepositoryDiscussion,
    Repository,
    Commit,
)
from app.database import db

MODEL_MAP = {
    "total": GithubContributionData.create_from_row,
    "Commit Comments": CommitComment.create_from_row,
    "Gist Comments": GistComment.create_from_row,
    "Issue Comments": IssueComment.create_from_row,
    "Repository Discussion Comments": RepositoryDiscussionComment.create_from_row,
    "Gists": Gist.create_from_row,
    "Issues": Issue.create_from_row,
    "Pull Requests": PullRequest.create_from_row,
    "Repository Discussions": RepositoryDiscussion.create_from_row,
    "Repositories": Repository.create_from_row,
    "Repo Commits": Commit.create_from_row,
    "User Commits": Commit.create_from_row,
}

db_bp = Blueprint("db", __name__)


def convert_row_to_dict(
    table_header: List[str], table_data: List[List[Any]]
) -> List[Dict[str, Any]]:
    return [dict(zip(table_header, row)) for row in table_data]


@db_bp.route("/db/check-duplicate", methods=["POST"])
@jwt_required()
def check_duplicate():
    data = request.get_json()
    name = data.get("name")
    dstype = data.get("type")
    if dstype in [
        "Owned Original Repo",
        "Owned Forked Repo",
        "Collaborating Original Repo",
        "Collaborating Forked Repo",
    ]:
        dstype = "Repositories"
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    existing_dataset = UserQuery.query.filter_by(
        ds_name=name, user_login=user.github_login, data_type=dstype
    ).first()
    if existing_dataset:
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200


@db_bp.route("/db/save-data", methods=["POST"])
@jwt_required()
def save_to_db():
    data = request.get_json()
    ds_name = data.get("name")
    dstype = data.get("type")
    table_header = data.get("tableHeader")
    table_data = data.get("tableData")
    langs = data.get("langs")
    start_time = data.get("startTime")
    end_time = data.get("endTime")
    github_id = get_jwt_identity()
    converted_data = convert_row_to_dict(table_header, table_data)
    repo_type = None
    if dstype in [
        "Owned Original Repo",
        "Owned Forked Repo",
        "Collaborating Original Repo",
        "Collaborating Forked Repo",
    ]:
        repo_type = dstype
        dstype = "Repositories"

    try:
        with db.session.begin():
            user = User.query.filter_by(github_id=github_id).first()
            user_query = UserQuery.create(
                user_login=user.github_login,
                ds_name=ds_name,
                start_time=start_time,
                end_time=end_time,
                data_type=dstype,
            )
            db.session.flush()
            create_function = MODEL_MAP.get(dstype)
            for row in converted_data:
                if dstype == "Repositories":
                    contribution = create_function(row, repo_type, user_query.id)
                elif dstype == "total":
                    contribution = create_function(row, langs, user_query.id)
                else:
                    contribution = create_function(row, user_query.id)
                db.session.add(contribution)
            db.session.commit()
        return jsonify({"message": "Data saved successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500


@db_bp.route("/db/user-queries", methods=["GET"])
@jwt_required()
def get_user_queries():
    github_id = get_jwt_identity()
    user = User.query.filter_by(github_id=github_id).first()
    user_queries = UserQuery.query.filter_by(user_login=user.github_login).all()
    return jsonify([query.to_dict() for query in user_queries])


@db_bp.route("/db/user-queries/<query_id>", methods=["DELETE"])
@jwt_required()
def delete_user_query(query_id):
    github_id = get_jwt_identity()
    try:
        with db.session.begin():
            user = User.query.filter_by(github_id=github_id).first()
            user_query = UserQuery.query.filter_by(
                id=query_id, user_login=user.github_login
            ).first()
            db.session.delete(user_query)
            db.session.commit()
        return jsonify({"message": "Query deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@db_bp.route("/db/user-queries/<query_id>", methods=["GET"])
@jwt_required()
def get_user_query_contribution(query_id):
    user_query = UserQuery.query.filter_by(id=query_id).first()
    data_type = user_query.data_type
    contributions = []
    if data_type == "total":
        contributions = [
            contribution.to_dict() for contribution in user_query.total_contribution
        ]
    elif data_type == "Commit Comments":
        contributions = [comment.to_dict() for comment in user_query.commit_comments]
    elif data_type == "Issue Comments":
        contributions = [comment.to_dict() for comment in user_query.issue_comments]
    elif data_type == "Gist Comments":
        contributions = [comment.to_dict() for comment in user_query.gist_comments]
    elif data_type == "Repository Discussion Comments":
        contributions = [
            comment.to_dict() for comment in user_query.repository_discussion_comments
        ]
    elif data_type == "Gists":
        contributions = [gist.to_dict() for gist in user_query.gists]
    elif data_type == "Issues":
        contributions = [issue.to_dict() for issue in user_query.issues]
    elif data_type == "Pull Requests":
        contributions = [pr.to_dict() for pr in user_query.pull_requests]
    elif data_type == "Repository Discussions":
        contributions = [
            discussion.to_dict() for discussion in user_query.repository_discussion
        ]
    elif data_type == "Repositories":
        contributions = [repo.to_dict() for repo in user_query.repository]
    elif data_type == "Repo Commits" or data_type == "User Commits":
        contributions = [commit.to_dict() for commit in user_query.commit]
    return jsonify(contributions)


@db_bp.route("/db/user-contributions/<query_id>/<contribution_id>", methods=["DELETE"])
@jwt_required()
def delete_user_contribution(query_id, contribution_id):
    github_id = get_jwt_identity()
    try:
        with db.session.begin():
            user = User.query.filter_by(github_id=github_id).first()
            user_query = UserQuery.query.filter_by(
                id=query_id, user_login=user.github_login
            ).first()

            if not user_query:
                return jsonify({"error": "User query not found or not authorized"}), 404

            data_type = user_query.data_type
            contribution = None
            contribution_id = int(contribution_id)

            if data_type == "total":
                contribution = next(
                    (
                        c
                        for c in user_query.total_contribution
                        if c.id == contribution_id
                    ),
                    None,
                )
            elif data_type == "Commit Comments":
                contribution = next(
                    (c for c in user_query.commit_comments if c.id == contribution_id),
                    None,
                )
            elif data_type == "Issue Comments":
                contribution = next(
                    (c for c in user_query.issue_comments if c.id == contribution_id),
                    None,
                )
            elif data_type == "Gist Comments":
                contribution = next(
                    (c for c in user_query.gist_comments if c.id == contribution_id),
                    None,
                )
            elif data_type == "Repository Discussion Comments":
                contribution = next(
                    (
                        c
                        for c in user_query.repository_discussion_comments
                        if c.id == contribution_id
                    ),
                    None,
                )
            elif data_type == "Gists":
                contribution = next(
                    (c for c in user_query.gists if c.id == contribution_id), None
                )
            elif data_type == "Issues":
                contribution = next(
                    (c for c in user_query.issues if c.id == contribution_id), None
                )
            elif data_type == "Pull Requests":
                contribution = next(
                    (c for c in user_query.pull_requests if c.id == contribution_id),
                    None,
                )
            elif data_type == "Repository Discussions":
                contribution = next(
                    (
                        c
                        for c in user_query.repository_discussion
                        if c.id == contribution_id
                    ),
                    None,
                )
            elif data_type == "Repositories":
                contribution = next(
                    (c for c in user_query.repository if c.id == contribution_id), None
                )
            elif data_type == "Repo Commits" or data_type == "User Commits":
                contribution = next(
                    (c for c in user_query.commit if c.id == contribution_id), None
                )

            if not contribution:
                return jsonify({"error": "Contribution not found"}), 404
            db.session.delete(contribution)
            db.session.commit()
        return jsonify({"message": "Contribution deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
