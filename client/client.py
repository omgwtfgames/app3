import httplib
from app3.auth import generate_auth, generate_timestamp
import random, time

class App3Request(object):
    def __init__(self, secret_key, path, params):
        self.secret_key = secret_key
        self.path = path
        self.params = params
        self.app3_timestamp = generate_timestamp()

class App3Client(object):
    """
    Simple REST Client for App3.
    """
    def __init__(self, server, secret_key=None):
        self.__client = httplib.HTTPConnection(server)
        self.__secret_key = secret_key
        
    def __format_params(self, params):
        """
        Takes a dictionary of parameters and turns them into a standard
        HTTP request query string.
        """
        if not params: params = {}
        return '&'.join(["%s=%s" % (str(k),v) for k,v in params.items()])
    
    def post(self, resource, id, params=None):
        """
        Executes a POST request on the specified resource.
        """
        response = self.__request(
            method = 'POST', 
            url = "/%s/%s/" % (resource, id), 
            params = params,
        )
        
        if response.status == 200: 
            return response.read()
        else: 
            return None

    def list(self, resource, params=None):
        """
        Lists the all of the resources of type resource.
        """
        response = self.__request(
            method = 'GET', 
            url = "/%s/" % resource, 
            params = params,
        )
        
        if response.status == 200: 
            return response.read()
        else: 
            return None
    
    def get(self, resource, id, params=None):
        """
        Retrieves the resource specified.
        """
        response = self.__request(
            method = 'GET', 
            url = "/%s/%s/" % (resource, id), 
            params = params,
        )
        
        if response.status == 200: 
            return response.read()
        else: 
            return None
    
    def exists(self, resource, id):
        """
        Returns whether the resource specified exists in the datastore.
        """
        response = self.__request(
            method = 'GET', 
            url = "/%s/%s/" % (resource, id), 
        )
        
        return response.status == 200
    
    def delete(self, resource, id):
        """
        Deletes the specified resource from the datastore.
        """
        response = self.__request(
            method = 'DELETE', 
            url = "/%s/%s/" % (resource, id), 
        )
        
        if response.status == 200: 
            return response.read()
        else: 
            return None
    
    def __request(self, method, url, params=None):
        """
        Internal method for executing all of the REST requests.
        """
        if not params: params = {}
        
        if self.__secret_key:
            request = App3Request(self.__secret_key, url, params)
            headers = {
                'App3-Auth': generate_auth(request),
                'App3-Timestamp': request.app3_timestamp,
            }
        else: 
            headers = {}
        
        params = self.__format_params(params)
        self.__client.request(method, url, params, headers)
        response = self.__client.getresponse()
        self.__client.close()
        
        return response
