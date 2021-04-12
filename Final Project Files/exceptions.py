class Error(Exception):
    """Base class for other exceptions"""
    pass

class ZeroInputError(Error):
    """Raised when the input is 0"""
    pass

class InvalidMassInputError(Error):
    """Raised when nothing was done in a mass action command"""
    pass

class NoDueNoTaskError(Error):
    """Raised when the both due date AND task is blank"""
    pass

class NoTaskError(Error):
    """Raised when the both due date AND task is blank"""
    pass

class NoDueDateError(Error):
    """Raised when the ONLY due date is blank"""
    pass

class InvalidDeadlineInput(Error):
    """Raised when 'by:' keyword is not entered'"""
    pass