import requests
import json
import sys
import warnings
import re
warnings.simplefilter("ignore")

if len(sys.argv) != 4:
   print ("Usage: {} IP user password".format(sys.argv[0]))
   sys.exit(1)

ipaddr = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

creds = { "username" : username, "password" : password, "tenant" : "default" }
endpoint = "https://" + ipaddr + "/v1/login"
cookies = requests.post(endpoint, json=creds, verify=False).cookies

endpoint = "https://" + ipaddr + "/configs/cluster/v1/version"
resp = json.loads(requests.get(endpoint, cookies=cookies, verify=False).text)
import pdb; pdb.set_trace()
prever = resp['status']['build-version']
#
# strip out Pipeline/Build designators
#
print (re.sub('-.*', "", prever))
