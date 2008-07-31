from exceptions import InvalidMethodName

def getter(func):
    """
    Decorator for a method which gets a key value.  
    The decorated method must start with "get_", followed 
    by the key name which is exposed to the dictionary.
    
    A getter will be exposed in keys(), and in iteration
    """
    if not func.__name__.startswith("get_"):
        raise InvalidMethodName("method name must start with 'get_'")
    func.getter = True 
    return func
    
def setter(func):
    """
    Decorator for a method which sets a key value.
    The decorated method must start with "set_", followed 
    by the key name.
    """
    if not func.__name__.startswith("set_"):
        raise InvalidMethodName("method name must start with 'set_'")
    func.setter = True
    return func

def deleter(func):
    """
    Decorator for a method which deletes a key value.
    The decorated method must start with "del_", followed 
    by the key name.
    """
    if not func.__name__.startswith("del_"):
        raise InvalidMethodName("method name must start with 'del_'")
    func.deleter = True
    return func

def http_get_action(func):
    """
    Decorator for exposing methods through HTTP GET requests.
    
    The method is called when a request is made with "action" 
    as a parameter and the method name as the value. Additional 
    parameters are passed in as keyword arguments.
    
    The decorated method must be idempotent (no side-effects), 
    as the results may be cached.
    
    class Person:
        @http_get_action
        def say_hi(self, times=1):
            return "hi " * int(times)
    """
    func.http_get_action = True
    return func
    
def http_post_action(func):
    """
    Decorator for exposing methods through HTTP POST requests.
    
    The method is called when a request is made with "action" 
    as a parameter and the method name as the value. Additional 
    parameters are passed in as keyword arguments.
    
    HTTP POST actions may have side effects.
    
    class Person:
        @http_post_action
        def change_name(self, name):
            self.name = name
    """
    func.http_post_action = True
    return func