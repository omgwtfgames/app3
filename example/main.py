# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

import wsgiref.handlers
from google.appengine.ext import webapp

import app3

# Set up our REST resources
import models
app3.RestHandler.resources = models.resources
app3.RestHandler.secret_key = models.secret_key

def main():
    # Create the AppEngine WSGI Application
    application = webapp.WSGIApplication([
        # All URIs should be handled by the RestHandler
        ('^/.*/$', app3.RestHandler),
        ],
        debug=True
    )

    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
