
import json
import yaml
import io
import requests


# Define data
n=1
m=15





while n<=3:
   
    
    
    while m<=20:
        data = {"Security_policy": [
    {
      "name": "tes_scale" + str(n),
      "description": "rule1_policy",
      "priority": "",
      
    }
  ]}
        data1= {"rules": [
        {
          "description": "rule2_sample",
          "name": "rules2",
          "proto-ports": 
            [{
              "ports": str(m),
              "protocol": "tcp"
            }]
          ,
          "action": "permit",
          "from-ip-addresses": [
            "192.168.0.1"
          ],
          "to-ip-addresses": [
            "192.168.1.1"
          ]
        }
      ]}
       
       

        m=m+1
        print(data)
        print(data1)
    n=n+1
    with io.open(r'/Users/jaikumar/Documents/data1.json', 'a', encoding='utf8') as outfile:
            json.dump(data, outfile)
            #json.dump(data, outfile, default_flow_style=False, allow_unicode=True)
    
    #print(data)
    #with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
        #yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Write YAML file
#with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
   # yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
#with open("/Users/jaikumar/Documents/data1.json", "r") as stream:
    #data_loaded = json.load(stream)

#print(data_loaded)

