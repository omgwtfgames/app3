from app3.db import ResourceModel

# All of these are Expando's meaning we can add to them as we please

class Person(ResourceModel): pass

resources = {
    'person': Person,
}

