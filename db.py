from google.appengine.ext import db
import app3

class ResourceModel(app3.Resource, db.Expando):
    """
    A REST Resource wrapper around an AppEngine model
    """
    
    def new(self, *args, **kwargs):
        """
        Default `new` method. Takes all the kwargs provided
        and pushes them into the database.
        """
        if kwargs:
            for key, value in kwargs.items():
                # ID must be a long value
                if key == "id": value = long(value)                
                setattr(self, key, value)
            
            self.put()
            return True
        
        else: # Need to have data to store
            return False

    def get(self, *args, **kwargs):
        """
        Default `get` method. Simply returns the object itself.
        """
        return self
    
    @classmethod
    def list(cls, max_keys=50, *args, **kwargs):
        """
        Default `list` method. Takes a max_keys argument to limit
        the size of the result set.
        """
        return cls.all().fetch(max_keys)

    def exposed_attrs(self):
        """
        Provides which attributes are exposed via the API.
        Default is everything.
        """
        return self.properties().keys() + self.dynamic_properties()