data = [{"kind":"Vrf","api-version":"v1","meta":{"name":"Demo-VRF-01","tenant":"default","namespace":"default","generation-id":"2","resource-version":"158782","uuid":"2055ab8c-92c6-4ea2-9778-9c62448023de","labels":{"CreatedBy":"Venice"},"creation-time":"2022-07-14T18:34:03.247815976Z","mod-time":"2022-07-14T18:34:03.234239784Z","self-link":"/venice/config/network/virtualrouters/default/Demo-VRF-01"},"spec":{"v4-route-table":"Demo-VRF-01.default","ing-v4-sec-policies":["DEMO-SP"],"eg-v4-sec-policies":["DEMO-SP"]},"status":{}},{"kind":"Vrf","api-version":"v1","meta":{"name":"default","tenant":"default","namespace":"default","generation-id":"1","resource-version":"721","uuid":"fdf5bd0b-6768-4d35-9cfa-9e34c8971895","labels":{"CreatedBy":"Venice"},"creation-time":"2022-07-13T22:39:29.256272313Z","mod-time":"2022-07-13T22:38:56.987324402Z","self-link":"/configs/network/v1/tenant/default/virtualrouters/default"},"spec":{"vrf-type":"CUSTOMER","v4-route-table":"default.default"},"status":{}},{"kind":"Vrf","api-version":"v1","meta":{"name":"pod1","tenant":"default","namespace":"default","generation-id":"1","resource-version":"1019507","uuid":"f23eafd8-608b-4c9b-baa9-a7347d33a277","labels":{"CreatedBy":"Venice"},"creation-time":"2022-07-19T07:20:41.027426067Z","mod-time":"2022-07-19T07:20:41.013618624Z","self-link":"/venice/config/network/virtualrouters/default/pod1"},"spec":{"v4-route-table":"pod1.default"},"status":{}}]
    #print(lst)
'''def dictwalk(i):
            for k,v in i.items():
                    #print( k , v)
                    if i["meta"]["name"] == "pod1":
                        uuid=i["meta"]["uuid"]
                        #print(uuid)
                        return(uuid)'''


import json

def find_uuid_vrf(i):

    for lst in i:
        #print(lst)
        #lst1=json.dumps(lst)
        lst=dict(lst)
        if lst["meta"]['name'] == "pod1":
            x=lst["meta"]["uuid"]
            return(x)


y = find_uuid_vrf(data)
print(y)
'''

def dictwalk(i):
            for k,v in i.items():
                if type(v)==dict:
                    dictwalk(v)
                else:
                    #print(k,v) 
                    if k == "uuid":
                        print(v)
                    #print(i)


for lst in data:
        #print(lst)
        x=dictwalk(lst)
        #print(x)'''