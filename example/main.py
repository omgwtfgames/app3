import wsgiref.handlers
from google.appengine.ext import webapp

import app3

# Set up our REST resources
from models import resources
import models
app3.RestHandler.resources = resources


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
