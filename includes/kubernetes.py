import requests

class k8s():

    def __init__(self, APIURL):
        self.APIURL = APIURL

    def getAllNodes(self):
        return(requests.get("%s/api/v1/nodes/" % self.APIURL).json())

    def getAllServices(self):
        return(requests.get("%s/api/v1/services/" % self.APIURL).json())

    def getServices(self):
        services = dict()

        for service in self.getAllServices()['items']:
            try:
                if ('hostheader' in service['metadata']['labels']):

                    services[service['metadata']['name']] = {
                     'hostheader': service['metadata']['labels']['hostheader'],
                     'uid': service['metadata']['uid'],
                     'nodePort': service['spec']['ports'][0]['nodePort']
                    }

            except Exception as e:
              logging.debug("passing on %s" % service['metadata']['name'])

        return(services)

    def getNodes(self):

        nodesList = list()

        for node in self.getAllNodes()['items']:
            try:
                # The master is not schedulable (won't create pods)
                node['spec']['unschedulable']
            except:
                for condition in node['status']['conditions']:
                    for address in node['status']['addresses']:
                        if condition['type'] == "Ready" and condition['status'] == "True" and not "master" in node['metadata']['name']:
                            if address['type'] == "InternalIP":
                                nodesList.append(address['address'])

        return(nodesList)
