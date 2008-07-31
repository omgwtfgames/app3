from google.appengine.ext import webapp, db
import app3

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
        params = {}
        for key in self.request.params:
            params[str(key)] = self.request.get(key)
            
        if "format" in params:
            format = params["format"]
            del params["format"]
        else:
            format = "text"
            
        obj = self.dispatch(self.request.path, self.request.method, params)
        obj = self.flatten(obj)
        
        if format == "json":
            self.response.headers["Content-Type"] = "application/json"
            out = simplejson.dumps(obj)
            
        elif format == "yaml":
            self.response.headers["Content-Type"] = "text/yaml"
            out = yaml.safe_dump(obj)
            
        elif format == "python":
            self.response.headers["Content-Type"] = "text/python"
            out = str(obj)
            
        elif format == "text":
            self.response.headers["Content-Type"] = "text/plain"
            out = str(obj)
            
        self.response.out.write(out)
    
    def flatten(self, obj, depth=0):
        """
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
        
        else: 
            return obj
