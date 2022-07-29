import json
import io
import yaml
import json

import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ipaddress.py")
ipaddress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ipaddress)

policies = {
  "Security_policy": [
    {
      "name": "netsec1",
      "rules": [],
      "priority": ""
    }
  ]
}


from_ip = int(ipaddress.IPv4Address("192.1.1.1"))
to_ip = int(ipaddress.IPv4Address("193.1.1.1"))
rule = {}


for i in range(100):
    rule["name"] = "rule_{}".format(i)
    rule["description"] = "rule_description_{}".format(i)
    rule["action"] = "permit"
    rule["from-ip-addresses"] = [str(ipaddress.IPv4Address(from_ip + i*256))]
    rule["to-ip-addresses"] = [str(ipaddress.IPv4Address(to_ip + i*256))]
    rule["proto-ports"] = [ { "protocol": "tcp", "ports": "443,80" } ]
    rule1={}
    
    rule1.update(rule)

    #print(rule1)
    policies["Security_policy"][0]["rules"].append(rule1)
    #print(json.dumps(policies))
    #print(rule)
    #rule=dict(rule)



    
    
    #policies["Security_policy"][0]["rules"].append(rule)
    
#policies["Security_policy"][0]["rules"].append(rule1)  
print(json.dumps(policies))
print(type(policies))


#with io.open(r'/Users/jaikumar/Documents/data_1.json', 'w', encoding='utf8') as outfile:
  #json.dump(policies, outfile)

#with io.open(r'/Users/jaikumar/Documents/data5.yaml', 'w', encoding='utf8') as outfile:
  #yaml.dump_all(policies, outfile, default_flow_style=False, allow_unicode=True)

with open(r'/Users/jaikumar/Documents/data5.yaml', 'w') as f:
  yaml.dump(policies, f, default_flow_style=False, sort_keys=False)




