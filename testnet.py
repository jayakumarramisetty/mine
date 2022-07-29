import json
import io
from operator import xor
import yaml
import json
import random
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/ipaddress.py")
ipaddress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ipaddress) 
import netaddr
import ipaddr
import IPy
        
import netmiko
router_ip = "192.168.68.128"
r_username = "admin"
r_password = "Pensando!2345"
ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
ssh.config_mode(config_command='configure term')
ssh.send_command_timing('vsx')
ssh.send_command_timing('vsx-sync' + 'dsm')
cli11 = ssh.send_command("show run vsx")
print(cli11)


