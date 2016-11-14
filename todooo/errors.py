class TodoooError(Exception):
    """Catch all error for the Todooo application"""
    pass


class InvalidCommandError(TodoooError):
    """An error where the command is not recognized by the REPL"""
    def __str__(self):
        return 'You entered an invalid command'


class NoListError(TodoooError):
    """An error where a list has not been established"""
    def __str__(self):
        return 'You must specify a list to use'


class InvalidListError(TodoooError):
    """An error where a list does not exist"""
    def __str__(self):
        return 'The list you specified does not exist'


class SameItemError(TodoooError):
    """An error to signify that the same item was selected"""
    def __str__(self):
        return 'The items you selected are the same'


class InvalidArgumentError(TodoooError):
    """An error where the argument type is not what was expected"""
    def __str__(self):
        return 'You entered an invalid argument'


class ExpectedItemError(InvalidArgumentError):
    """An error where a numeric Item ID was expected"""
    def __str__(self):
        return 'Please enter a item ID'


class InvalidItemError(InvalidArgumentError):
    """An error where the Item ID is out of range"""
    def __str__(self):
        return 'Please enter a item ID from this list'
