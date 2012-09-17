"""A python wrapper for the Proxmox 2.x API.

Example usage:

1) Create an instance of the prox_auth class by passing in the
url or ip of a server, username and password:

a = prox_auth('vnode01.example.org','apiuser','examplePassword')

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

# Authentication class, needs to be initialised then passed to a pyproxmox instance.
# Takes the url or IP of a server, username and password.
class prox_auth:
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

# Requires a vaild prox_auth object as a parameter.
class pyproxmox:
    # Set class variables
    def __init__(self, auth_class):
        self.url = auth_class.url
        self.ticket = auth_class.ticket
        self.CSRF = auth_class.CSRF

    #--------------------#
    # IMPORTANT METHODS  #
    #--------------------#
    
    # GET method 
    def get(self,option):
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

    # POST method
    def post(self,option, post_data):
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

    # PUT method
    def put(self,option):
        self.full_url = "https://%s:8006/api2/json/%s" % (self.url,option, post_data)
    
        self.response = cStringIO.StringIO()

        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, self.full_url)
        self.c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
        self.c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
        self.c.setopt(pycurl.HTTPHEADER, ['CSRFPreventionToken:'+str(self.CSRF)])
        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.c.setopt(pycurl.PUT, 1)

        if post_data is not None:
            post_data = urllib.urlencode(post_data)
            self.c.setopt(pycurl.POSTFIELDS, post_data)
            
        self.c.setopt(pycurl.COOKIE, "PVEAuthCookie="+str(self.ticket))
        self.c.setopt(pycurl.WRITEFUNCTION, self.response.write)
        self.c.perform()

        self.returned_data = json.loads(self.response.getvalue())
        return self.returned_data
    
    #--------------------------#
    # ADD MORE AS TIME PERMITS #
    #--------------------------#

    #-------------#
    # GET METHODS #
    #-------------#

    # Cluster Methods
    def getClusterStatus(self):
        data = self.get('cluster/status')
        return data

    def getClusterBackupSchedule(self):
        data = self.get('cluster/backup')
        return data

    

    # Node Methods
    def getNodeNetworks(self,node):
        data = self.get('nodes/%s/network' % (node))
        return data

    def getNodeInterface(self,node,interface):
        data = self.get('nodes/%s/network/%s' % (node,interface))
        return data

    def getNodeContainerIndex(self,node):
        data = self.get('nodes/%s/openvz' % (node))
        return data

    def getNodeVirtualIndex(self,node):
        data = self.get('nodes/%s/qemu' % (node))
        return data

    def getNodeServiceList(self,node):
        data = self.get('nodes/%s/services' % (node))
        return data

    def getNodeStorage(self,node):
        data = self.get('nodes/%s/storage' % (node))
        return data

    def getNodeFinishedTasks(self,node):
        data = self.get('nodes/%s/tasks' % (node))
        return data

    def getNodeDNS(self,node):
        data = self.get('nodes/%s/dns' % (node))
        return data

    def getNodeStatus(self,node):
        data = self.get('nodes/%s/status' % (node))
        return data

    def getNodeSyslog(self,node):
        data = self.get('nodes/%s/syslog' % (node))
        return data

    def getNodeRRD(self,node):
        data = self.get('nodes/%s/rrd' % (node))
        return data
    
    def getNodeRRDData(self,node):
        data = self.get('nodes/%s/rrddata' % (node))
        return data

    def getNodeBeans(self,node):
        data = self.get('nodes/%s/ubfailcnt' % (node))
        return data

    def getNodeTaskByUPID(self,node,upid):
        data = self.get('nodes/%s/tasks/%s' % (node,upid))
        return data

    def getNodeTaskLogByUPID(self,node,upid):
        data = self.get('nodes/%s/tasks/%s/log' % (node,upid))
        return data

    def getNodeTaskStatusByUPID(self,node,upid):
        data = self.get('nodes/%s/tasks/%s/status' % (node,upid))
        return data

    
    # OpenVZ Methods

    def getContainerIndex(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s' % (node,vmid))
        return data

    def getContainerStatus(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/status/current' % (node,vmid))
        return data

    def getContainerBeans(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/status/ubc' % (node,vmid))
        return data

    def getContainerConfig(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/config' % (node,vmid))
        return data

    def getContainerInitLog(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/initlog' % (node,vmid))
        return data

    def getContainerRRD(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/rrd' % (node,vmid))
        return data

    def getContainerRRDData(self,node,vmid):
        data = self.get('nodes/%s/openvz/%s/rrddata' % (node,vmid))
        return data

    # KVM Methods

    def getVirtualIndex(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s' % (node,vmid))
        return data

    def getVirtualStatus(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/status/current' % (node,vmid))
        return data

    def getVirtualBeans(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/status/ubc' % (node,vmid))
        return data

    def getVirtualConfig(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/config' % (node,vmid))
        return data

    def getVirtualInitLog(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/initlog' % (node,vmid))
        return data

    def getVirtualRRD(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/rrd' % (node,vmid))
        return data

    def getVirtualRRDData(self,node,vmid):
        data = self.get('nodes/%s/qemu/%s/rrddata' % (node,vmid))
        return data

    # Storage Methods

    def getStorageVolumeData(self,node,storage,volume):
        data = self.get('nodes/%s/storage/%s/content/%s' % (node,storage,volume))
        return data

    def getStorageConfig(self,storage):
        data = self.get('storage/%s' % (storage))
        return data
    
    def getNodeStorageContent(self,node,storage):
        data = self.get('nodes/%s/storage/%s/content' % (node,storage))
        return data

    def getNodeStorageRRD(self,node,storage):
        data = self.get('nodes/%s/storage/%s/rrd' % (node,storage))
        return data

    def getNodeStorageRRDData(self,node,storage):
        data = self.get('nodes/%s/storage/%s/rrddata' % (node,storage))
        return data

    #--------------#
    # POST METHODS #
    #--------------#

    # Create or update an OpenVZ container
    def createOpenvzContainer(self,node,vmid,template,cpus,description,disk,hostname,memory,password,swap):
        post_data = [('vmid', str(vmid)),
                     ('ostemplate', str(template)),
                     ('cpus', str(cpus)),
                     ('description', str(description)),
                     ('disk', str(disk)),
                     ('hostname', str(hostname)),
                     ('memory', str(memory)),
                     ('password', str(password)),
                     ('swap', str(swap))
                     ]
        data = self.post("nodes/%s/openvz" % (node), post_data)
        return data

    # Mount a containers private area
    def mountOpenvzPrivate(self,node,vmid):
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/mount' % (node,vmid), post_data)
        return data

    # Shut down a container
    def shutdownOpenvzContainer(self,node,vmid):
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/shutdown' % (node,vmid), post_data)
        return data

    # Start a container
    def startOpenvzContainer(self,node,vmid):
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/start' % (node,vmid), post_data)
        return data

    # Stop a container
    def stopOpenvzContainer(self,node,vmid):
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/stop' % (node,vmid), post_data)
        return data

    # Unmount a containers private area
    def unmountOpenvzPrivate(self,node,vmid):
        post_data = None
        data = self.post('nodes/%s/openvz/%s/status/unmount' % (node,vmid), post_data)
        return data

    # Migrate a container
    def migrateOpenvzContainer(self,node,vmid,target):
        post_data = [('target', str(target))]
        data = self.post('nodes/%s/openvz/%s/migrate' % (node,vmid), post_data)
        return data

    
    #--------------#
    # PUT  METHODS #
    #--------------#

    #----------------#
    # DELETE METHODS #
    #----------------#
