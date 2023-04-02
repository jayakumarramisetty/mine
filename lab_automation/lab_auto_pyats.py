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
import getpass
import datetime
from ats import aetest
sys.path.append(os.environ['PEN_SYSTEST'])
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs')
sys.path.append(os.environ['PEN_SYSTEST'] + '/lib/protoc_libs/operd')

import yaml
input_params = '''
swi_ip_stdln: ["192.168.68.128"]
swi_ip_vsx: ["10.9.8.33"]
swi_usr: "admin"
swi_pwd: "Pensando!2345"
iperf_ip: ["192.168.71.107", "192.168.70.178"]
iperf_usr: "root"
iperf_pwd: "docker"
t_vrf: "pod1"
line_port: ["31", "30"]
console_port: ["2031", "2030"]
'''


'''

username1 = "n "
password1 = " n"
destination_server1 = "n "
dst_file = "n "
src_file = "n "


print('sudo sshpass -p {} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}:{} {}'
                .format(password1,username1,destination_server1,dst_file,src_file))

'''
##getting system date 
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def system_time():
    parser = datetime.datetime.now() 
    return parser.strftime("%d-%m-%Y_%H:%M:%S")

time_stamp = system_time()

input_params = yaml.safe_load(input_params)



def copy_firmware_to_switch(password,username,destination_server,dst_file_loc,src_file_loc):
            for ip in input_params['swi_ip_vsx']:
                router_ip = ip
                r_username = input_params['swi_usr']
                r_password = input_params['swi_pwd']
                print("\n\nConnecting Device ",ip)
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                print("\n\nConnected Device ",ip)
                time.sleep(1)
                ssh.send_command("start-shell", expect_string=r"~\$" )
                print('entered into shell')
                print('transferring file---->')
                output1=ssh.send_command('sudo sshpass -p {} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}:{} {}'
                    .format(password, username, destination_server, dst_file_loc, src_file_loc), expect_string=r"~\$")
                print(output1)
                print('File successfully copied to {} location'.format(src_file_loc))
                print(system_time())
                ssh.disconnect()

def reload_switch_cli(boot_partition):
            for ip in input_params['swi_ip_vsx']:
                router_ip = ip
                r_username = input_params['swi_usr']
                r_password = input_params['swi_pwd']
                print("\n\nConnecting Device ",ip)
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                print("\n\nConnected Device ",ip)
                time.sleep(1)
                output = ssh.send_command("write memory" , expect_string='(?!^)#')
                print(output)
                output1 = ssh.send_command("boot system {}".format(boot_partition) , expect_string=r'Continue (y/n)?')
                print(output1)
                ssh.write_channel("y")
                print('Switch reboot successfully')
                ssh.disconnect()

def clear_console_line(line):
    ssh = netmiko.ConnectHandler(**{'device_type': 'cisco_ios_telnet', 'ip': "10.9.9.171" , 'username': "admin", 'password': "N0isystem$"})
    print(ssh.find_prompt())
    for i in range(5):
        output=ssh.send_command("clear line {}".format(line), expect_string='[confirm]')
        o2=ssh.send_command("\n", expect_string=r'#')
        print(output)
        print(o2)
        print('console line cleared {} times'.format(i))
        time.sleep(3)
    ssh.disconnect()




    
def reboot_from_svos(port):
   
    '''Reboot device if switch is stuck in console
    :param console_details: Details of switch
    :return:'''
    svos_flag = False
    ssh = netmiko.ConnectHandler(**{'device_type': 'generic_termserver_telnet', 'ip': "10.9.9.171" , 'username': "admin", 'password': "N0isystem$" , 'port' : port, 'default_enter' : '\r'})
    #output = ssh.send_command()
    print(ssh.find_prompt())
    if 'ServiceOS' in ssh.find_prompt():
        print('switch enter to svos mode')
        try:
            ssh.write_channel('reboot\n')
            print('rebooted switch from svos')
        except Exception as e:
            print('failed')
        svos_flag = True
    ssh.disconnect()
    return svos_flag


class check_rechability(aetest.Testcase):
        must_pass=True
        @aetest.test
        def check_rechability(self):
            for ip in input_params['swi_ip_vsx']:
                    response = os.system('ping -c 1 ' + ip)
                    assert response == 0
                    print("=>"*500 , 'DSS with ip address ' + ip + " is rechable","=>"*500  )
                    
        
class lab_automation_dss(aetest.Testcase):
        
        @aetest.test
        def command_check(self,password,username,destination_server,dst_file_loc,src_file_loc):
              print('sudo sshpass -p {} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}:{} /fs/nos/{}.swi'
                    .format(password, username, destination_server, dst_file_loc, src_file_loc))
        
        

        @aetest.test
        def get_version(self):
            for ip in input_params['swi_ip_vsx']:
                router_ip = ip
                r_username = input_params['swi_usr']
                r_password = input_params['swi_pwd']
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                print("\n\n===============================Connected Device ===========================>",ip)
                cli_output1 = ssh.send_command("show version")
                time.sleep(2)
                cli_output2 = ssh.send_command("show images")
                time.sleep(2)
                print("============show version==============")
                print(cli_output1)
                print("===========show images===============")
                print(cli_output2)
                ssh.disconnect()

        @aetest.test
        def get_config_backup(self):
            for ip in input_params['swi_ip_vsx']:
                router_ip = ip
                r_username = input_params['swi_usr']
                r_password = input_params['swi_pwd']
                print("\n\nConnecting Device ",ip)
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                print("\n\nConnected Device ",ip)
                time.sleep(1)
                print ("Reading the running config ")
                config_output = ssh.send_command("show running-config")
                time.sleep(5)
                filename=ip+ "_config"+'_'+time_stamp+".txt"
                saveconfig=open(filename,'w+')
                print("Writing Configuration to file")
                saveconfig.write(config_output)
                saveconfig.close()
                time.sleep(2)
                ssh.disconnect()
                print ("Configuration saved to file" + "==============>",filename)

        @aetest.test
        def copy_firmware_to_switch(self,password,username,destination_server,dst_file_loc,src_file_loc):
                        for ip in input_params['swi_ip_vsx']:
                            router_ip = ip
                            r_username = input_params['swi_usr']
                            r_password = input_params['swi_pwd']
                            print("\n\nConnecting Device ",ip)
                            ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                            print("\n\nConnected Device ",ip)
                            time.sleep(1)
                            ssh.send_command("start-shell", expect_string=r"~\$" )
                            print('entered into shell')
                            print('transferring file---->')
                            output1=ssh.send_command('sudo sshpass -p {} scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {}@{}:{} /fs/nos/{}.swi'
                                .format(password, username, destination_server, dst_file_loc, src_file_loc), expect_string=r"~\$", read_timeout=600)
                            print(output1)
                            print('File successfully copied to {}.swi location'.format(src_file_loc))
                            print(system_time())
                            ssh.disconnect()

        @aetest.test
        def reload_switch_cli_both(self,src_file_loc):
            reload_switch_cli(src_file_loc)
            print('Waiting for the switch to comeup')
            time.sleep(90)
            
            for ip in input_params['swi_ip_vsx']:
                    max_count = 10
                    count = 0
                    status = False
                    while count < max_count:
                        output = True if os.system("ping -c 1 " + ip) is 0 else False
                        if output:
                            logging.info('Switch came up successfully')
                            print('switch cameup successfully')
                            status = True
                            break
                        else:
                            count += 1
                            logging.info('Switch did not came up yet checking again')
                            time.sleep(60)
                    if status==False: 
                        print('Checking if switch has entered SVOS conolse')
                        clear_console_line(30)
                        svos_status = reboot_from_svos(2030)
                        if svos_status:
                                    print('Machine had entered service OS console, box is rebooted now')
                                    max_count = 10
                                    count = 0
                                    status = False
                                    while count < max_count:
                                        output = True if os.system("ping -c 1 " + ip) is 0 else False
                                        if output:
                                            print('switch cameup successfully')
                                            status = True
                                            break
                                        else:
                                            count += 1
                                            logging.info('Switch did not came up yet checking again')
                                            time.sleep(60)
                                    if status==False:
                                        print('switch failed to come up')
                                    #else:
                                        #print('switch failed to come up')
                        else:
                            print('switch failed to come up')

            time.sleep(60)
            print('wait for 60=========>')


        @aetest.test
        def get_version_post(self):
            for ip in input_params['swi_ip_vsx']:
                router_ip = ip
                r_username = input_params['swi_usr']
                r_password = input_params['swi_pwd']
                ssh = netmiko.ConnectHandler(**{'device_type': 'hp_procurve', 'ip': router_ip, 'username': r_username, 'password': r_password})
                print("\n\n===============================Connected Device ===========================>",ip)
                cli_output1 = ssh.send_command("show version")
                time.sleep(2)
                cli_output2 = ssh.send_command("show images")
                time.sleep(2)
                print("============show version==============")
                print(cli_output1)
                print("===========show images===============")
                print(cli_output2)
                ssh.disconnect()
                          
                                          

                            
                            
