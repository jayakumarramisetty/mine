import json
import io
import yaml
import json

import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ipaddress.py")
ipaddress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ipaddress)

from_ip = int(ipaddress.IPv4Address("192.168.1.1"))
to_ip = int(ipaddress.IPv4Address("193.168.1.1"))
rule = {}


for i in range(24000):
       
        rule["from-ip-addresses"] = [str(ipaddress.IPv4Address(from_ip + i))]
        rule["to-ip-addresses"] = [str(ipaddress.IPv4Address(to_ip + i))]

        print(rule)