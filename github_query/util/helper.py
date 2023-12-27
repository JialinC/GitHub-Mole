import os
import re
import string
import random
from datetime import datetime, timedelta
from github_query.github_graphql.query import Query
from github_query.github_graphql.client import Client
from github_query.queries.utils.query_cost import QueryCost


def print_methods(obj):
    """
    debug method.
    Args:
        obj: object to investigate
    """
    # Get a list of all methods
    methods = [method for method in dir(obj) if callable(getattr(obj, method))]

    # Print the list of methods
    for method in methods:
        print(method)


def print_attr(obj):
    """
    debug method.
    Args:
        obj: object to investigate
    """
    # Get a list of all attributes
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr))]

    # Print the list of attributes
    for attribute in attributes:
        print(attribute)


def get_abs_path(file_name):
    """
    Return the absolute path of the output file.
    Args:
        file_name: file name
    Returns:
        string: the absolute path of the output file
    """
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_file_path = "query_result/" + file_name
    abs_file_path = os.path.join(script_dir, rel_file_path)
    return abs_file_path


def generate_file_name():
    """
    Generate a random string as file name.
    Returns:
        string: random string of length 6
    """
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return file_name


def add_a_year(time_string):
    """
    Add a year to the input time string.
    Args:
        time_string: time string
    Returns:
        string: time string
    """
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    # Convert the string to a datetime object
    time = datetime.strptime(time_string, time_format)

    # Add a duration of 1 year
    new_time = time + timedelta(days=365)

    # Convert the new datetime object back to a string
    new_time_string = new_time.strftime(time_format)
    return new_time_string


def in_time_period(time, start, end):
    """
    Decide whether the given time is in the specified time period.
    Args:
        time: time string
        start: period starting time string
        end: period ending time string
    Returns:
        bool: true if the given time is in the time period, false otherwise
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    return end > time > start


def created_before(created, time):
    """
    Decide whether the given time is in the specified time period.
    Args:
        time: time stamp to compare against
        created: object created time
    Returns:
        bool: true if the given time is in the time period, false otherwise
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
    return created < time


def write_csv(file, data_row):
    """
    Write the given data row to given file.
    Args:
        file: path to file
        data_row: input line to write to the file
    """
    with open(file=file, mode='a') as f:
        f.writelines(data_row + "\n")
        f.flush()


def get_owner_and_name(link: str):
    """
    Parse the URL and identifies the author login and the repository name.
    Args:
        link: Link to parse
    Returns:
        Author login and repository name
    """
    pattern = r"https?://(?:www\.)?github\.(?:[^/]+\.[^/]+|[^/]+)/(?P<owner>[^/]+)/?(?P<repo>[^/]+)"
    match = re.match(pattern, link)
    assert match is not None, f"Link '{link}' is invalid"
    return match.group("owner"), match.group("repo")


def have_rate_limit(client: Client, query: Query, args: dict):
    """
    Test whether the user has enough rate limit to execute the given query
    Args:
        client: client to execute query
        query: query to be executed
        args: arguments of the query
    Returns:
        True or false user has enough rate limit to execute the given query
    """
    query_string = query.substitute(**args).__str__()
    match = re.search(r'query\s*{(?P<content>.+)}', query_string)
    rate_limit = client.execute(query=QueryCost(match.group('content')), substitutions={"dryrun": True})['rateLimit']
    cost = rate_limit['cost']
    remaining = rate_limit['remaining']
    reset_at = rate_limit['resetAt']
    if cost < remaining - 5:
        return [True, reset_at]
    else:
        return [False, reset_at]
