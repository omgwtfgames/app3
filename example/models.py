# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

from app3.db import ResourceModel

# All of these are Expando's meaning we can add to them as we please

class Person(ResourceModel): pass

resources = {
    'person': Person,
}

secret_key = 'correct_password'
