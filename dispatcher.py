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
        
        # Resource by ID: /resource/id/
        match = re.match(r'^/(?P<resource>[a-zA-Z0-9]+)/(?P<id>[a-zA-Z0-9]+)/$', path)
        if match:
            return self.dispatch_resource_by_id(
                resource = match.group('resource'),
                id = match.group('id'),
                method = method,
                params = params,
            )
        
        raise InvalidPathError({'path': path, 'method': method, 'params': params, })
    
    def get_resource(self, resource):
        """
        Given a resource name, return the ResourceModel object or raise
        an exception.
        """
        resource_name = resource
        
        # Unknown resource
        if resource not in self.resources:
            raise InvalidResourceError({'resource': resource})
        
        resource = self.resources[resource]
        
        # Not a REST resource type
        if not issubclass(resource, ResourceModel): 
            raise InvalidResourceError({'resource': resource, 'resource_name': resource_name})
        
        return resource
    
    def dispatch_list(self, resource, method, params):
        """
        Returns a list of resource objects when possible.
        """
        resource = self.get_resource(resource)()
        
        if method == "GET":
            return resource.list(**params)
        
        else: # Unknown method
            raise InvalidMethodError({'method': method, 'resource': resource, 'params': params, })
    
    def dispatch_resource_by_id(self, resource, id, method, params):
        """
        Retrieves a resource by ID and gets, updates, creates, or deletes it
        based on the method provided.
        """
        resource_type = self.get_resource(resource)
        resource = resource_type.retrieve(id)
        
        if method == "GET":
            if resource: # Retrieve an existing resource
                return resource.get(**params)
            else:
                raise ResourceNotFoundError({'method': method, 'resource': resource, 'id': id, 'params': params, })
        
        elif method == "POST":
            if resource: # Update an existing resource
                return resource.update(**params)
            else: # Create a new resource
                return resource_type.new(id, **params)
        
        elif method == "DELETE":
            if resource: # Delete an existing resource
                return resource.delete(**params)
            else:
                raise ResourceNotFoundError({'method': method, 'resource': resource, 'id': id, 'params': params, })
        
        else: # Unknown method!
            raise InvalidMethodError({'method': method, 'resource': resource, 'id': id, 'params': params, })
