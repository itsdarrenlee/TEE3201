class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidInputError(Error):
    """Raised when the input is blank"""
    pass