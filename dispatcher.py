# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

from app3.db import ResourceModel
from app3.exceptions import InvalidMethodError, ResourceNotFoundError, InvalidResourceError, InvalidPathError
import re

class Dispatcher(object):
    resources = []
    secret_key = None

    def dispatch(self, request):
        """
        Given a path, method, and parameters, dispatches the REST
        request to the appropriate 
        """
        
        # List Match /resource/
        match = re.match(r'^/(?P<resource>[a-zA-Z0-9]+)/$', request.path)
        if match:
            return self.dispatch_list(request, match.group('resource'))
        
        # Resource by ID: /resource/id/
        match = re.match(r'^/(?P<resource>[a-zA-Z0-9]+)/(?P<id>[a-zA-Z0-9]+)/$', request.path)
        if match:
            return self.dispatch_resource_by_id(
                request = request,
                resource = match.group('resource'),
                id = match.group('id'),
            )
        
        raise InvalidPathError(request)
    
    def get_resource(self, resource):
        """
        Given a resource name, return the ResourceModel object or raise
        an exception.
        """
        resource_name = resource
        
        # Unknown resource
        if resource not in self.resources:
            raise InvalidResourceError({'resource': resource, 'resource': resource})
        
        resource = self.resources[resource]
        
        # Not a REST resource type
        if not issubclass(resource, ResourceModel): 
            raise InvalidResourceError({'resource': resource, 'resource_name': resource_name})
        
        return resource
    
    def dispatch_list(self, request, resource):
        """
        Returns a list of resource objects when possible.
        """
        resource = self.get_resource(resource)()
        
        if request.method == "GET":
            return resource.list(request)
        
        else: # Unknown method
            raise InvalidMethodError(request)
    
    def dispatch_resource_by_id(self, request, resource, id):
        """
        Retrieves a resource by ID and gets, updates, creates, or deletes it
        based on the method provided.
        """
        resource_type = self.get_resource(resource)
        resource = resource_type.retrieve(request, id)
        
        if request.method == "GET":
            if resource: # Retrieve an existing resource
                return resource.get(request)
            else:
                raise ResourceNotFoundError(request)
        
        elif request.method == "POST":
            if resource: # Update an existing resource
                return resource.update(request)
            else: # Create a new resource
                return resource_type.new(request, id)
        
        elif request.method == "DELETE":
            if resource: # Delete an existing resource
                return resource.delete(request)
            else:
                raise ResourceNotFoundError(request)
        
        else: # Unknown method!
            raise InvalidMethodError(request)
