pyproxmox
=========

## A Python wrapper for the Proxmox 2.x API

###### Installation using pip

		sudo pip install pyproxmox

###### Example usage:

1. Import everything from the module:

		from pyproxmox import *

2. Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

		a = prox_auth('vnode01.example.org','apiuser@pve','examplePassword')

3. Create and instance of the pyproxmox class using the auth object as a parameter:

		b = pyproxmox(a)

4. Run the pre defined methods of the pyproxmox class. NOTE: they all return data, usually in JSON format:

		status = b.getClusterStatus('vnode01')

For more information see https://github.com/Daemonthread/pyproxmox

#### Methods requiring post_data

These methods need to passed a correctly formatted list of tuples.
for exmaple, if I was to use the createOpenvzContainer for the above example node
I would need to pass the post_data with all the required variables for proxmox.

	post_data = [('ostemplate','local:vztmpl/debian-6.0-standard_6.0-4_amd64.tar.gz'),
		('vmid','9001'),('cpus','4'),('description','test container'),
		('disk','10'),('hostname','test.example.org'),('memory','1024'),
		('password','testPassword'),('swap','1024')]
	
	b.createOpenvzContainer('vnode01',post_data)

For more information on the accepted variables please see http://pve.proxmox.com/pve2-api-doc/

### Current List of Methods:

##### CLUSTER GET METHODS

getClusterStatus()

getClusterBackupSchedule()

##### NODE GET METHODS

getNodeNetworks(node)

getNodeInterface(node,interface)

getNodeContainerIndex(node)

getNodeVirtualIndex(node)

getNodeServiceList(node)

getNodeStorage(node)

getNodeFinishedTasks(node)

getNodeDNS(node)

getNodeStatus(node)

getNodeSyslog(node)

getNodeRRD(node)   

getNodeRRDData(node)

getNodeBeans(node)

getNodeTaskByUPID(node,upid)

getNodeTaskLogByUPID(node,upid)

getNodeTaskStatusByUPID(node,upid)

##### OPENVZ GET METHODS

getContainerIndex(node,vmid)

getContainerStatus(node,vmid)

getContainerBeans(node,vmid)

getContainerConfig(node,vmid)

getContainerInitLog(node,vmid)

getContainerRRD(node,vmid)

getContainerRRDData(node,vmid)

##### KVM GET METHODS

getVirtualIndex(node,vmid)

getVirtualStatus(node,vmid)

getVirtualBeans(node,vmid)

getVirtualConfig(node,vmid)

getVirtualInitLog(node,vmid)

getVirtualRRD(node,vmid)

getVirtualRRDData(,node,vmid)

##### STORAGE GET METHODS

getStorageVolumeData(node,storage,volume)

getStorageConfig(storage)   

getNodeStorageContent(node,storage)

getNodeStorageRRD(node,storage)

getNodeStorageRRDData(node,storage)

##### OPENVZ POST METHODS

createOpenvzContainer(node,post_data)

mountOpenvzPrivate(node,vmid)

shutdownOpenvzContainer(node,vmid)

startOpenvzContainer(node,vmid)

stopOpenvzContainer(node,vmid)

unmountOpenvzPrivate(node,vmid)

migrateOpenvzContainer(node,vmid,target)
