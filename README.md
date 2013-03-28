pyproxmox
=========

## A Python wrapper for the Proxmox 2.x API

### Installation and dependency
    
    sudo pip install pyproxmox requests

###### Example usage

1. Import everything from the module

		from pyproxmox import *

2. Create an instance of the prox_auth class by passing in the
url or ip of a server in the cluster, username and password

		a = prox_auth('vnode01.example.org','apiuser@pve','examplePassword')

3. Create and instance of the pyproxmox class using the auth object as a parameter

		b = pyproxmox(a)

4. Run the pre defined methods of the pyproxmox class

		status = b.getClusterStatus()

NOTE They all return data, usually in JSON format.

For more information see https//github.com/Daemonthread/pyproxmox

#### Methods requiring post_data

These methods need to passed a correctly formatted list of tuples.
for example, if I was to use the createOpenvzContainer for the above example node
I would need to pass the post_data with all the required variables for proxmox.

	post_data = [('ostemplate','localvztmpl/debian-6.0-standard_6.0-4_amd64.tar.gz'),
				('vmid','9001'),('cpus','4'),('description','test container'),
				('disk','10'),('hostname','test.example.org'),('memory','1024'),
				('password','testPassword'),('swap','1024')]
	
	b.createOpenvzContainer('vnode01',post_data)

For more information on the accepted variables please see http//pve.proxmox.com/pve2-api-doc/

### Current List of Methods

#### GET Methods

##### Cluster Methods
		getClusterStatus()
"Get cluster status information. Returns JSON"

		getClusterBackupSchedule()
"List vzdump backup schedule. Returns JSON"

##### Node Methods
		getNodeNetworks(node)
"List available networks. Returns JSON"
  
		getNodeInterface(node,interface)
"Read network device configuration. Returns JSON"

		getNodeContainerIndex(node)
"OpenVZ container index (per node). Returns JSON"
 
		getNodeVirtualIndex(node)
"Virtual machine index (per node). Returns JSON"

		getNodeServiceList(node)
"Service list. Returns JSON"
   
		getNodeServiceState(node,service)
"Read service properties"

		getNodeStorage(node)
"Get status for all datastores. Returns JSON"
  
		getNodeFinishedTasks(node)
"Read task list for one node (finished tasks). Returns JSON"

		getNodeDNS(node)
"Read DNS settings. Returns JSON"

		getNodeStatus(node)
"Read node status. Returns JSON"

		getNodeSyslog(node)
"Read system log. Returns JSON"

		getNodeRRD(node)
"Read node RRD statistics. Returns PNG"

		getNodeRRDData(node)
"Read node RRD statistics. Returns RRD"

		getNodeBeans(node)
"Get user_beancounters failcnt for all active containers. Returns JSON"

		getNodeTaskByUPID(node,upid)
"Get tasks by UPID. Returns JSON"

		getNodeTaskLogByUPID(node,upid)
"Read task log. Returns JSON"

		getNodeTaskStatusByUPID(node,upid)
"Read task status. Returns JSON"

##### Scan

		getNodeScanMethods(node)
"Get index of available scan methods, Returns JSON"

		getRemoteiSCSI(node)
"Scan remote iSCSI server."

		getNodeLVMGroups(node)
"Scan local LVM groups"

		getRemoteNFS(node)
"Scan remote NFS server"

		getNodeUSB(node)
"List local USB devices"

    
##### OpenVZ Methods

		getContainerIndex(node,vmid)
"Directory index. Returns JSON"

		getContainerStatus(node,vmid)
"Get virtual machine status. Returns JSON"

		getContainerBeans(node,vmid)
"Get container user_beancounters. Returns JSON"

		getContainerConfig(node,vmid)
"Get container configuration. Returns JSON"

		getContainerInitLog(node,vmid)
"Read init log. Returns JSON"

		getContainerRRD(node,vmid)
"Read VM RRD statistics. Returns PNG"


		def getContainerRRDData(node,vmid)
"Read VM RRD statistics. Returns RRD"

##### KVM Methods

		getVirtualIndex(node,vmid)
"Directory index. Returns JSON"

		getVirtualStatus(node,vmid)
"Get virtual machine status. Returns JSON"

		getVirtualConfig(node,vmid)
"Get virtual machine configuration. Returns JSON"

		getVirtualRRD(node,vmid)
"Read VM RRD statistics. Returns JSON"

		getVirtualRRDData(node,vmid)
"Read VM RRD statistics. Returns JSON"

##### Storage Methods

		getStorageVolumeData(node,storage,volume)
"Get volume attributes. Returns JSON"

		getStorageConfig(storage)
"Read storage config. Returns JSON"
    
		getNodeStorageContent(node,storage)
"List storage content. Returns JSON"

		getNodeStorageRRD(node,storage)
"Read storage RRD statistics. Returns JSON"

		getNodeStorageRRDData(node,storage)
"Read storage RRD statistics. Returns JSON"


#### POST Methods

	
##### OpenVZ Methods
	
		createOpenvzContainer(node,post_data)
"Create or restore a container. Returns JSON
Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]"

		mountOpenvzPrivate(node,vmid)
"Mounts container private area. Returns JSON"

		shutdownOpenvzContainer(node,vmid)
"Shutdown the container. Returns JSON"

		startOpenvzContainer(node,vmid)
"Start the container. Returns JSON"

		stopOpenvzContainer(node,vmid)
"Stop the container. Returns JSON"

		unmountOpenvzPrivate(node,vmid)
"Unmounts container private area. Returns JSON"

		migrateOpenvzContainer(node,vmid,target)
"Migrate the container to another node. Creates a new migration task. Returns JSON"

##### KVM Methods

		createVirtualMachine(node,post_data)
"Create or restore a virtual machine. Returns JSON
Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]"
		
		resetVirtualMachine(node,vmid)
"Reset a virtual machine. Returns JSON"
		
		resumeVirtualMachine(node,vmid)
"Resume a virtual machine. Returns JSON"
	
		shutdownVirtualMachine(node,vmid)
"Shut down a virtual machine. Returns JSON"
	
		startVirtualMachine(node,vmid)
"Start a virtual machine. Returns JSON"
	
		stopVirtualMachine(node,vmid)
"Stop a virtual machine. Returns JSON"

		suspendVirtualMachine(node,vmid)
"Suspend a virtual machine. Returns JSON"
		
		migrateVirtualMachine(node,vmid,target)
"Migrate a virtual machine. Returns JSON"

		monitorVirtualMachine(node,vmid,command)
"Send monitor command to a virtual machine. Returns JSON"
		
		vncproxyVirtualMachine(node,vmid)
"Creates a VNC Proxy for a virtual machine. Returns JSON"

		rollbackVirtualMachine(node,vmid,snapname)
"Rollback a snapshot of a virtual machine. Returns JSON"

		getSnapshotConfigVirtualMachine(node,vmid,snapname)
"Get snapshot config of a virtual machine. Returns JSON"
      
#### DELETE Methods
    
##### OPENVZ
    
		deleteOpenvzContainer(node,vmid)
"Deletes the specified openvz container"

##### NODE
    
		deleteNodeNetworkConfig(node)
"Revert network configuration changes."
  
		deleteNodeInterface(node,interface)
"Delete network device configuration"
    
##### KVM
    
		deleteVirtualMachine(node,vmid)
"Destroy the vm (also delete all used/owned volumes)."
        
##### POOLS
		deletePool(poolid)
"Delete Pool"

##### STORAGE
		deleteStorageConfiguration(storageid)
"Delete storage configuration"

#### PUT Methods

##### NODE
		setNodeDNSDomain(node,domain)
"Set the nodes DNS search domain"

		setNodeSubscriptionKey(node,key)
"Set the nodes subscription key"
        
		setNodeTimeZone(node,timezone)
"Set the nodes timezone"

##### OPENVZ
		setOpenvzContainerOptions(node,vmid,post_data)
"Set openvz virtual machine options."
  
##### KVM
		setVirtualMachineOptions(node,vmide,post_data)
"Set KVM virtual machine options."

		sendKeyEventVirtualMachine(node,vmid, key)
"Send key event to virtual machine"

		unlinkVirtualMachineDiskImage(node,vmid, post_data)
"Unlink disk images"
 
##### POOLS
		setPoolData(poolid, post_data)
"Update pool data."
 
##### STORAGE
		updateStorageConfiguration(storageid,post_data)
"Update storage configuration"
