class Error(Exception):
    """Base class for Rest resource exceptions"""
    pass

class NotImplementedError(Error):
    pass

class InvalidMethodName(Error):
    pass
