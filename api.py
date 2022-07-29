from tokenize import cookie_re
from urllib import response
from wsgiref import headers
import requests
import os
from urllib.request import HTTPBasicAuthHandler
import urllib
import pensando_dss
import sys
import warnings
import re
import urllib3
import textwrap
from requests.auth import HTTPDigestAuth
import json
import warnings
warnings.simplefilter("ignore")
if len(sys.argv) !=4:
    print ("Usage: {} IP user password".format(sys.argv[0]))
ipaddr = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
print(ipaddr)
print(username)
print(password)
todo = { "username": username,"password": password,"tenant": "default"}
api_url = "https://" + ipaddr + "/v1/login"
cookies = requests.post(api_url, json=todo, verify=False).cookies
#print(cookies.json())
with open('/Users/jaikumar/Documents/input.json') as f:
    todo1=json.load(f)
    print(todo1)
api_url = "https://" + ipaddr + "/configs/security/v1/networksecuritypolicies"
response = requests.post(api_url, json=todo1, cookies=cookies, verify=False)
import pdb; pdb.set_trace()
#print(resp)
#output = resp['status']
#print (re.sub('-.*'), "", output)