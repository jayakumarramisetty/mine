from pydoc import cli
import requests
import netmiko
import logging
import re
import sys
from pathlib import Path
import os
import time
import paramiko
import logging
from ats import aetest
sys.path.append(os.environ['PEN_SYSTEST'])
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs')
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs/operd')

import yaml
input = '''
swi_ip_stdln: ["192.168.68.128"]
swi_ip_vsx: ["192.168.68.128", "192.168.69.237"]
swi_usr: "admin"
swi_pwd: "Pensando!2345"
iperf_ip: ["192.168.71.107", "192.168.70.178"]
iperf_usr: "root"
iperf_pwd: "docker"
t_vrf: "pod1"
'''

input = yaml.safe_load(input)
vrf_name = input['t_vrf']

def vrf_list(vrf):
    vrf_list = re.split(": |, |\s", vrf)
    vrf_list.remove('VRFs')
    return(vrf_list)

def config_change_vrf_primary(vrf,dsm):
        router_ip = input['swi_ip_vsx'][0]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vrf ' + vrf)
        ssh.send_command_timing('dsm ' + dsm)
        ssh.disconnect()

def config_change_vrf_secondary(vrf,dsm):
        router_ip = input['swi_ip_vsx'][1]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vrf ' + vrf)
        ssh.send_command_timing('dsm ' + dsm)
        ssh.disconnect()

def config_vsx_dsm(command):
        router_ip = input['swi_ip_vsx'][0]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vsx ')
        ssh.send_command_timing('vsx-sync ' + command)
        ssh.disconnect()

def config_vsx_no_dsm(nocommand):
        router_ip = input['swi_ip_vsx'][0]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vsx ')
        ssh.send_command_timing('no ' + 'vsx-sync ' + nocommand)
        ssh.disconnect()

def config_interface_shut_primary(interfnum):
        router_ip = input['swi_ip_vsx'][0]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('interface ' + interfnum)
        ssh.send_command_timing('shutdown')
        ssh.disconnect()

def config_interface_noshut_primary(interfnum):
        router_ip = input['swi_ip_vsx'][0]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('interface ' + interfnum)
        ssh.send_command_timing('no shutdown')
        ssh.disconnect()

def config_interface_shut_secondary(interfnum):
        router_ip = input['swi_ip_vsx'][1]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('interface ' + interfnum)
        ssh.send_command_timing('shutdown')
        ssh.disconnect()

def config_interface_noshut_secondary(interfnum):
        router_ip = input['swi_ip_vsx'][1]
        r_username = input['swi_usr']
        r_password = input['swi_pwd']
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('interface ' + interfnum)
        ssh.send_command_timing('no shutdown')
        ssh.disconnect()
        
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

def parse_flows(flows):
    tcp_count=0
    udp_count=0
    icmp_count=0
    other_count=0
    for i in range(0,8):
        flows1 = parse_flow_table(flows,i)
        for lst in flows1:
            print(lst)
            if lst['Proto']=="TCP":
                tcp_count += 1
            elif lst['Proto']=="UDP":
                udp_count +=1
            elif lst['Proto']=="ICMP":
                icmp_count +=1
            else:
                other_count += 1
    return (tcp_count, udp_count, icmp_count, other_count)


class vrf_config_change_standalone(aetest.Testcase):
        @aetest.test
        def make_standalone(self):
            config_interface_shut_secondary("lag 111")
            print("leg on secondary is down")
            time.sleep(10)
            config_interface_shut_primary("lag 256")
            print("ISL IS down")
            time.sleep(10)
        @aetest.test
        def iperf_server_start(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
            "nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
            "nohup ping 10.29.21.71 > ping_log.log 2>&1 & ", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            


        

        time.sleep(20)

        @aetest.test
        def iperf_client_start(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t800  > test_tcp_iperf.log 2>&1 &" ,
            "nohup iperf -c 10.29.21.60 -i1 -u -t800 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    






        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = input['swi_ip_stdln']
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = input['swi_ip_stdln']
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
  
        @aetest.test 
        def vrf_config_change_standalone(self):
            router_ip = input['swi_ip_stdln'][0]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            ssh = netmiko.ConnectHandler(
               **{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        print("VRF pod1 mapped to DSM1, changing to DSM2")
                        config_change_vrf_primary(vrf_name, "1/2")
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + udp_count_pre + "\n Post: " + udp_count_post)
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + icmp_count_pre + "\n Post: " + icmp_count_post)
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + others_count_pre + "\n Post: " + others_count_post)
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        print("VRF pod1 mapped to DSM2, changing to DSM1")
                        config_change_vrf_primary(vrf_name, "1/1")
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + udp_count_pre + "\n Post: " + udp_count_post)
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + icmp_count_pre + "\n Post: " + icmp_count_post)
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + others_count_pre + "\n Post: " + others_count_post)
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            elif not test_vrf1 and not test_vrf2:
                print("No vrfs configured")
           
            
            ssh.disconnect()


        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = input['swi_ip_stdln']
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = input['swi_ip_stdln']
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = input['swi_ip_stdln']
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

        @aetest.test
        def iperf_client_stop(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["killall iperf" , "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    



        @aetest.test
        def iperf_server_stop(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["killall iperf", "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

        @aetest.test
        def make_vsx_pair_with_sync(self):
            config_interface_noshut_secondary("lag 111")
            print("leg on secondary is up")
            time.sleep(10)
            config_interface_noshut_primary("lag 256")
            print("ISL IS up")
            time.sleep(10)

            print("=>"*100)
            print("waiting for 100 sec timeout")
            time.sleep(100)
            print("=>"*100)

class verify_vsx_oper_status(aetest.Testcase):


        must_pass=True

        @aetest.test 
        def vrf_status_verify(self):
            router_ip = input['swi_ip_vsx'][0]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            ssh = netmiko.ConnectHandler(
    **{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show vsx status | i VSX")
            time.sleep(10)
            cli_output2 = ssh.send_command("show vsx status")
            print(cli_output2)
            time.sleep(10)
            print("configuring vsx sync dsm")
            config_vsx_dsm("dsm")
            re_vsx= re.search("VSX.*", cli_output1)
            vsx = re_vsx.group()
            assert vsx == "VSX Operational State"
            print("=>"*500 , "VSX configured , executing VSX_sync test case", "=>"*500)

            #else:
                #sys.exit("VSX not configured, executing standalone test case")
            ssh.disconnect()

class vrf_clitest_vsx_withsync(aetest.Testcase):


        @aetest.test
        def iperf_server_start(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
            "nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
            "nohup ping 10.29.21.71 > ping_log.log 2>&1 & ", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            


        

        time.sleep(20)

        @aetest.test
        def iperf_client_start(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t800  > test_tcp_iperf.log 2>&1 &" ,
            "nohup iperf -c 10.29.21.60 -i1 -u -t800 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    






        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_sync(self):
            router_ip = input['swi_ip_vsx'][0]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            ssh = netmiko.ConnectHandler(
               **{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        #print("configuring vsx sync dsm")
                        #config_vsx_dsm("dsm")
                        print("VRF pod1 mapped to DSM1, changing to DSM2")
                        config_change_vrf_primary(vrf_name, "1/2")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + udp_count_pre + "\n Post: " + udp_count_post)
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + icmp_count_pre + "\n Post: " + icmp_count_post)
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + others_count_pre + "\n Post: " + others_count_post)
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        #print("configuring vsx sync dsm")
                        #config_vsx_dsm("dsm")
                        print("VRF pod1 mapped to DSM2, changing to DSM1")
                        config_change_vrf_primary(vrf_name, "1/1")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + udp_count_pre + "\n Post: " + udp_count_post)
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + icmp_count_pre + "\n Post: " + icmp_count_post)
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + others_count_pre + "\n Post: " + others_count_post)
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           
            elif not test_vrf1 or not test_vrf2:
               print("No vrfs configured")
           
            
            ssh.disconnect()

        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

        @aetest.test
        def iperf_client_stop(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["killall iperf" ,"pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    



        @aetest.test
        def iperf_server_stop(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["killall iperf", "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

            print("=>"*100)
            print("waiting for 100 sec timeout")
            time.sleep(100)
            print("=>"*100)
            config_interface_shut_secondary("lag 111")
            print("Leg on secondary is down")
            time.sleep(10)

class vrf_clitest_vsx_withoutsync_primary(aetest.Testcase):


        @aetest.test
        def iperf_server_start(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
            "nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
            "nohup ping 10.29.21.71 > ping_log.log 2>&1 & ", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            


        

        time.sleep(20)

        @aetest.test
        def iperf_client_start(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t800  > test_tcp_iperf.log 2>&1 &" ,
            "nohup iperf -c 10.29.21.60 -i1 -u -t800 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_withoutsync_primary(self):
           router_ip = [input['swi_ip_vsx'][0]]
           r_username = input['swi_usr']
           r_password = input['swi_pwd']
           for ip in router_ip:
            ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unconfiguring vsx sync dsm")
                        config_vsx_no_dsm("dsm")
                        print("VRF pod1 mapped to DSM1, changing to DSM2")
                        config_change_vrf_primary(vrf_name, "1/2")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unconfiguring vsx sync dsm")
                        config_vsx_no_dsm("dsm")
                        print("VRF pod1 mapped to DSM2, changing to DSM1")
                        config_change_vrf_primary(vrf_name, "1/1")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           
            elif not test_vrf1 or not test_vrf2:
               print("No vrfs configured")
           
            
            ssh.disconnect()


        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

        @aetest.test
        def iperf_client_stop(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["killall iperf" , "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    



        @aetest.test
        def iperf_server_stop(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["killall iperf", "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            print("=>"*100)
            print("waiting for 100 sec timeout")
            time.sleep(100)
            print("=>"*100)
            config_interface_noshut_secondary("lag 111")
            print("Leg on secondary up")
            time.sleep(10)
            config_interface_shut_primary("lag 111")
            print("Leg on primary down")
            time.sleep(10)


class vrf_clitest_vsx_withoutsync_secondary(aetest.Testcase):


        @aetest.test
        def iperf_server_start(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
            "nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
            "nohup ping 10.29.21.71 > ping_log.log 2>&1 & ", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            


        

        time.sleep(20)

        @aetest.test
        def iperf_client_start(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t800  > test_tcp_iperf.log 2>&1 &" ,
            "nohup iperf -c 10.29.21.60 -i1 -u -t800 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_withoutsync_secondary(self):
           router_ip = [input['swi_ip_vsx'][1]]
           r_username = input['swi_usr']
           r_password = input['swi_pwd']
           for ip in router_ip:
            ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("VRF pod1 mapped to DSM1, changing to DSM2")
                        config_change_vrf_secondary(vrf_name, "1/2")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("VRF pod1 mapped to DSM2, changing to DSM1")
                        config_change_vrf_secondary(vrf_name, "1/1")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           
            elif not test_vrf1 or not test_vrf2:
               print("No vrfs configured")
           
            
            ssh.disconnect()

        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

        @aetest.test
        def iperf_client_stop(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["killall iperf" , "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    



        @aetest.test
        def iperf_server_stop(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["killall iperf", "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            print("=>"*100)
            print("waiting for 100 sec timeout")
            time.sleep(100)
            print("=>"*100)
            config_interface_noshut_primary("lag 111")
            print("Leg on primary up")
            time.sleep(10)

class vrf_clitest_vsx_interfaceflaps(aetest.Testcase):


        @aetest.test
        def iperf_server_start(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["nohup iperf -s -i1  > test_tcp_iperf.log 2>&1 &", 
            "nohup iperf -s -i1 -u  > test_udp_iperf.log 2>&1 &", 
            "nohup ping 10.29.21.71 > ping_log.log 2>&1 & ", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
            


        

        time.sleep(20)

        @aetest.test
        def iperf_client_start(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["nohup iperf -c 10.29.21.60 -i1 -t800  > test_tcp_iperf.log 2>&1 &" ,
            "nohup iperf -c 10.29.21.60 -i1 -u -t800 > test_udp_iperf.log 2>&1 &", "ps -aux | grep iperf"]

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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_ztraffic_test(self):
           router_ip = [input['swi_ip_vsx'][1]]
           r_username = input['swi_usr']
           r_password = input['swi_pwd']
           for ip in router_ip:
            ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("shutting down the leg interface")
                        config_interface_shut_primary("lag 111")
                        time.sleep(10)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unshutting  the leg interface")
                        config_interface_noshut_primary("lag 111")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("shutting down the leg interface")
                        config_interface_shut_primary("lag 111")
                       
                        time.sleep(10)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unshutting  the leg interface")
                        config_interface_noshut_primary("lag 111")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           
            elif not test_vrf1 or not test_vrf2:
               print("No vrfs configured")
           
            
            ssh.disconnect()

        @aetest.test
        def vrf_cli_ISL_FLAP_test(self):
           router_ip = [input['swi_ip_vsx'][1]]
           r_username = input['swi_usr']
           r_password = input['swi_pwd']
           for ip in router_ip:
            ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
            cli_output1 = ssh.send_command("show dsm 1/1 vrf")
            cli_output2 = ssh.send_command("show dsm 1/2 vrf")
            print(cli_output1)
            print(cli_output2)
            test_vrf1 = re.search("VRFs.*", cli_output1)
            test_vrf2 = re.search("VRFs.*", cli_output2)
            if test_vrf1:
               vrfs_temp = test_vrf1.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("shutting down the ISL interface")
                        config_interface_shut_primary("lag 256")
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/1", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unshutting  the ISL interface")
                        config_interface_noshut_primary("lag 256")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
            if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if vrf_name in vrf1:
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                        tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                        ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                        print("shutting down the ISL interface")
                        config_interface_shut_primary("lag 256")
                       
                        time.sleep(60)
                        ssh.send_command("diag", expect_string="#")
                        ssh.send_command("diag dsm console 1/2", expect_string="$")
                        cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                        tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                        ssh.send_command("exit",expect_string="$")
                        print("unshutting  the ISL interface")
                        config_interface_noshut_primary("lag 256")
                        assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
                        assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
                        print("FLows in vrf pod1 match before and after change to DSM mapping")
                        print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
                        print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
                        print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           
            elif not test_vrf1 or not test_vrf2:
               print("No vrfs configured")
           
            
            ssh.disconnect()

        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = [input['swi_ip_vsx'][0], input['swi_ip_vsx'][1]]
            r_username = input['swi_usr']
            r_password = input['swi_pwd']
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

        @aetest.test
        def iperf_client_stop(self):
            host_ip = input['iperf_ip'][1]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands1 = ["killall iperf" , "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
    



        @aetest.test
        def iperf_server_stop(self):
            host_ip = input['iperf_ip'][0]
            username = input['iperf_usr']
            passwd = input['iperf_pwd']

            commands = ["killall iperf", "pkill -9 iperf",
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
                time.sleep(5)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)

