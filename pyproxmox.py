"""
A python wrapper for the Proxmox 2.x API.

Example usage:

1) Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

a = prox_auth('vnode01.example.org','apiuser@pve','examplePassword')

2) Create and instance of the pyproxmox class using the auth object as a parameter:

b = pyproxmox(a)

3) Run the pre defined methods of the pyproxmox class. NOTE: they all return data, usually in JSON format:

status = b.getClusterStatus('vnode01')

For more information see https://github.com/Daemonthread/pyproxmox.
"""
import pycurl
import urllib
import cStringIO
import json

# Authentication class
class prox_auth:
	"""
	The authentication class, requires three strings:
	
	1. An IP/resolvable url (minus the https://)
	2. Valid username, including the @pve or @pam
	3. A password
	
	Creates the required ticket and CSRF prevention token for future connections.
	
	Designed to be instanciated then passed to the new pyproxmox class as an init parameter.
	"""
    def __init__(self,url,username,password):
        self.url = url
        
        self.post_data = "username=%s&password=%s" % (username,password)
        self.full_url = "https://%s:8006/api2/json/access/ticket" % (self.url)

        self.response = cStringIO.StringIO()
    
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.full_url)
        self.c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        self.c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.c.setopt(pycurl.POST, 1)
        self.c.setopt(pycurl.POSTFIELDS, self.post_data)
        self.c.setopt(pycurl.WRITEFUNCTION, self.response.write)
        self.c.perform()

        self.returned_data = json.loads(self.response.getvalue())
        
        self.ticket = self.returned_data['data']['ticket']
        self.CSRF = self.returned_data['data']['CSRFPreventionToken']

# The meat and veg class
class pyproxmox:
    """
    A class that acts as a python wrapper for the Proxmox 2.x API.
    Requires a valid instance of the prox_auth class when initializing.
    
    GET and POST methods are currently implemented along with quite a few
    custom API methods.
    """
    # INIT
    def __init__(self, auth_class):
		"""Take the prox_auth instance and extract the important stuff"""
        self.url = auth_class.url
        self.ticket = auth_class.ticket
        self.CSRF = auth_class.CSRF
    
    # GET
    def get(self,option):
		"""
		Method for putting together and performing a GET request against
		the Proxmox API.
		
		Uses pycurl for the actual work.
		
		Requires one string variable. 
		
		The option is added to the end of the formatted url for the api.
		
		An example being a cluster status request, simply pass the string
		'cluster/status'.
		"""
        self.full_url = "https://%s:8006/api2/json/%s" % (self.url,option)
    
        self.response = cStringIO.StringIO()

        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.full_url)
        self.c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        self.c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.c.setopt(pycurl.COOKIE, "PVEAuthCookie="+str(self.ticket))
        self.c.setopt(pycurl.WRITEFUNCTION, self.response.write)
        self.c.perform()

        self.returned_data = json.loads(self.response.getvalue())
        return self.returned_data

    # POST
    def post(self,option, post_data):
		"""
		Method for putting together and performing a POST request against
		the Proxmox API.
		
		Uses pycurl for the actual work.
		
		Requires two variables. 
		
		1) option = String. This is used in the formatting of the url.
		
		An example being a request to stop container 101 on node vnode01, 
		in this case the option string would be:
		'nodes/vnode01/openvz/101/status/stop'
		
		2) post_data = a list of tuples in the format [('postname','data')]
		or None if there is no post data to be used (as in the above container
		stop example).
		"""
        self.full_url = "https://%s:8006/api2/json/%s" % (self.url,option)
    
        self.response = cStringIO.StringIO()
        
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.full_url)
        self.c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        self.c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
        self.c.setopt(pycurl.HTTPHEADER, ['CSRFPreventionToken:'+str(self.CSRF)])
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        
        if post_data is not None:
            post_data = urllib.urlencode(post_data)
            self.c.setopt(pycurl.POSTFIELDS, post_data)
            
        self.c.setopt(pycurl.POST, 1)
        self.c.setopt(pycurl.COOKIE, "PVEAuthCookie="+str(self.ticket))
        self.c.setopt(pycurl.WRITEFUNCTION, self.response.write)
        self.c.perform()

        self.returned_data = json.loads(self.response.getvalue())
        return self.returned_data

    """
    Methods using the GET protocol to communicate with the Proxmox API.
    """

    # Cluster Methods
    def getClusterStatus(self):
		"""Get cluster status information. Returns JSON"""
        data = self.get('cluster/status')
        return data

    def getClusterBackupSchedule(self):
		"""List vzdump backup schedule. Returns JSON"""
        data = self.get('cluster/backup')
        return data

    

    # Node Methods
    def getNodeNetworks(self,node):
		"""List available networks. Returns JSON"""
        data = self.get('nodes/%s/network' % (node))
        return data

    def getNodeInterface(self,node,interface):
		"""Read network device configuration. Returns JSON"""
        data = self.get('nodes/%s/network/%s' % (node,interface))
        return data

    def getNodeContainerIndex(self,node):
		"""OpenVZ container index (per node). Returns JSON"""
        data = self.get('nodes/%s/openvz' % (node))
        return data

    def getNodeVirtualIndex(self,node):
		"""Virtual machine index (per node). Returns JSON"""
        data = self.get('nodes/%s/qemu' % (node))
        return data

    def getNodeServiceList(self,node):
		"""Service list. Returns JSON"""
        data = self.get('nodes/%s/services' % (node))
        return data

    def getNodeStorage(self,node):
		"""Get status for all datastores. Returns JSON"""
        data = self.get('nodes/%s/storage' % (node))
        return data

    def getNodeFinishedTasks(self,node):
		"""Read task list for one node (finished tasks). Returns JSON"""
        data = self.get('nodes/%s/tasks' % (node))
        return data

    def getNodeDNS(self,node):
		"""Read DNS settings. Returns JSON"""
        data = self.get('nodes/%s/dns' % (node))
        return data

    def getNodeStatus(self,node):
		"""Read node status. Returns JSON"""
        data = self.get('nodes/%s/status' % (node))
        return data

    def getNodeSyslog(self,node):
		"""Read system log. Returns JSON"""
        data = self.get('nodes/%s/syslog' % (node))
        return data

    def getNodeRRD(self,node):
		"""Read node RRD statistics. Returns PNG"""
        data = self.get('nodes/%s/rrd' % (node))
        return data
    
    def getNodeRRDData(self,node):
		"""Read node RRD statistics. Returns RRD"""
        data = self.get('nodes/%s/rrddata' % (node))
        return data

    def getNodeBeans(self,node):
		"""Get user_beancounters failcnt for all active containers. Returns JSON"""
        data = self.get('nodes/%s/ubfailcnt' % (node))
        return data

    def getNodeTaskByUPID(self,node,upid):
		"""Get tasks by UPID. Returns JSON"""
        data = self.get('nodes/%s/tasks/%s' % (node,upid))
        return data

    def getNodeTaskLogByUPID(self,node,upid):
		"""Read task log. Returns JSON"""
        data = self.get('nodes/%s/tasks/%s/log' % (node,upid))
        return data

    def getNodeTaskStatusByUPID(self,node,upid):
		"""Read task status. Returns JSON"""
        data = self.get('nodes/%s/tasks/%s/status' % (node,upid))
        return data

    
    # OpenVZ Methods

    def getContainerIndex(self,node,vmid):
		"""Directory index. Returns JSON"""
        data = self.get('nodes/%s/openvz/%s' % (node,vmid))
        return data

    def getContainerStatus(self,node,vmid):
		"""Get virtual machine status. Returns JSON"""
        data = self.get('nodes/%s/openvz/%s/status/current' % (node,vmid))
        return data

    def getContainerBeans(self,node,vmid):
		"""Get container user_beancounters. Returns JSON"""
        data = self.get('nodes/%s/openvz/%s/status/ubc' % (node,vmid))
        return data

    def getContainerConfig(self,node,vmid):
		"""Get container configuration. Returns JSON"""
        data = self.get('nodes/%s/openvz/%s/config' % (node,vmid))
        return data

    def getContainerInitLog(self,node,vmid):
		"""Read init log. Returns JSON"""
        data = self.get('nodes/%s/openvz/%s/initlog' % (node,vmid))
        return data

    def getContainerRRD(self,node,vmid):
		"""Read VM RRD statistics. Returns PNG"""
        data = self.get('nodes/%s/openvz/%s/rrd' % (node,vmid))
        return data

    def getContainerRRDData(self,node,vmid):
		"""Read VM RRD statistics. Returns RRD"""
        data = self.get('nodes/%s/openvz/%s/rrddata' % (node,vmid))
        return data

    # KVM Methods

    def getVirtualIndex(self,node,vmid):
		"""Directory index. Returns JSON"""
        data = self.get('nodes/%s/qemu/%s' % (node,vmid))
        return data

    def getVirtualStatus(self,node,vmid):
		"""Get virtual machine status. Returns JSON"""
        data = self.get('nodes/%s/qemu/%s/status/current' % (node,vmid))
        return data

    def getVirtualConfig(self,node,vmid):
		"""Get virtual machine configuration. Returns JSON"""
        data = self.get('nodes/%s/qemu/%s/config' % (node,vmid))
        return data

    def getVirtualRRD(self,node,vmid):
		"""Read VM RRD statistics. Returns JSON"""
        data = self.get('nodes/%s/qemu/%s/rrd' % (node,vmid))
        return data

    def getVirtualRRDData(self,node,vmid):
		"""Read VM RRD statistics. Returns JSON"""
        data = self.get('nodes/%s/qemu/%s/rrddata' % (node,vmid))
        return data

    # Storage Methods

    def getStorageVolumeData(self,node,storage,volume):
		"""Get volume attributes. Returns JSON"""
        data = self.get('nodes/%s/storage/%s/content/%s' % (node,storage,volume))
        return data

    def getStorageConfig(self,storage):
		"""Read storage config. Returns JSON"""
        data = self.get('storage/%s' % (storage))
        return data
    
    def getNodeStorageContent(self,node,storage):
		"""List storage content. Returns JSON"""
        data = self.get('nodes/%s/storage/%s/content' % (node,storage))
        return data

    def getNodeStorageRRD(self,node,storage):
		"""Read storage RRD statistics. Returns JSON"""
        data = self.get('nodes/%s/storage/%s/rrd' % (node,storage))
        return data

    def getNodeStorageRRDData(self,node,storage):
		"""Read storage RRD statistics. Returns JSON"""
        data = self.get('nodes/%s/storage/%s/rrddata' % (node,storage))
        return data

	"""
	Methods using the POST protocol to communicate with the Proxmox API. 
	"""
	
	# OpenVZ Methods
	
    def createOpenvzContainer(self,node,post_data):
		"""
		Create or restore a container. Returns JSON
		Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]
		"""
        data = self.post("nodes/%s/openvz" % (node), post_data)
        return data

    def mountOpenvzPrivate(self,node,vmid):
		"""Mounts container private area. Returns JSON"""
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/mount' % (node,vmid), post_data)
        return data

    def shutdownOpenvzContainer(self,node,vmid):
		"""Shutdown the container. Returns JSON"""
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/shutdown' % (node,vmid), post_data)
        return data

    def startOpenvzContainer(self,node,vmid):
		"""Start the container. Returns JSON"""
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/start' % (node,vmid), post_data)
        return data

    def stopOpenvzContainer(self,node,vmid):
		"""Stop the container. Returns JSON"""
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/stop' % (node,vmid), post_data)
        return data

    def unmountOpenvzPrivate(self,node,vmid):
		"""Unmounts container private area. Returns JSON"""
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/unmount' % (node,vmid), post_data)
        return data

    def migrateOpenvzContainer(self,node,vmid,target):
		"""Migrate the container to another node. Creates a new migration task. Returns JSON"""
        post_data = [('target', str(target))]
        data = self.post('nodes/%s/openvz/%s/migrate' % (node,vmid), post_data)
        return data

    # KVM Methods
    
    def createVirtualMachine(self,node,post_data):
		"""
		Create or restore a virtual machine. Returns JSON
		Requires a dictionary of tuples formatted [('postname1','data'),('postname2','data')]
		"""
		data = self.post("nodes/%s/qemu" % (node), post_data)
		return data
		
	def resetVirtualMachine(self,node,vmid):
		"""Reset a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/reset" % (node,vmid), post_data)
		return data
		
	def resumeVirtualMachine(self,node,vmid):
		"""Resume a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/resume" % (node,vmid), post_data)
		return data
		
	def shutdownVirtualMachine(self,node,vmid):
		"""Shut down a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/shutdown" % (node,vmid), post_data)
		return data
	
	def startVirtualMachine(self,node,vmid):
		"""Start a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/start" % (node,vmid), post_data)
		return data
		
	def stopVirtualMachine(self,node,vmid):
		"""Stop a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/stop" % (node,vmid), post_data)
		return data

	def suspendVirtualMachine(self,node,vmid):
		"""Suspend a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/status/suspend" % (node,vmid), post_data)
		return data
		
	def migrateVirtualMachine(self,node,vmid,target):
		"""Migrate a virtual machine. Returns JSON"""
		post_data = [('target', str(target))]
		data = self.post("nodes/%s/qemu/%s/status/start" % (node,vmid), post_data)
		return data
		
	def monitorVirtualMachine(self,node,vmid,command):
		"""Send monitor command to a virtual machine. Returns JSON"""
		post_data = [('command', str(command))]
		data = self.post("nodes/%s/qemu/%s/monitor" % (node,vmid), post_data)
		return data
		
	def vncproxyVirtualMachine(self,node,vmid):
		"""Creates a VNC Proxy for a virtual machine. Returns JSON"""
		post_data = None
		data = self.post("nodes/%s/qemu/%s/vncproxy" % (node,vmid), post_data)
		return data
	
