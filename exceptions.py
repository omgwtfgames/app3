# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

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
    
class PermissionDeniedError(Error):
    error_type = 'PermissionDeniedError'
