# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

from google.appengine.ext import webapp, db
import app3
from app3.exceptions import InvalidMethodError, ResourceNotFoundError, InvalidResourceError, InvalidPathError, PermissionDeniedError

# For serializing the result:
from django.utils import simplejson
import yaml

# Used in the flatten method
import datetime
import types
import os

class RestHandler(webapp.RequestHandler, app3.Dispatcher):
    """
    Responsible for returning the correct data to the user.
    """
    
    def get(self):
        self.dispatch_request()
        
    def put(self):
        self.dispatch_request()
        
    def post(self):
        self.dispatch_request()
        
    def delete(self):
        self.dispatch_request()
        
    def dispatch_request(self):
        """
        Dispatches the request to the dispatcher, which returns
        the correct resource or raises a specified exception.
        """
        request = app3.App3Request(self.request, self.secret_key)
        
        resource = None
        try:
            resource = self.dispatch(request)
            
        except PermissionDeniedError, e:
            self.error(401)
            resource = e.error
        
        except ResourceNotFoundError, e:
            self.error(404)
            resource = e.error
        
        except InvalidMethodError, e:
            self.error(500)
            resource = e.error
        
        except InvalidResourceError, e:
            self.error(404)
            resource = e.error
        
        except InvalidMethodError, e:
            self.error(500)
            resouce = e.error
        
        except InvalidPathError, e:
            self.error(404)
            resource = e.error
        
        #except Exception, e:
            #self.error(500)
            #resource = e.message
        
        resource = self.flatten(resource)
        
        if request.format == "json":
            self.response.headers["Content-Type"] = "application/json"
            out = simplejson.dumps(resource)
        
        elif request.format == "yaml":
            self.response.headers["Content-Type"] = "text/yaml"
            out = yaml.safe_dump(resource)
        
        elif request.format == "python":
            self.response.headers["Content-Type"] = "text/python"
            out = str(resource)
        
        else:
            self.response.headers["Content-Type"] = "text/plain"
            out = str(resource)
        
        self.response.out.write(out)
    
    def flatten(self, obj, depth=0):
        """
        Thank you to the author at http://python-rest.googlecode.com for this.
        It was licensed as Apache v 2, so please use with care.
        
        Recursively flattens objects to a serializable form:
            datetime.datetime -> iso formatted date string
            db.users.User -> user nickname
            db.GeoPt -> string
            db.IM -> string
            db.Key -> string
        
        Returns:
            A shallow copy of the object
        
        Reference:
            http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html
            http://python-rest.googlecode.com
        
        """
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        
        elif isinstance(obj, db.users.User):
            return obj.nickname()
        
        elif isinstance(obj, (db.GeoPt, db.IM, db.Key)):
            return str(obj)
        
        elif isinstance(obj, types.ListType):
            return [self.flatten(item, depth+1) for item in obj]
        
        elif isinstance(obj, (types.DictType, app3.Resource)):
            copy = {}
            for key in obj:
                copy[key] = self.flatten(obj[key], depth+1)
            return copy
        
        elif isinstance(obj, db.Model): # If it is a model, go down one level:
            return dict([(key, getattr(obj, key)) for key in obj.properties()])
        
        else: 
            return obj
