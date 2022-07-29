import netmiko
import re
import json
import yaml

def find_uuid_vrf(i):
        for lst in i:
            if lst["meta"]['name'] == "pod1":
                x=lst["meta"]["uuid"]
                return(x)
def find(key, dictionary):
    # everything is a dict
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result

router_ip = "192.168.68.128"
r_username = "admin"
r_password = "Pensando!2345"
ssh = netmiko.ConnectHandler(
    **{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
ssh.send_command("start-shell", expect_string="$")
vrfs=ssh.send_command("curl localhost:9007/api/vrfs/")
#import pdb ; pdb.set_trace()
vrf2=json.loads(vrfs)
vrf_uuid = find_uuid_vrf(vrf2)
print(vrf_uuid)
ssh.send_command("exit",expect_string="#")
ssh.send_command("diag", expect_string="#")
ssh.send_command("diag dsm console 1/2", expect_string="$")
vrf_out = ssh.send_command("pdsctl show vpc --status -i " + vrf_uuid + " --yaml")
print(vrf_out)
##import pdb ; pdb.set_trace()
flow_out_raw= yaml.safe_load(vrf_out[:-7])
for x in find("hwid", flow_out_raw):
    print(x)
    vrf_hwid = x
vrf_flows = ssh.send_command("pdsctl show flow --vpcid " + str(vrf_hwid))
print(vrf_flows)

