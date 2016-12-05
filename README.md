# Kubernetes Dynamic Configuration for HAProxy and Nginx
## Backround
at Magnifind.ca we are using Kubernetes under AWS. in order to save costs and keep our architecture simple and secure in some cases we are using HAproxy to balance within our internal services.

Kubernetes does not integrate with HAproxy so we needed to write a small program that will help us dynamically configure HAProxy with any change done in k8s. The program writen in Python and support all versions.

We recommend using running the service under runit (We love runit!) since it's platform independant, simple fast and straight forward.

# How is it woring?
Very simple! The script pings Kubernetes API every 5 seconds if anything changes in the relevant services or update with the nodes it will reconfigure haproxy. The program will only configure HAProxy with services that is using *NodePort*

Obviously, you'll need to make small changes in the jinja template and with the DoSomething function.

# Installation and Configuration
Nothing fancy or complex... Install all the needed modules with pip and make sure this machine can access to the Kubernetes master api with no credentials.

By default, the API is exposed only on localhost you might want to solve it with a simple port farwards rule to the specific machine that samples it. 

**Another option (recommended) is to run the script from within the master and write a shell script that will run the command remotly via SSH**

### Installing

```
git clone git@github.com:magnifindinc/KubernetesHAProxy.git 
pip install -r requirements.txt
```

### Example
```
./configureService.py --api-server "http://my.kubernetes.localhost:8080" --interval 3 --proxy-type ngin
```
