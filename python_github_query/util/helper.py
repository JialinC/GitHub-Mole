import os
import string
import random
from string import Template
from datetime import datetime


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


def add_a_year(time):
    """
    Add a year to the input time string.
    Args:
        time: time string
    Returns:
        string: time string
    """
    date_list = time.split("-")
    date_list[0] = str(int(date_list[0]) + 1)
    return "-".join(date_list)


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
