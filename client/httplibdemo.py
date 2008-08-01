import httplib

c = httplib.HTTPConnection('localhost:8080')

params = {'name': 'jimmy', 'age': '24'}
c.request('POST', '/person/tom2/', '&'.join(["%s=%s" % (k,v) for k,v in params.items()]))
r = c.getresponse()
content = r.read()
print content
c.close()

c.request('GET', '/person/')
r = c.getresponse()
content = r.read()
print content
c.close()

c.request('GET', '/person/tom/')
r = c.getresponse()
content = r.read()
print content
c.close()

c.request('GET', '/person/tom2/')
r = c.getresponse()
content = r.read()
print content
c.close()