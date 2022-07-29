
import yaml
import io
import requests

# Define data
for n in range(1,5):
    for m in range(1,10):

        data =[{
  "Security_policy": [
    {
      "name": "tes_scale" + str(n),
      "description": "rule1_policy" + str(n),
      "priority": "",
      "rules": [
        {
          "description": "rule2_sample" + str(m),
          "name": "rules2" + str(m),
          "proto-ports": [
            {
              "ports": str(m),
              "protocol": "tcp"
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
      ]
    }
  ]
}]

        #m=m+1
        print(data)
        with io.open(r'/Users/jaikumar/Documents/data.yaml', 'a', encoding='utf8') as outfile:
            yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)
    #n=n+1
    #print(data)
    #with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
        #yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Write YAML file
#with io.open(r'/Users/jaikumar/Documents/data.yaml', 'w', encoding='utf8') as outfile:
   # yaml.dump_all(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
#with open("/Users/jaikumar/Documents/data.yaml", 'r') as stream:
    #data_loaded = yaml.safe_load(stream)

#print(data_loaded)