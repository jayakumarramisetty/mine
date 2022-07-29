import paramiko

def iperf_client_start():
    host_ip = '192.168.70.178'
    username = 'root'
    passwd = 'docker'

    commands1 = ["./iperf_client.sh",
    "df -h"]

    iperf_client= paramiko.SSHClient()
    iperf_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        iperf_client.connect(hostname=host_ip, username=username, password=passwd)
    except:
        print("[!] Cannot connect to the iperf Server")
        exit()

    for command in commands1:
        print(command)
        stdin, stdout, stderr = iperf_client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
    return


iperf_client_start()