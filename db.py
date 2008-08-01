from google.appengine.ext import db
import app3

__all__ = ["ResourceModel"]

RESTRICTED_PROPERTIES = ('id', 'app3_perms', 'app3_auth', )

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
    public_read = False
    public_write = False
    
    # -----------------
    # Common Properties
    # -----------------

    id = db.StringProperty()
    app3_perms = db.ReferenceProperty(Permissions)
    
    # -------------
    # Write Methods
    # -------------
    
    @classmethod
    def new(cls, id, *args, **kwargs):
        """
        Default `new` method. Takes all the kwargs provided
        and pushes them into the database.
        """
        # Must have data to put:
        if not kwargs: return False
        
        resource = cls()
        # Set the ID
        resource.id = id
        
        # Save the Permissions with class defaults:
        resource.app3_perms = Permissions(
            public_read = cls.public_read,
            public_write = cls.public_write,
            ).put()
        
        # Assign the other values:
        for key, value in kwargs.items():
            if not key in RESTRICTED_PROPERTIES: 
                setattr(resource, key, value)
        
        # Save the resource:
        resource.put()
        
        return True

    def update(self, *args, **kwargs):
        # Nothing to update, short circuit:
        if not kwargs: return True
        
        # Assign all values:
        for key, value in kwargs.items():
            if not key in RESTRICTED_PROPERTIES: 
                setattr(self, key, value)
        
        # Save the resource:
        self.put()
        
        return True
    
    def delete(self, *args, **kwargs):
        """
        Deletes this object from the data store.
        """
        super(ResourceModel, self).delete(**kwargs)
        
        return True
    
    # ------------
    # Read Methods
    # ------------
    
    def get(self, *args, **kwargs):
        """
        Default `get` method. Simply returns the object itself.
        """
        return self

    @classmethod
    def exists(cls, id):
        """
        Returns whether the object exists or not
        """
        return cls.retrieve(id) == None
    
    @classmethod
    def retrieve(cls, id):
        """
        Retrieves an object by its id.
        """
        return cls.gql("WHERE id = :id", id=id).get()
    
    @classmethod
    def list(cls, max_keys=50, *args, **kwargs):
        """
        Default `list` method. Takes a max_keys argument to limit
        the size of the result set.
        """
        return cls.all().fetch(max_keys)

    # --------------
    # Helper Methods
    # --------------

    def exposed_attrs(self):
        """
        Provides which attributes are exposed via the API.
        Default is everything.
        """
        return self.properties().keys() + self.dynamic_properties()