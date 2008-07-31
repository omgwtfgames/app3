from app3.db import ResourceModel
import re

class Dispatcher(object):
    resources = []    

    def dispatch(self, path, method, params):
        # Unique ID Match
        match = re.match(r'^/(?P<unique_id>\d+)/$', path)
        if match:
            return self.dispatch_unique_id(
                unique_id = long(match.group('unique_id')), 
                method = method, 
                params = params,
            )
        
        # List Match
        match = re.match(r'^/(?P<resource>[a-zA-Z]+)/$', path)
        if match:
            return self.dispatch_list(
                resource = match.group('resource'), 
                method = method, 
                params = params,
            )
        
        # Resource by ID
        match = re.match(r'^/(?P<resource>[a-zA-Z]+)/(?P<id>\d+)/$', path)
        if match:
            return self.dispatch_resource_by_id(
                resource = match.group('resource'),
                id = long(match.group('id')),
                method = method,
                params = params,
            )
    
    def dispatch_unique_id(self, unique_id, method, params):
        resource = ResourceModel.get_by_id(unique_id)
        
        # Not Found
        if not resource: return None
        
        elif method == "GET" and hasattr(resource, "get"): 
            return resource.get(**params)
        
        elif method == "POST" and hasattr(resource, "update"):
            return resource.update(**params)
        
        elif method == "DELETE" and hasattr(resource, "delete"):
            return resource.delete(**params)
        
        else: # Unknown method!
            return None
    
    def dispatch_list(self, resource, method, params):
        
        # Unknown resource
        if resource not in self.resources: return None
        
        resource = self.resources[resource]
        
        # Not a REST resource type
        if not issubclass(resource, ResourceModel): return None
        
        if method == "GET" and hasattr(resource, "list"):
            return resource.list(**params)
        
        # Creating a new resource
        elif method == "POST":
            resource = resource()
            if hasattr(resource, "new"):
                return resource.new(**params)
            
        else: # Unknown method
            return None

    
    def dispatch_resource_by_id(self, resource, id, method, params):
        
        # Unknown resource
        if resource not in self.resources: return None
        
        resource = self.resources[resource]
        
        # Not a REST resource type
        if not issubclass(resource, ResourceModel): return None
        
        resource = resource.gql("WHERE id = :id", id=id).get()
        
        # Resource by that ID not found - Should return a proper 404
        if not resource:  return None
        
        elif method == "GET" and hasattr(resource, "get"): 
            return resource.get(**params)
        
        elif method == "POST" and hasattr(resource, "update"):
            return resource.update(**params)
        
        elif method == "DELETE" and hasattr(resource, "delete"):
            return resource.delete(**params)
        
        else: # Unknown method!
            return None
