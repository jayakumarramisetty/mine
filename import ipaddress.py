import ipaddress
import json
import yaml
import netaddr
from netaddr import IPNetwork
for ip in IPNetwork('192.0.2.0/24'):
    dict_file=ip
with open(r'ip.yaml', 'w') as file:
    documents=yaml.dump(dict_file, file)
    print(documents)
