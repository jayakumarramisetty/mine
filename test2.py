import netmiko
import paramiko


def iperf_server_start():
    host_ip = '192.168.70.223'
    username = 'root'
    passwd = 'docker'

    commands = [
    "iperf -s -i1  > test_tcp_iperf.log &" ,
    "iperf -s -i1 -u > test_tcp_iperf.log &",
    "ping 10.29.21.71 > ping_log.log &",
    "df -h"]

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