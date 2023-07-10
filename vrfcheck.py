
import getpass
import requests
import json
import netmiko
import time
from collections import defaultdict

ipaddr = input("Enter the IP Address of PSM: \n")
ipaddr = str(ipaddr)
username = input("Enter the Username of PSM: \n")
username = str(username)
password = getpass.getpass("Enter the Password of PSM: \n")
swi_usr = input("Enter the common Username of CX10K-switches : \n")
swi_usr = str(swi_usr)
swi_psswd = getpass.getpass("Enter the common Password of CX10K-switches: \n")

print(ipaddr)
print(username)
print(password)
DSS_IP_Address = []
VRF_list_PSM = []
VRF_list_switch = {}
todo = { "username": username,"password": password,"tenant": "default"}
api_url = "https://" + ipaddr + "/v1/login"
cookies = requests.post(api_url, json=todo, verify=False).cookies


#############
def get_dss_ip(ip):
    api_url = "https://" + ip + "/configs/cluster/v1/distributedserviceentities"
    response = requests.get(api_url, json=todo, cookies=cookies, verify=False)
    dss_api=json.loads(response.content)
    print(type(dss_api))
    print(dss_api)
    for item in dss_api['items']:
        ip_address = item['spec']['ip-config']['ip-address']
        print(ip_address)
        DSS_IP = ip_address.split("/")[0]
        DSS_IP_Address.append(DSS_IP)
    print (f"DSS_IP_Address_list : {DSS_IP_Address}")
##############
def get_psm_vrf_list(ip):
    api_url = "https://" + ip + "/configs/network/v1/tenant/default/virtualrouters"
    response = requests.get(api_url, json=todo, cookies=cookies, verify=False)
    vrf_api=json.loads(response.content)
    print(type(vrf_api))
    print(vrf_api)
    for item in vrf_api['items']:
        vrf_name_psm= item['meta']['name']
        print(vrf_name_psm)
        VRF_list_PSM.append(vrf_name_psm)
    print (f"PSM_VRF_list : {VRF_list_PSM}")
##############    
def get_vrf_list_switch():
    for ip in DSS_IP_Address:
                    router_ip = ip
                    r_username = swi_usr
                    r_password = swi_psswd
                    print("\n\nConnecting Device ",ip)
                    ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                    print("\n\n===============================Connected Device ===========================>",ip)
                    cli_output1 = ssh.send_command("show vrf | include Name")
                    ssh.disconnect()
                    #print(cli_output1)
                    list_output = [line.split(':')[1].strip() for line in cli_output1.split('\n')]
                    print(list_output)
                    VRF_list_switch["Switch_{}".format(ip)] = [list_output]

    print (type(VRF_list_switch))

################
get_dss_ip(ipaddr)
get_psm_vrf_list(ipaddr)
get_vrf_list_switch()
print(VRF_list_switch)

for key, value in VRF_list_switch.items():
    print("="*30)
    print(f'****** {key} ******')
    print("="*30)
    if value[0] == VRF_list_PSM:
        print(key, "matches the PSM_VRF list")
    else:
        extra_elements = [element for element in value[0] if element not in VRF_list_PSM]
        print(key, "does not match the PSM_VRF list")
        print("VRFs list which are not configured/missing in PSM_VRF list and are on DSS switch:", extra_elements)
        print("Warning !! Please make sure to configure the missing VRFs and match PSM and DSS to avoid impact !!")












