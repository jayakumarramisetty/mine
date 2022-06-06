
import yaml
import io
import requests

# Define data
n=1
while n<=10:
    m=10
    while m<=100:

        data =[ {
    "Security_policy": [
        {
            "name": "tes_scale" + str(n),
            "rules": [
                {
                    "name": "rulename" + str(m),
                    "description": "rule1_sample",
                    "proto-ports": [
                        {
                            "protocol": "tcp",
                            "ports": m
                        }
                    ],
                    "action": "permit",
                    "from-ip-addresses": [
                        "192.168.0.1"
                    ],
                    "to-ip-addresses": [
                        "192.168.1.1"
                    ]
                }
            ],
            "priority": ""
        }
    ]
}]

        m=m+1
        print(data)
        with io.open(r'/Users/jaikumar/Documents/data.yaml', 'a', encoding='utf8') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    n=n+1
    #print(data)
    #with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
        #yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Write YAML file
#with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
   # yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
with open("/Users/jaikumar/Documents/data.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

#print(data_loaded)
