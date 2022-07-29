import netmiko
def config_vsx_no_dsm(nocommand):
        router_ip = "192.168.68.128"
        r_username = "admin"
        r_password = "Pensando!2345"
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vsx ')
        ssh.send_command_timing('no ' + 'vsx-sync ' + nocommand)
        ssh.disconnect()