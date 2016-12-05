{% for service in servicesDict.items() %}
upstream {{ service[0] }}_backend {
    {% for nodeIP in nodesList %}
    server {{ nodeIP }}:{{ service[1]['nodePort'] }}{% endfor %}
} {% endfor %}
{% for service in servicesDict.items() %}
server {
    listen 80;
    server_name  {{ service[1]['hostheader'] }};

    location / {
        proxy_pass http://{{ service[0] }}_backend;
    }
} {% endfor %}
