import httplib
import auth

class Request(object):
    def __init__(self, secret_key, path, params):
        self.secret_key = secret_key
        self.path = path
        self.params = params
        self.app3_timestamp = auth.generate_timestamp()

class App3Client(object):
    def __init__(self, server, secret_key=None):
        self.__client = httplib.HTTPConnection(server)
        self.__secret_key = secret_key
        
    def __format_params(self, params):
        return '&'.join(["%s=%s" % (str(k),v) for k,v in params.items()])
    
    def post(self, resource, id, params=None):
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
        response = self.__request(
            method = 'GET', 
            url = "/%s/%s/" % (resource, id), 
        )
        
        return response.status == 200
    
    def delete(self, resource, id):
        response = self.__request(
            method = 'DELETE', 
            url = "/%s/%s/" % (resource, id), 
        )
        
        if response.status == 200: 
            return response.read()
        else: 
            return None
    
    def __request(self, method, url, params=None):
        if not params: params = {}
        
        if self.__secret_key:
            request = Request(self.__secret_key, url, params)
            headers = {
                'App3-Auth': auth.generate_auth(request),
                'App3-Timestamp': request.app3_timestamp,
            }
        else: 
            headers = {}
        
        params = self.__format_params(params)
        self.__client.request(method, url, params, headers)
        response = self.__client.getresponse()
        self.__client.close()
        
        return response
