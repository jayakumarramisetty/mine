

        

import netmiko
import paramiko
import time


def iperf_server_start():
    host_ip = '192.168.70.223'
    username = 'root'
    passwd = 'docker'

    commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
"nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
"ping 10.29.21.71 > ping_log.log & ", "ps -aux | grep iperf"]

    iperf_server= paramiko.SSHClient()
    iperf_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        iperf_server.connect(hostname=host_ip, username=username, password=passwd)
    except:
        print("[!] Cannot connect to the iperf Server")
        exit()

    for command in commands:
        print("=>"*50, command)
        stdin, stdout, stderr = iperf_server.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    return


iperf_server_start()

time.sleep(20)


def iperf_client_start():
    host_ip = '192.168.70.178'
    username = 'root'
    passwd = 'docker'

    commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t500  > test_tcp_iperf.log 2>&1 &" ,
    "nohup iperf -c 10.29.21.60 -i1 -u -t500 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

    iperf_client= paramiko.SSHClient()
    iperf_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        iperf_client.connect(hostname=host_ip, username=username, password=passwd)
    except:
        print("[!] Cannot connect to the iperf Server")
        exit()

    for command in commands1:
        print("=>"*50, command)
        stdin, stdout, stderr = iperf_client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    return




iperf_client_start()

time.sleep(150)

def iperf_client_stop():
    host_ip = '192.168.70.178'
    username = 'root'
    passwd = 'docker'

    commands1 = ["killall iperf" ,
     "ps -aux | grep iperf"]

    iperf_client= paramiko.SSHClient()
    iperf_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        iperf_client.connect(hostname=host_ip, username=username, password=passwd)
    except:
        print("[!] Cannot connect to the iperf Server")
        exit()

    for command in commands1:
        print("=>"*50, command)
        stdin, stdout, stderr = iperf_client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    return


iperf_client_stop()

def iperf_server_stop():
    host_ip = '192.168.70.223'
    username = 'root'
    passwd = 'docker'

    commands = ["killall iperf", 
"killall ping", 
 "ps -aux | grep iperf"]

    iperf_server= paramiko.SSHClient()
    iperf_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        iperf_server.connect(hostname=host_ip, username=username, password=passwd)
    except:
        print("[!] Cannot connect to the iperf Server")
        exit()

    for command in commands:
        print("=>"*50, command)
        stdin, stdout, stderr = iperf_server.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    return


iperf_server_stop()





#router_ip = ["192.168.68.128", "192.168.69.237"]
#r_username = "admin"
#r_password = "Pensando!2345"
#for ip in router_ip:
 #   ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
#    ssh.config_mode(config_command='configure term')
 #   cli11 = ssh.send_command("show vsx status")
  #  print(cli11)
   # ssh.disconnect()



