# Overview #

App3 is a flexible REST interface to the AppEngine Datastore that allows you to easily query models as REST resources.

## Quick Start ##

Included in App3 is a sample application that provides a single rest resource: 'person'. To get it running quickly, download the sample application package in the featured downloads and run it in AppEngine.

To check if you have the application up and running in AppEngine, try going to: http://localhost:8080/person/ in your browser. You should get an empty list displayed.
```
wget http://localhost:8080/person/ -O person.list
cat person.list
[]
```

The demo DB is a read only database unless you provide the correct secret key ('correct\_password'). All reading REST requests are permitted where write REST requests require authentication.

To easily put data into the datastore, you can use the provided REST client. If you have trouble with the following code, check out the PythonPath page for help on setting up your AppEngine environment.

Once you have your Python path set, can do the following:

```
>>> from app3.client import App3Client
>>> client = App3Client('localhost:8080', 'correct_password') # Needed for authentication
>>> client.list('person')
>>> client.post('person', 'tim', {'age': 24, 'eyes': 'brown'})
>>> client.get('person', 'tim')
>>> client.list('person')
>>> client.delete('person', 'tim')
```

See the [Configuration](http://code.google.com/p/app3/wiki/Configuration) page for more details on how to change the resources, secret key, etc.

## Useful Tools with App3 ##

  * **Note**: After looking through the REST client library available, I felt that it was just too complicated and wrote a small sample client using httplib. It is in the svn trunk under the client directory and provided with App3 and the sample application.

## Similar Projects ##

  * http://code.google.com/p/python-rest/