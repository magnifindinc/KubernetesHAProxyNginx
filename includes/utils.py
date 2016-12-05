import os
import jinja2
import hashlib
from includes import kubernetes

class utilities():

    def renderConfigFile(self, servicesDict, nodesList, proxyType, PATH):

        templateLoader = jinja2.FileSystemLoader(os.path.join(PATH, 'templates'))
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("%s.conf.tpl" % proxyType)

        templateVars = {
                        "servicesDict": servicesDict,
                        "nodesList": nodesList 
                        }

        return(template.render(templateVars))

    def renderConfiguration(self, cliarguments):
        PATH = os.path.dirname(os.path.abspath(__file__)) 
        configuration = self.renderConfigFile(kubernetes.k8s(cliarguments.api_server).getServices(), 
                        kubernetes.k8s(cliarguments.api_server).getNodes(), 
                        cliarguments.proxy_type, PATH)
        
        return(configuration)

    def createConfigFile(self, configuration, cliarguments):
        with open("%s.conf" % cliarguments.proxy_type, 'w') as configfile:
            configfile.write(configuration)
    
    def runCommand(self, cliarguments):
        if cliarguments.dryrun:
            print("Dryrun! Should run: %s" % cliarguments.command)
        else:
            os.system('%s > /tmp/%s.log' % (cliarguments.command, cliarguments.command))
            print open('/tmp/%s.log' % cliarguments.command, 'r').read()

    def checkMD5s(self, cliarguments):
        md5 = hashlib.md5(self.renderConfiguration(cliarguments))
        currentMD5SUM = md5.hexdigest()

        smd5 = hashlib.md5(str(kubernetes.k8s(cliarguments.api_server).getServices()))
        currentSERVICESMD5SUM = smd5.hexdigest()

        return([currentMD5SUM, currentSERVICESMD5SUM])

    def andAction(self, cliarguments):
        config = self.renderConfiguration(cliarguments)
        self.createConfigFile(config, cliarguments)
        self.runCommand(cliarguments)

