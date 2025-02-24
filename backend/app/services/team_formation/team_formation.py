"""
This module provides functionality for forming teams based on normalized numerical data using constrained K-Means
clustering.
Functions:
    label_to_type(label: int) -> str:
        Convert a numeric label to a human-readable type.
    normalize_data(columns: dict) -> np.ndarray:
        Normalize the numerical data from the provided columns dictionary.
    create_clusters(identifiers: list, labels: np.ndarray, team_size: int) -> list:
        Create clusters from the labels and shuffle the members within each cluster.
    form_teams(columns: dict, team_size: int, allow_exceed: bool) -> dict:
        Form teams based on the normalized data and constrained K-Means clustering.
        Returns a dictionary containing the formed teams and optionally any leftover members.
"""

import random
import logging
import numpy as np
from k_means_constrained import KMeansConstrained


def label_to_type(label: int) -> str:
    """
    Convert a numeric label to a human-readable type.

    Args:
        label (int): The numeric label to convert.

    Returns:
        str: The human-readable type corresponding to the given label.
    """
    return f"Type {label + 1}"


def normalize_data(columns: dict) -> np.ndarray:
    """
    Normalize the numerical data.

    Parameters:
    columns (dict): A dictionary where the keys are column names and the values are lists of numerical data.

    Returns:
    np.ndarray: A 2D numpy array where the numerical data has been normalized (zero mean and unit variance).
    """
    keys = list(columns.keys())
    numerical_data = np.array([columns[key] for key in keys[1:]], dtype=float).T
    means = np.mean(numerical_data, axis=0)
    std_devs = np.std(numerical_data, axis=0)
    return (numerical_data - means) / std_devs


def create_clusters(identifiers: list, labels: np.ndarray, team_size: int) -> list:
    """
    Create clusters from the labels.

    Args:
        identifiers (list): A list of identifiers corresponding to the data points.
        labels (np.ndarray): An array of labels indicating the cluster each data point belongs to.
        team_size (int): The number of clusters to form.

    Returns:
        list: A list of clusters, where each cluster is a list of [identifier, human_readable_label] pairs.
    """
    clusters = [[] for _ in range(team_size)]
    for identifier, label in zip(identifiers, labels):
        human_readable_label = label_to_type(label)
        clusters[label].append([identifier, human_readable_label])
    for cluster in clusters:
        random.shuffle(cluster)
    return clusters


def form_teams(columns: dict, team_size: int, allow_exceed: bool) -> dict:
    """
    Forms teams based on the provided data and team size.
    Args:
        columns (dict): A dictionary where keys are column names and values are lists of data.
        team_size (int): The desired size of each team.
        allow_exceed (bool): If True, allows teams to exceed the specified team size.
    Returns:
        dict: A dictionary containing the formed teams and optionally any left-over members if exceeding is not allowed.
            - "teams" (dict): A dictionary where keys are team names and values are lists of team members.
            - "left_over" (list, optional): A list of left-over members if exceeding is not allowed.
    Raises:
        Exception: If an error occurs during the team formation process.
    """
    try:
        identifiers = columns[list(columns.keys())[0]]
        normalized_data = normalize_data(columns)
        size_min = len(normalized_data) // team_size
        size_max = size_min + 1 if len(normalized_data) % team_size > 0 else size_min

        kmeans = KMeansConstrained(
            n_clusters=team_size,
            size_min=size_min,
            size_max=size_max,
            random_state=0,
        )
        kmeans.fit(normalized_data)
        labels = kmeans.labels_

        clusters = create_clusters(identifiers, labels, team_size)
        teams = {}
        left_over = []
        for i in range(size_min):
            team_key = f"Team {i + 1}"
            teams[team_key] = []
            for j in range(team_size):
                teams[team_key].append(
                    {"id": clusters[j][i][0], "type": clusters[j][i][1]}
                )
        over_size_team = len(normalized_data) % team_size
        if over_size_team > 0:
            for c in clusters:
                if len(c) > size_min:
                    if allow_exceed:
                        team_key = f"Team {over_size_team}"
                        teams[team_key].append(
                            {"id": c[size_min][0], "type": c[size_min][1]}
                        )
                        over_size_team -= 1
                    else:
                        left_over.append({"id": c[size_min][0], "type": c[size_min][1]})

        if allow_exceed:
            return {"teams": teams}
        else:
            return {"teams": teams, "left_over": left_over}

    except Exception as e:
        logging.error("Error forming teams: %s", e)
        raise
