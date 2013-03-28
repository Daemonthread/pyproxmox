import sys
sys.path.append("../src")
from pyproxmox import prox_auth,pyproxmox

a = prox_auth('pnode01','apiuser@pve', 'apipasswd')

b = pyproxmox(a)

status = b.getClusterStatus()
print(status)
