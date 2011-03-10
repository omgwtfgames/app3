# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

from client import App3Client

for i in range(0, 50):
    c = App3Client('localhost:8080', 'correct_password')
    assert c.post('person', 'george', {'name': 'george wilson', 'address': '1716 chestnut street'})
    assert c.exists('person', 'george')
    assert c.get('person', 'george')
    assert c.delete('person', 'george')
    assert not c.exists('person', 'george')
    assert c.post('person', 'george', {'name': 'george wilson', 'address': '1716 chestnut street'})
    assert c.exists('person', 'george')
    del c
    
    c = App3Client('localhost:8080', 'incorrect_password') # Models are read public, not write public
    assert c.list('person')
    assert c.exists('person', 'george')
    assert not c.post('person', 'george', {'data': 'adsf'})
    assert not c.delete('person', 'george')
    assert c.exists('person', 'george')
    assert c.get('person', 'george')
    del c
    
    c = App3Client('localhost:8080') # Models are read public, not write public - NO password:
    assert c.list('person')
    assert c.exists('person', 'george')
    assert not c.post('person', 'george', {'data': 'adsf'})
    assert not c.delete('person', 'george')
    assert not c.delete('person', 'george')
    assert c.exists('person', 'george')
    assert c.get('person', 'george')
    del c
    
    c = App3Client('localhost:8080', 'correct_password')
    assert c.post('person', 'george', {'name': 'george wilson', 'address': '1716 chestnut street'})
    assert c.exists('person', 'george')
    assert c.get('person', 'george')
    assert c.delete('person', 'george')
    assert not c.exists('person', 'george')
    assert c.post('person', 'george', {'name': 'george wilson', 'address': '1716 chestnut street'})
    assert c.exists('person', 'george')
    del c
