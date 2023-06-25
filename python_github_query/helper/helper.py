def print_methods(obj):
    # Get a list of all methods
    methods = [method for method in dir(obj) if callable(getattr(obj, method))]

    # Print the list of methods
    for method in methods:
        print(method)


def print_attr(obj):
    # Get a list of all attributes
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr))]

    # Print the list of attributes
    for attribute in attributes:
        print(attribute)