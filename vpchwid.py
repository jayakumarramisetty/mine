
import json
import sys
import yaml

data1 = '''
typemeta: null
objmeta: null
spec:
  id:
  - 242
  - 62
  - 175
  - 216
  - 96
  - 139
  - 76
  - 155
  - 186
  - 169
  - 167
  - 52
  - 125
  - 51
  - 162
  - 119
  type: 2
  v4routetableid: []
  v6routetableid: []
  ingv4securitypolicyid: []
  ingv6securitypolicyid: []
  egv4securitypolicyid: []
  egv6securitypolicyid: []
  virtualroutermac: 0
  fabricencap:
    type: 0
    value: null
    xxx_nounkeyedliteral: {}
    xxx_unrecognized: []
    xxx_sizecache: 0
  v4meterpolicy: []
  v6meterpolicy: []
  tos: 0
  vni: []
  flowmoncollector: []
  xxx_nounkeyedliteral: {}
  xxx_unrecognized: []
  xxx_sizecache: 0
status:
  hwid: 3
  bdhwid: 4
  xxx_nounkeyedliteral: {}
  xxx_unrecognized: []
  xxx_sizecache: 0
stats:
  xxx_nounkeyedliteral: {}
  xxx_unrecognized: []
  xxx_sizecache: 0
xxx_nounkeyedliteral: {}
xxx_unrecognized: []
xxx_sizecache: 0]'''

data= yaml.safe_load(data1)
print (data)
def find(key, dictionary):
    # everything is a dict
    for k, v in dictionary.items():
        if k == key:
            yield v
            #print(v)
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
                
        

for x in find("hwid", data):
    print(x)


'''def find(key, dictionary):
    # everything is a dict
    for k, v in dictionary.items():
        if k == key:
            yield v
            #print(v)
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
                
        

for x in find("hwid", data):
    print(x)'''