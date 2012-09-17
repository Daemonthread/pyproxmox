A python wrapper for the Proxmox 2.x API.

Example usage:

1) Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

a = prox_auth('vnode01.example.org','apiuser','examplePassword')

2) Create and instance of the pyproxmox class using the auth object as a parameter:

b = pyproxmox(a)

3) Run the pre defined methods of the pyproxmox class. NOTE: they all return data, usually in JSON format:

status = b.getClusterStatus('vnode01')

For more information see http://pypi.python.org/pypi/pyproxmox
