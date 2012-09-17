pyproxmox
=========

A Python wrapper for the Proxmox 2.x API

Example usage:

1) from pyproxmox import *

2) Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

a = prox_auth('vnode01.example.org','apiuser','examplePassword')

3) Create and instance of the pyproxmox class using the auth object as a parameter:

b = pyproxmox(a)

4) Run the pre defined methods of the pyproxmox class. NOTE: they all return data, usually in JSON format:

status = b.getClusterStatus('vnode01')

For more information see https://github.com/Daemonthread/pyproxmox

Current List of Methods:

With the exception of the RRD methods all return unformatted JSON data.
Not yet fully implemented, adding more methods as I have time.

# CLUSTER GET METHODS
getClusterStatus()
getClusterBackupSchedule()

# NODE GET METHODS
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

# OPENVZ GET METHODS

getContainerIndex(node,vmid)
getContainerStatus(node,vmid)
getContainerBeans(node,vmid)
getContainerConfig(node,vmid)
getContainerInitLog(node,vmid)
getContainerRRD(node,vmid)
getContainerRRDData(node,vmid)

# KVM GET METHODS

getVirtualIndex(node,vmid)
getVirtualStatus(node,vmid)
getVirtualBeans(node,vmid)
getVirtualConfig(node,vmid)
getVirtualInitLog(node,vmid)
getVirtualRRD(node,vmid)
getVirtualRRDData(,node,vmid)

# STORAGE GET METHODS

getStorageVolumeData(node,storage,volume)
getStorageConfig(storage)   
getNodeStorageContent(node,storage)
getNodeStorageRRD(node,storage)
getNodeStorageRRDData(node,storage)

# OPENVZ POST METHODS
createOpenvzContainer(node,vmid,template,cpus,description,disk,hostname,memory,password,swap)
mountOpenvzPrivate(node,vmid)
shutdownOpenvzContainer(node,vmid)
startOpenvzContainer(node,vmid)
stopOpenvzContainer(node,vmid)
unmountOpenvzPrivate(node,vmid)
migrateOpenvzContainer(node,vmid,target)
