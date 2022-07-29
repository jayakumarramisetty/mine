from multiprocessing.sharedctypes import Value
from tkinter import N
from tokenize import cookie_re
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
import yaml
import warnings
import io
warnings.simplefilter("ignore")

import collections


    #with open("/Users/jaikumar/Documents/input.json", "r") as jsonFile:
 

data= dict ( {"Security_policy": [
    {
      "name": "tes_scale",
      "description": "rule1_policy",
      "priority": "",
      "rules": [
        {
          "description": "rule2_sample",
          "name": "rules2",
          "proto-ports": 
            [{
              "ports": "100",
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
      ]
    }
  ]})

for key in data:
    print()
   # if ['rules'] in value :
        #for k,v in value['rules'].items():
            #print(k)


  
           
           
           
           
           
           # if ['ports'] in value:
       # print ()

#for key, value in data.items():
    #print(key, value)
    #if 'Security_policy' in value:
      # for k, v in value['Security_policy'].items():
           #print (k, v)
        
    
    

#print (data['Security_policy'][0]['rules'][0]['proto-ports'][0]['ports'])

#print(data)

#print