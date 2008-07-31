class Error(Exception):
    """
    Base class for resource exceptions
    """
    error_type = 'GeneralError'
    def __init__(self, error):
        self.error = {'error': {
            'error': self.error_type,
            'details': error, 
            }
        }
    
    def __repr__(self):
        return self.error

class NotImplementedError(Error):
    error_type = 'NotImplementedError'

class InvalidMethodError(Error):
    error_type = 'InvalidMethodError'

class InvalidResourceError(Error):
    error_type = 'InvalidResourceError'

class ResourceNotFoundError(Error):
    error_type = 'ResourceNotFoundError'

class InvalidPathError(Error):
    error_type = 'InvalidPathError'
