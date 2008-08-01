from google.appengine.ext import db
import app3
from app3.exceptions import PermissionDeniedError

__all__ = ["ResourceModel"]

RESTRICTED_PROPERTIES = ('id', )

class Permissions(db.Model):
    """
    Model for storing the read and write permissions on resources.
    """
    public_read = db.BooleanProperty(required=True, default=False)
    public_write = db.BooleanProperty(required=True, default=False)

class ResourceModel(app3.Resource, db.Expando):
    """
    A REST Resource wrapper around an AppEngine model
    """
    
    # -------------------
    # Permission Settings
    # -------------------
    public_read = True
    public_write = False
    secret_key = None
    
    # -----------------
    # Common Properties
    # -----------------

    id = db.StringProperty()
    app3_perms = db.ReferenceProperty(Permissions)
    
    # -------------
    # Write Methods
    # -------------
    
    @classmethod
    def new(cls, request, id):
        """
        Default `new` method. Takes all the kwargs provided
        and pushes them into the database.
        """
        # Must have data to put:
        if not request.params: return False
        
        if cls.public_write or request.authenticate():
            resource = cls()
            # Set the ID
            resource.id = id
            
            # Save the Permissions with class defaults:
            resource.app3_perms = Permissions(
                public_read = cls.public_read,
                public_write = cls.public_write,
                ).put()
            
            # Assign the other values:
            for key, value in request.params.items():
                if not key in RESTRICTED_PROPERTIES: 
                    setattr(resource, key, value)
            
            # Save the resource:
            resource.put()
            
            return True
        
        else:
            raise PermissionDeniedError(request)

    def update(self, request):
        # Nothing to update, short circuit:
        if self.public_write or request.authenticate():
            if not request.params: return True
            
            # Assign all values:
            for key, value in request.params.items():
                if not key in RESTRICTED_PROPERTIES: 
                    setattr(self, key, value)
            
            # Save the resource:
            self.put()
            
            return True
        
        else:
            raise PermissionDeniedError(request)
    
    def delete(self, request):
        """
        Deletes this object from the data store.
        """
        if self.public_write or request.authenticate():
            super(ResourceModel, self).delete(*args, **kwargs)
            
            return True
        
        else:
            raise PermissionDeniedError(request)
    
    # ------------
    # Read Methods
    # ------------
    
    def get(self, request):
        """
        Default `get` method. Simply returns the object itself.
        """
        if self.public_read or request.authenticate():
            return self
        else:
            raise PermissionDeniedError(request)

    @classmethod
    def exists(cls, request, id):
        """
        Returns whether the object exists or not
        
        Not exposed via API, used internally only.
        """
        if cls.public_read or request.authenticate():
            return cls.retrieve(id) == None
        else:
            raise PermissionDeniedError(request)
        
    @classmethod
    def retrieve(cls, request, id):
        """
        Retrieves an object by its id.
        
        Not exposed via API, used internally only.
        """
        if cls.public_read or request.authenticate():
            return cls.gql("WHERE id = :id", id=id).get()
        else:
            raise PermissionDeniedError(request)
    
    @classmethod
    def list(cls, request, max_keys=50):
        """
        Default `list` method. Takes a max_keys argument to limit
        the size of the result set.
        """
        if cls.public_read or request.authenticate():
            return cls.all().fetch(max_keys)
        else:
            raise PermissionDeniedError(request)

    # --------------
    # Helper Methods
    # --------------

    def exposed_attrs(self):
        """
        Provides which attributes are exposed via the API.
        Default is everything.
        """
        return self.properties().keys() + self.dynamic_properties()