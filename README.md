# Kubernetes Dynamic Configuration for HAProxy and Nginx
## Backround
at Magnifind.ca we are using Kubernetes under AWS. In order to save costs and keep our architecture simple and secure in some cases we are using HAproxy to balance within our internal services.

Kubernetes does not integrate with HAproxy so we needed to write a small program that will help us dynamically configure HAProxy/Nginx with any change done in k8s. The program writen in Python and support all versions.

We recommend using running the service under runit (We love runit!) since it's platform independant, simple fast and straight forward.

# How is it working?
Very simple! The script pings Kubernetes API every 5 seconds, if anything changes in the relevant services or update with the nodes it will generate haproxy/nginx configuration and run a script. It will only look for services that is using **NodePort**

You might need to make small changes in the jinja template and your own script. 

# Installation and Configuration
Nothing fancy or complex... Install all the needed modules with pip and if you plan to query the API from remote machine make sure it's accessible. 

You will need to add one more label (hostheader) to the service you want to load balance,

Here is an exmaple: "hostheader": "www.mydomain.tld"

### Installing

```
git clone git@github.com:magnifindinc/KubernetesHAProxyNginx.git 
pip install -r requirements.txt
```

### Example
```
./configureService.py --command ./dosomething.sh --api-server "http://my.kubernetes.localhost:8080" --interval 3 --proxy-type nginx
```

### Contact
Feel free to fork, contribute or ask any quesion :)
My Email address: adir.iakya@magnifind.ca





