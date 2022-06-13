import json
import io
import yaml
import json

import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ipaddress.py")
ipaddress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ipaddress)

policy4 = {"Security_policy":[]}
n=1
while n<=5:
    policies = {
      "name": "netsecpolicy"+str(n),
      "rules": [],
      "priority": ""
    }
  

    sip="10."+str(n)+"."+"0."+"1"
    dip="11."+str(n)+"."+"0."+"1"
    from_ip = int(ipaddress.IPv4Address(str(sip)))
    to_ip = int(ipaddress.IPv4Address(str(dip)))
    rule = {}


    for i in range(6):
        rule["name"] = "rule_{}".format(i)
        rule["description"] = "rule_description_{}".format(i)
        rule["action"] = "permit"
        rule["from-ip-addresses"] = [str(ipaddress.IPv4Address(from_ip + i))]
        rule["to-ip-addresses"] = [str(ipaddress.IPv4Address(to_ip + i))]
        rule["proto-ports"] = [ { "protocol": "tcp", "ports": "443,80" } ]
        rule1={}
    
        rule1.update(rule)

    #print(rule1)
        
        policies["rules"].append(rule1)
        policy1={}
        policy1.update(policies)
    #print(json.dumps(policy1))
    
    policy4["Security_policy"].append(policy1)

    
    #with open(r'/Users/jaikumar/Documents/data5.yaml', 'a') as f:
        #yaml.dump(policy1, f, default_flow_style=False, sort_keys=False)
    #print(rule)
    #rule=dict(rule)

    n=n+1

print(json.dumps(policy4)) 

with open(r'/Users/jaikumar/Documents/data5.yaml', 'a') as f:
        yaml.dump(policy4, f, default_flow_style=False, sort_keys=False)

print(type(policy4))








