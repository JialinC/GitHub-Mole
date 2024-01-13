import os
import re
import string
import random
from datetime import datetime, timedelta
from backend.app.services.github_query.github_graphql.query import Query
from backend.app.services.github_query.github_graphql.client import Client
from backend.app.services.github_query.queries.costs.query_cost import QueryCost


def print_methods(obj: object) -> None:
    """
    Prints all callable methods of the given object. Useful for debugging and introspection.
    
    Args:
        obj (object): The object to investigate.
    """
    methods = [method for method in dir(obj) if callable(getattr(obj, method))]
    for method in methods:
        print(method)


def print_attr(obj: object) -> None:
    """
    Prints all non-callable attributes of the given object. Useful for debugging and introspection.
    
    Args:
        obj (object): The object to investigate.
    """
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr))]
    for attribute in attributes:
        print(attribute)


def get_abs_path(file_name: str) -> str:
    """
    Constructs and returns the absolute path for a given file name, assuming the file is in the 'query_result' directory.
    
    Args:
        file_name (str): The name of the file.
    
    Returns:
        str: The absolute path of the file.
    """
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    rel_file_path = "query_result\\" + file_name
    abs_file_path = os.path.join(script_dir, rel_file_path)
    return abs_file_path


def generate_file_name() -> str:
    """
    Generates a random string of 6 characters, consisting of uppercase letters and digits, to be used as a file name.
    
    Returns:
        str: A randomly generated file name.
    """
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return file_name


def add_by_days(time_string: str, days: int) -> str:
    """
    Adds the given number of days to the given time string formatted as "%Y-%m-%dT%H:%M:%SZ".
    
    Args:
        time_string (str): The initial time string.
        days (int): The number of days to add.
    
    Returns:
        str: A new time string one year later than the input.
    """
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    # Convert the string to a datetime object
    time = datetime.strptime(time_string, time_format)

    # Add a duration of given number of days
    new_time = time + timedelta(days=days)

    # Convert the new datetime object back to a string
    new_time_string = new_time.strftime(time_format)
    return new_time_string

def minus_by_days(time_string: str, days: int) -> str:
    """
    Minus the given number of days to the given time string formatted as "%Y-%m-%dT%H:%M:%SZ".
    
    Args:
        time_string (str): The initial time string.
        days (int): The number of days to minus.
    
    Returns:
        str: A new time string one year later than the input.
    """
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    # Convert the string to a datetime object
    time = datetime.strptime(time_string, time_format)

    # Minus a duration of given number of days
    new_time = time - timedelta(days=days)

    # Convert the new datetime object back to a string
    new_time_string = new_time.strftime(time_format)
    return new_time_string


def in_time_period(time: str, start: str, end: str) -> bool:
    """
    Determines if a given time is within a specified time period.
    
    Args:
        time (str): The time to check.
        start (str): The start of the period.
        end (str): The end of the period.
    
    Returns:
        bool: True if the time is within the period; False otherwise.
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    return end >= time >= start


def created_before(created: str, time: str) -> bool:
    """
    Determines if an object was created before a certain time.
    
    Args:
        created (str): The creation time of the object.
        time (str): The time to compare against.
    
    Returns:
        bool: True if created before the specified time; False otherwise.
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
    return created < time

def created_after(created: str, time: str) -> bool:
    """
    Determines if an object was created after a certain time.
    
    Args:
        created (str): The creation time of the object.
        time (str): The time to compare against.
    
    Returns:
        bool: True if created after the specified time; False otherwise.
    """
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
    return created > time


def write_csv(file: str, data_row: str) -> None:
    """
    Appends a single line of data to a CSV file.
    
    Args:
        file (str): The file to write to.
        data_row (str): The data to write as a single line.
    """
    with open(file=file, mode='a') as f:
        f.writelines(data_row + "\n")
        f.flush()


def get_owner_and_name(link: str) -> tuple:
    """
    Extracts the repository owner's login and repository name from a GitHub URL.
    
    Args:
        link (str): The URL to parse.
    
    Returns:
        tuple: A tuple containing the owner's login and the repository name.
    """
    pattern = r"https?://(?:www\.)?github\.(?:[^/]+\.[^/]+|[^/]+)/(?P<owner>[^/]+)/?(?P<repo>[^/]+)"
    match = re.match(pattern, link)
    assert match is not None, f"Link '{link}' is invalid"
    return match.group("owner"), match.group("repo")


def have_rate_limit(client: Client, query: Query, args: dict) -> list:
    """
    Determines whether enough rate limit remains to execute a given query.
    
    Args:
        client (Client): The client to use for execution.
        query (Query): The query to execute.
        args (dict): Arguments for the query.
    
    Returns:
        list: A list containing a boolean indicating whether the rate limit is sufficient and the reset time.
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
