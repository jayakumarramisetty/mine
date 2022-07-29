from tkinter import N
import IPy
import ipaddress
import json
import yaml

import ndicts
from ndicts.ndicts import NestedDict
from ndicts.ndicts import DataDict


n=10
data = {"Security_policy": [
    {
      "name": "tes_scale",
      "description": "rule1_policy",
      "priority": "",
      
    }
  ]}

print(type(data))


#nd = NestedDict(data)

#print (nd)

#for k , v in nd.items():
  #print (k , v)

#print(data)

def dict_walk(d):
    for k, v in d.items():
        if type(v) == dict:
          for p ,  q in v.items():
            if p == ['rules']:
              




            #print(k)
              dict_walk(v)
        else:
            print (k,v)
dict_walk(data)

#def dict_walk(d):
    #for k, v in d.items():
        #if type(v) == dict:
         # print(k)
         # dict_walk (v)
        #else:
          #print(k,v)
#dict_walk(data)



            


           






            #n=10
            #while n<=20:
                #d1['proto-ports']['ports'] = n
                #n=n+1
                #print(d1)



                        
#print(data)