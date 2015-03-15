## Models ##

In your application, you can define models wherever you want, so long as a dictionary (mapping the resource name to the actual class object) gets set to the app3.RestHandler.resources property. That is:
```
import app3
class MyModel(app3.db.ResourceModel): pass
resources = {'mymodel': MyModel,}
app3.RestHandler.resources = resources
```

In the main.py file provided in the sample application, we define the models and the resources dictionary in models.py, and assign the resources dictionary in main.py.

## Authentication ##

There are cases where you wouldn't want just anybody writing to your data store. App3 ships with global read access, but only authenticated users have write access. To be able to authenticate, you need to set the secret key variable. This can be done pretty easily:
```
import app3
app3.RestHandler.secret_key = 'my_secret_key'
```

After you've set this, in the provided client (app3.client.App3Client), you should pass the secret key as your second argument:
```
>>> from app3.client import App3Client
>>> client = App3Client('localhost:8080', 'my_secret_key')
>>> # Do authenticated things...
```

In the main.py file provided in the sample application, we define the secret key in the models.py and assign it inside main.py.

## General Model Permissions ##

If you'd like to change the permissions for an object as a whole, you can do so when you define your models. The base class (app3.db.ResourceModel) defines public\_read and public\_write. You can change these in the ResourceModel class (app3/db.py) to change the global defaults, or in your own model.

For example, in models.py of the sample application:
```
import app3
class Person(app3.db.ResourceModel):
    public_read = True
    public_write = True
```

## Row Level Permissions ##

Row level permissions are not finished yet. Soon...