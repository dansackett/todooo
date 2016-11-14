import errors


def validate_num_arguments_eq(num_args):
    """Validate that the number of supplied args is equal to some number"""
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            if len(args[1]) != num_args:
                raise errors.InvalidArgumentError
            else:
                func(*args, **kwargs)
        return wrapped_func
    return decorator


def validate_num_arguments_lt(num_args):
    """Validate that the number of supplied args is less than to some number"""
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            if len(args[1]) > num_args:
                raise errors.InvalidArgumentError
            else:
                func(*args, **kwargs)
        return wrapped_func
    return decorator


def validate_num_arguments_gt(num_args):
    """Validate that the number of supplied args is greater than to some number"""
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            if len(args[1]) < num_args:
                raise errors.InvalidArgumentError
            else:
                func(*args, **kwargs)
        return wrapped_func
    return decorator


def parse_index(lst, id):
    """Validate an index to the list is within range and a digit and return it"""
    if not id.isdigit():
        raise errors.ExpectedItemError

    idx = int(id) - 1

    if idx > len(lst) - 1 or idx < 0:
        raise errors.InvalidItemError

    return idx
