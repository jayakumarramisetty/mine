from pydoc import cli
import requests
import netmiko
import logging
import re
import sys
from pathlib import Path
import os
import time
import logging
from ats import aetest
sys.path.append(os.environ['PEN_SYSTEST'])
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs')
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs/operd')

    
         
def vrf_list(vrf):
    vrf_list = re.split(": |, |\s", vrf)
    vrf_list.remove('VRFs')
    return(vrf_list)

def config_change_vrf_primary(vrf,dsm):
        router_ip = "192.168.68.128"
        r_username = "admin"
        r_password = "Pensando!2345"
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vrf ' + vrf)
        ssh.send_command_timing('dsm ' + dsm)
        ssh.disconnect()

def config_change_vrf_secondary(vrf,dsm):
        router_ip = "192.168.69.237"
        r_username = "admin"
        r_password = "Pensando!2345"
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vrf ' + vrf)
        ssh.send_command_timing('dsm ' + dsm)
        ssh.disconnect()

def config_vsx_dsm(command):
        router_ip = "192.168.68.128"
        r_username = "admin"
        r_password = "Pensando!2345"
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vsx ')
        ssh.send_command_timing('vsx-sync ' + command)
        ssh.disconnect()

def config_vsx_no_dsm(nocommand):
        router_ip = "192.168.68.128"
        r_username = "admin"
        r_password = "Pensando!2345"
        ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
        ssh.config_mode(config_command='configure term')
        ssh.send_command_timing('vsx ')
        ssh.send_command_timing('no ' + 'vsx-sync ' + nocommand)
        ssh.disconnect()
        

def parse_flows(flows):
    tcp_count = 0
    udp_count = 0
    icmp_count = 0
    others_count = 0
    f = flows.splitlines()
    j = re.compile("^[0-9].*")
    flows = list(filter(j.match, f))
    print(flows)
    for i in flows:
        flows_split = re.split("(\s+)", i)
        print(flows_split)
        if flows_split[14] == "TCP":
            tcp_count += 1
        elif flows_split[14] == "UDP":
            udp_count += 1
        elif flows_split[14] == "ICMP":
            icmp_count += 1
        else:
            others_count += 1
    return (tcp_count, udp_count, icmp_count, others_count)

class vrf_clitest_vsx_withsync(aetest.Testcase):

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_sync(self):
           router_ip = "192.168.68.128"
           r_username = "admin"
           r_password = "Pensando!2345"
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
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       print("configuring vsx sync dsm")
                       config_vsx_dsm("dsm")
                       print("VRF pod1 mapped to DSM1, changing to DSM2")
                       config_change_vrf_primary("pod1", "1/2")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       print("configuring vsx sync dsm")
                       config_vsx_dsm("dsm")
                       print("VRF pod1 mapped to DSM2, changing to DSM1")
                       config_change_vrf_primary("pod1", "1/1")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           
           else:
               print("No vrfs configured")
           
           assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
           assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           print("FLows in vrf pod1 match before and after change to DSM mapping")
           print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
           print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           ssh.disconnect()

        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

class vrf_clitest_vsx_withoutsync_primary(aetest.Testcase):

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_withoutsync_primary(self):
           router_ip = ["192.168.68.128"]
           r_username = "admin"
           r_password = "Pensando!2345"
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
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       print("unconfiguring vsx sync dsm")
                       config_vsx_no_dsm("dsm")
                       print("VRF pod1 mapped to DSM1, changing to DSM2")
                       config_change_vrf_primary("pod1", "1/2")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       print("unconfiguring vsx sync dsm")
                       config_vsx_no_dsm("dsm")
                       print("VRF pod1 mapped to DSM2, changing to DSM1")
                       config_change_vrf_primary("pod1", "1/1")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           
           else:
               print("No vrfs configured")
           
           assert udp_count_pre == udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
           assert icmp_count_pre == icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           print("FLows in vrf pod1 match before and after change to DSM mapping")
           print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
           print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           ssh.disconnect()


        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()

class vrf_clitest_vsx_withoutsync_secondary(aetest.Testcase):

        @aetest.test
        def get_elba_pretest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_pretest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
  
        @aetest.test 
        def vrf_cli_flow_test_vsx_withoutsync_secondary(self):
           router_ip = ["192.168.69.237"]
           r_username = "admin"
           r_password = "Pensando!2345"
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
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                       print("VRF pod1 mapped to DSM1, changing to DSM2")
                       config_change_vrf_secondary("pod1", "1/2")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           if test_vrf2:
               vrfs_temp = test_vrf2.group()
               vrf1 = vrf_list(vrfs_temp)
               print(vrf1)
               if "pod1" in vrf1:
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/2", expect_string="$")
                       cli_output_flow_pre_change = ssh.send_command("pdsctl show flow")
                       tcp_count_pre, udp_count_pre, icmp_count_pre, others_count_pre = parse_flows(cli_output_flow_pre_change)
                       ssh.send_command("exit",expect_string="$")
                       #print("unconfiguring vsx sync dsm")
                       #config_vsx_no_dsm("dsm")
                       print("VRF pod1 mapped to DSM2, changing to DSM1")
                       config_change_vrf_secondary("pod1", "1/1")
                       
                       time.sleep(60)
                       ssh.send_command("diag", expect_string="#")
                       ssh.send_command("diag dsm console 1/1", expect_string="$")
                       cli_output_flow_post_change = ssh.send_command("pdsctl show flow")
                       tcp_count_post, udp_count_post, icmp_count_post, others_count_post = parse_flows(cli_output_flow_post_change)
                       ssh.send_command("exit",expect_string="$")
           
           else:
               print("No vrfs configured")
           
           assert udp_count_pre != udp_count_post, print("UDP flows count not matching : \n Pre: " + str(udp_count_pre) + "\n Post: " + str(udp_count_post))
           assert icmp_count_pre != icmp_count_post, print("ICMP flows count not matching : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           assert others_count_pre == others_count_post, print("Other flows count not matching : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           print("FLows in vrf pod1 match before and after change to DSM mapping")
           print("UDP flows count : \n Pre: "+str(udp_count_pre)+ "\n Post: " + str(udp_count_post))
           print("ICMP flows count  : \n Pre: " + str(icmp_count_pre) + "\n Post: " + str(icmp_count_post))
           print("Other flows count  : \n Pre: " + str(others_count_pre) + "\n Post: " + str(others_count_post))
           ssh.disconnect()

        @aetest.test
        def get_elba_posttest_flow_output_elba1(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/1", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()
        @aetest.test
        def get_elba_posttest_flow_output_elba2(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
                ssh.send_command("diag", expect_string="#")
                ssh.send_command("diag dsm console 1/2", expect_string="$")
                cli_output_flow = ssh.send_command("pdsctl show flow")
                print(cli_output_flow)
                ssh.disconnect()

        @aetest.test
        def get_show_output(self):
            router_ip = ["192.168.68.128", "192.168.69.237"]
            r_username = "admin"
            r_password = "Pensando!2345"
            for ip in router_ip:
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': ip, 'username': r_username, 'password': r_password})
           
                cli_output1 = ssh.send_command("show dsm 1/1 vrf")
                cli_output2 = ssh.send_command("show dsm 1/2 vrf")
                cli1 = ssh.send_command("show run vsx")

                print(cli_output1)
                print(cli_output2)
                print(cli1)
                ssh.disconnect()
