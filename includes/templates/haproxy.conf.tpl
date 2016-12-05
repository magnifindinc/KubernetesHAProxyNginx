global
    log 127.0.0.1   local0
    log 127.0.0.1   local1 notice
    maxconn 4096

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option forwardfor
    option http-server-close
    
    # Timeouts
    timeout connect 4000
    timeout client  5000
    timeout server  30000

    frontend http
    bind 0.0.0.0:80

{% for service in servicesDict.items() %}
    # ACL for {{ service[0] }}
    acl {{ service[0] }}_acl hdr(host) -i {{ service[1]['hostheader'] }}
    use_backend {{ service[0] }}_backend if {{ service[0] }}_acl
{% endfor %}

{% for service in servicesDict.items() %}
backend {{ service[0] }}_backend
    balance source
    option httpclose
    option forwardfor
    {% for nodeIP in nodesList %}
    server {{ service[0] }}{{ loop.index }}{{ service[1]['uuid'] }} {{ nodeIP }}:{{ service[1]['nodePort'] }}{% endfor %}
{% endfor %}
