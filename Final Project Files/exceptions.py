class Error(Exception):
    """Base class for other exceptions"""
    pass

class BlankInputError(Error):
    """Raised when the input is blank"""
    pass

class ZeroInputError(Error):
    """Raised when the input is 0"""
    pass

class InvalidMassInputError(Error):
    """Raised when nothing was done in a mass action command"""
    pass