# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

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
