# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

import UserDict

class Resource(UserDict.DictMixin):
    """
    A customizable dictionary. Useful for object traversal and 
    encapsulation.  Easy to serialize.

    Decorators can be used to customize key access.
        
        class Dog(Resource):
            @getter
            def get_name(self):
                return self.name
                
            @setter
            def set_name(self, value):
                self.name = value.lower()
                
            @deleter
            def del_name(self):
                del self.name
    """
    
    def exposed_attrs(self):
        """
        Attribute names to be exposed as keys
        """
        return []
    
    def hidden_keys(self):
        """
        Keys to hide from iteration. A Key will still be accessible if it is 
        a getter or if it is listed in exposed_attrs()
        """
        return []
    
    def child_object(self, name):
        """
        Called to get a child object if it isn't found as a getter or an attribute
        """
        raise AttributeError
        
    # Dictionary Methods
    def __getitem__(self, key):
        """
        Called to implement evaluation of self[key]
        """
        getter = getattr(self, 'get_'+key, None)
        if hasattr(getter, 'getter'):
            return getter()
        if key in self.exposed_attrs():
            return getattr(self, key)
        return self.child_object(key)
        
    def __setitem__(self, key, value):
        """
        Called to implement assignment to self[key]
        """
        setter = getattr(self, 'set_'+key, None)
        if hasattr(setter, 'setter'):
            return setter(value)
        
    def __delitem__(self, key):
        """
        Called to implement deletion of self[key]
        """
        deleter = getattr(self, 'del_'+key, None)
        if hasattr(deleter, 'deleter'):
            return deleter(value)
        
    def keys(self):
        """
        List of keys for iteration
        """
        getter_keys = [name.replace('get_', '', 1) for name in dir(self) 
                   if hasattr(getattr(self, name, None), 'getter')]
        exposed_keys = getter_keys + self.exposed_attrs()
        return [key for key in exposed_keys if key not in self.hidden_keys()]
