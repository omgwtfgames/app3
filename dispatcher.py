from app3.db import ResourceModel
from app3.exceptions import InvalidMethodError, ResourceNotFoundError, InvalidResourceError, InvalidPathError
import re

class Dispatcher(object):
    resources = []    

    def dispatch(self, path, method, params):
        """
        Given a path, method, and parameters, dispatches the REST
        request to the appropriate 
        """
        
        # List Match /resource/
        match = re.match(r'^/(?P<resource>[a-zA-Z0-9]+)/$', path)
        if match:
            return self.dispatch_list(
                resource = match.group('resource'), 
                method = method, 
                params = params,
            )
        
        # Resource by ID: /resource/##/
        match = re.match(r'^/(?P<resource>[a-zA-Z0-9]+)/(?P<id>\d+)/$', path)
        if match:
            return self.dispatch_resource_by_id(
                resource = match.group('resource'),
                id = long(match.group('id')),
                method = method,
                params = params,
            )
        
        raise InvalidPathError({'path': path, 'method': method, 'params': params, })
    
    def get_resource(self, resource, id=None):
        resource_name = resource
        
        # Unknown resource
        if resource not in self.resources:
            raise InvalidResourceError({'resource': resource})
        
        resource = self.resources[resource]
        
        # Not a REST resource type
        if not issubclass(resource, ResourceModel): 
            raise InvalidResourceError({'resource': resource, 'resource_name': resource_name})
        
        if id:         
            resource = resource.gql("WHERE id = :id", id=id).get()
            
            # Resource by that ID not found - Should return a proper 404
            if not resource: 
                raise ResourceNotFoundError({'resource': resource, 'id': id})
        
        return resource
    
    def dispatch_list(self, resource, method, params):        
        resouce = self.get_resource(resource)()
        
        if method == "GET" and hasattr(resource, "list"):
            return resource.list(**params)
        
        # Creating a new resource
        elif method == "POST":
            resource = resource()
            if hasattr(resource, "new"):
                return resource.new(**params)
            
        else: # Unknown method
            raise InvalidMethodError({'method': method, 'resource': resource, 'params': params, })
    
    def dispatch_resource_by_id(self, resource, id, method, params):
        resource = self.get_resource(resource, id)
        
        if method == "GET" and hasattr(resource, "get"): 
            return resource.get(**params)
        
        elif method == "POST" and hasattr(resource, "update"):
            return resource.update(**params)
        
        elif method == "DELETE" and hasattr(resource, "delete"):
            return resource.delete(**params)
        
        else: # Unknown method!
            raise InvalidMethodError({'method': method, 'resource': resource, 'id': id, 'params': params, })
