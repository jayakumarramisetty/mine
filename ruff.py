
import json
import pprint
from pprint import pprint
from collections import Counter
from collections import defaultdict
from itertools import chain
import numpy as np


flowtable = '''
Legend
Handle    : Session Handle
Role      : I (Initiator), R (Responder)
Direction : U (From Uplink), H (From Host)
BdId      : Bridge Domain ID or subnet ID
SIP       : Source IP address
Sport     : Source port for TCP/UDP
Id        : ICMP identifier
DIP       : Destination IP address
Dport     : Destination port for TCP/UDP
TyCo      : ICMP type and code
Proto     : IP Protocol
Action    : A (Allow), D (Drop), P (Pending evaluation)
--------------------------------------------------------------------------------------------------------------------------------------------
Handle  Role/Dir  BdId  SIP                                     Sport|Id  DIP                                     Dport|TyCo  Proto  Action  
--------------------------------------------------------------------------------------------------------------------------------------------
Flow-table-0
239      I/H      5     10.29.21.71                             36594     10.29.21.60                             5001        TCP       A       
239      R/U      5     10.29.21.60                             5001      10.29.21.71                             36594       TCP       A       
No. of flows: 2 
Flow-table-1
524530   I/U      5     10.29.21.60                             24018     10.29.21.71                             2048        ICMP      A       
524530   R/H      5     10.29.21.71                             24018     10.29.21.60                             0           ICMP      A       
No. of flows: 2 
Flow-table-2
Flow-table-3
1573105  I/H      5     10.29.21.71                             36590     10.29.21.60                             5001        TCP       A       
1573105  R/U      5     10.29.21.60                             5001      10.29.21.71                             36590       TCP       A       
No. of flows: 2 
Flow-table-4
Flow-table-5
2621686  I/H      5     10.29.21.71                             42028     10.29.21.60                             5001        UDP       A       
2621686  R/U      5     10.29.21.60                             5001      10.29.21.71                             42028       UDP       A       
No. of flows: 2 
Flow-table-6
Flow-table-7'''

import re
def parse_flow_table(text, table_no):
    flows = []
    table_header =  re.search(r'-+\n(.*)\n-+', text).group(1)
    table_data_match = re.search(r'Flow-table-{}\n((\d+ .*\n)+)No. of flows:'.format(table_no), text)
    if not table_data_match:
        return []
    table_data = table_data_match.group(1).strip('\n')
    header_names = table_header.split()
    for line in table_data.split('\n'):
        flow_data = line.split()
        flows.append(dict(zip(header_names, flow_data)))
    return flows
    

#flowtable1={"flows":[]}
def parse_flows(flows):
    tcp_count=0
    udp_count=0
    icmp_count=0
    other_count=0
    for i in range(0,8):
        flows1 = parse_flow_table(flows,i)
        #print(json.dumps(flows1))
        for lst in flows1:
            for k,v in lst.items():
                if k == "Proto":
                    if v=="TCP":
                        tcp_count += 1
                    elif v=="UDP":
                        udp_count +=1
                    elif v=="ICMP":
                        icmp_count +=1
                    else:
                        other_count += 1
    return (tcp_count, udp_count, icmp_count, other_count)
    #count_list=[tcp_count,udp_count,icmp_count]
    #print(count_list)
t,u,i,o=parse_flows(flowtable)

print(t,u,i,o)
                #czip_list= zip (*count_list)
            #print(czip_list)
            #print(sum(item) for item in czip_list)
                    #czip_list = sum(map(np.array, czip_list))
                    #print(czip_list)

        #flow2=[]

        #flow2.append(flows1)
        #flowtable1["flows"].append(flows1)
#flowtable1=[flowtable1]     
#print(flowtable1)
'''
for lst in flowtable1:
            #count= Counter(lst.values())
            #print(count)
            for k,v in lst.items():
                tcp_count=0
                udp_count=0
                icmp_count=0
                other_count=0
                if k == "Proto":
                    if v=="TCP":
                        tcp_count += 1
                    elif v=="UDP":
                        udp_count +=1
                    elif v=="ICMP":
                        icmp_count +=1
                    print(tcp_count,udp_count,icmp_count)

#counter_dict = Counter(chain(*flowtable1.values()))

#def dict_walk(d):
    #for k, v in d.items():
        #if type(v) == dict:
         # print(k)
         # dict_walk (v)
        #else:
          #print(k,v)
#dict_walk(data)


#print(counter_dict['TCP'])



#count = Counter(flowtable1.values())
#print(count)
'''
