from client import Client

c = Client('localhost:8080', 'abcdefg')

print c.list('person')

print c.get('person', 'tom')