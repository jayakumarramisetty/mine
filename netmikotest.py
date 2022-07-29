
import netmiko
from netmiko import ConnectHandler
iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.1.50',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco',
}
net_connect =ConnectHandler(**iosv_l2)
net_connect.enable()
output =net_connect.send_command('show ip int brief')
print(output)
config_commands = [ 'int loop 0', 'ip addre 1.1.1.1 255.255.255.0', 'no sh']
output = net_connect.send_config_set(config_commands)
print (output)
output =net_connect.send_command('show ip int brief')
print (output)