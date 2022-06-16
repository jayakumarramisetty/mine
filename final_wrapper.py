import json
import io
from operator import xor
import yaml
import json
import random
import importlib.util
import ipaddress
#spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ipaddress.py")
#ipaddress = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(ipaddress)
#User provided input for both #of rules and #of policies
x=input("Enter the number of rules you need per policy: \n")
x=int(x)
y=input("Enter the number of policies: \n")
y=int(y)
#define main dict
policy4 = {"Security_policy":[]}
#1st loop start for security policy body iteration
for n in range(y):
    policies = {
      "name": "netsecpolicy"+str(n),
      "rules": [],
      "priority": ""
    }
  
#define the IP address for iteration
    sip="10."+str(n)+"."+"0."+"1"
    dip="11."+str(n)+"."+"0."+"1"
    from_ip = int(ipaddress.IPv4Address(str(sip)))
    to_ip = int(ipaddress.IPv4Address(str(dip)))
    rule = {}

#2nd loop for the rule body iteration
    for i in range(x):
        #k="permit" if (i%2==0) else "deny"
        act_list=["permit", "deny"]
        rule["name"] = "rule_{}".format(i)
        rule["description"] = "rule_description_{}".format(i)
        rule["action"] = str(random.choice(act_list))
        rule["from-ip-addresses"] = [str(ipaddress.IPv4Address(from_ip + i))]
        rule["to-ip-addresses"] = [str(ipaddress.IPv4Address(to_ip + i))]
        rule["proto-ports"] = [ { "protocol": "tcp", "ports": str(random.randint(1024,65530)) } ]
        #define the rule dictionary
        rule1={}
        rule1.update(rule)
        policies["rules"].append(rule1)
        #define policy dictionary
        policy1={}
        policy1.update(policies)

    #append the output to the final dict
    policy4["Security_policy"].append(policy1)

#print the required output
print(json.dumps(policy4)) 
# Write json to YAML file
with open(r'data_input_rules.yaml', 'w') as f:
        yaml.dump(policy4, f, default_flow_style=False, sort_keys=False)
#print the type of output and it is dictionary
print(type(policy4))








