from google.appengine.ext import webapp, db
import app3
from app3.exceptions import InvalidMethodError, ResourceNotFoundError, InvalidResourceError, InvalidPathError

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
        
        resource = None
        try:
            resource = self.dispatch(self.request.path, self.request.method, params)
        
        except ResourceNotFoundError, e:
            self.error(404)
            resource = e.error
        
        except InvalidMethodError, e:
            self.error(500)
            resouce = e.error
        
        except InvalidResourceError, e:
            self.error(404)
            resource = e.error
        
        except InvalidMethodError, e:
            self.error(500)
            resouce = e.error
        
        except InvalidPathError, e:
            self.error(404)
            resource = e.error
        
        except Exception, e:
            self.error(500)
            resource = e.error
        
        resource = self.flatten(resource)
        
        if format == "json":
            self.response.headers["Content-Type"] = "application/json"
            out = simplejson.dumps(resource)
        
        elif format == "yaml":
            self.response.headers["Content-Type"] = "text/yaml"
            out = yaml.safe_dump(resource)
        
        elif format == "python":
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
        
        else: 
            return obj
