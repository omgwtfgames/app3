# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

from app3 import auth

class App3Request(object):
    """
    A struct type object for storing the details of an App3 request
    
    This was built mostly 
    """
    format = "text"
    app3_timestamp = None
    app3_auth = None
    
    def __init__(self, request, secret_key=None):
        """
        """
        self.path = request.path
        self.method = request.method
        self.secret_key = secret_key
        self.params = dict([(str(key), request.get(key)) for key in request.params])
        self.headers = request.headers
        
        if "format" in self.params:
            self.format = self.params["format"]
        
        if "App3-Timestamp" in self.headers:
            self.app3_timestamp = self.headers['App3-Timestamp']
        
        if "App3-Auth" in self.headers:
            self.app3_auth = self.headers['App3-Auth']
    
    def authenticate(self):
        return auth.is_authorized(self)
    
    
