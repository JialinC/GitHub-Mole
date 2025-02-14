import random
import logging
import numpy as np
from k_means_constrained import KMeansConstrained


def label_to_type(label: int) -> str:
    """Convert a numeric label to a human-readable type."""
    return f"Type {label + 1}"


def normalize_data(columns: dict) -> np.ndarray:
    """Normalize the numerical data."""
    keys = list(columns.keys())
    numerical_data = np.array([columns[key] for key in keys[1:]], dtype=float).T
    means = np.mean(numerical_data, axis=0)
    std_devs = np.std(numerical_data, axis=0)
    return (numerical_data - means) / std_devs


def create_clusters(identifiers: list, labels: np.ndarray, team_size: int) -> list:
    """Create clusters from the labels."""
    clusters = [[] for _ in range(team_size)]
    for identifier, label in zip(identifiers, labels):
        human_readable_label = label_to_type(label)
        clusters[label].append([identifier, human_readable_label])
    for cluster in clusters:
        random.shuffle(cluster)
    return clusters


def form_teams(columns: dict, team_size: int, allow_exceed: bool) -> dict:
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
                        team_key = f"Team {over_size_team + 1}"
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
