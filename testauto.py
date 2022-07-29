import re
import netmiko



Feature Overview
Design
L2L Bridging
L2R Bridging
L2L Routing
L2R Routing
Caveats


This feature evaluates the policy evaluation changes between vlans(L2L and L2R routing case).

Symmetry/Consistency in the evaluation of the traffic between vlans is achieved through subnet based implementation(subnet-id replaced with vpc-id).

L2L Bridging(Both A and B)


Packet from host 1 reaches DSS.

On DSS in L2L switching(i.e here packet leaving server)  the egress policy(Tx-policy) is evaluated.

Packet switching happens and reaches the destination host 2.

→No evaluation will happen at destination because of same vlan

L2R Bridging(Both A and B)


Packet from host 1 reaches DSS-1 

On DSS-1 in L2R switching the egress policy(Tx-policy) is evaluated.

Packet will be switched to remote based on vxlan evpn or normal l2 through fabric.

Packet will reach the remote destination switch

On DSS-2 in L2R switching the Ingress policy(Rx-policy) is evaluated.

Packet reaches destination.

→Asymmetry in bridging will happen in the switching case.

L2L Routing (A release)


Packet from host1 reaches DSS (Pre-routed packet) and the routing happens.

On DSS in L2L routing the egress policy(Tx-policy) is evaluated for pre-routed packet 

Packet routing happens and  reaches destination host 2.


L2L Routing (B release)

Packet from host1 reaches DSS (Pre-routed packet)

On DSS in L2L routing the egress policy(Tx-policy) is evaluated for pre-routed packet and ingress policy(Rx-policy)is evaluated for post-routed packet.

Packet routing happens and reaches destination host 2.

L2R Routing (B release)

Packet from host1 reaches DSS (Pre-routed packet)

On DSS-1 in L2R routing the egress policy(Tx-policy) is evaluated for pre-routed packet.

Packet is sent to fabric(gateway) for routing.

Post routed packet will reach the remote DSS switch.

On DSS-2 in L2R routing the Ingress policy(Rx-policy) is evaluated for post-routed packet.

Packet reaches the destination.

→Symmetry and consistency will be achieved in both the routing cases.
→For L2R case , routing can also happen on both DSS-1 and DSS-2 ,and the symmetry of evaluation will not change.



Caveats (if any)



VLAN Redirect should be enabled for both the pre-routed as well as post-routed vlans for this to work,Otherwise, the traffic will be dropped, and would be treated as a misconfiguration.

ISL should be part of  all VLANs. Selective pruning of vlans on ISL cannot be supported.

Flows to and from an L3 interface to a policy enabled SVI will not be supported.

In Switching/Bridging case for L2L the evaluation happens only with egress policy whereas for L2R both ingress and egress policy get evaluated





Feature Overview
3-way handshake validation
FIN/RST sequence validation
Configuration and changes

This feature enables/implement two types of validations for TCP sessions in DSS by default.
Initial handshake validation
FIN/RST close sequence validation

With this feature enabled, the switch will validate the sequence number in packets with the flags (SYN/FIN/RST) and will drop the spoofed packets.

Glossary

P4 pipeline: P4 based processing unit inside the DSM

VPP: High performance packet processing stack where the first packet gets processed and the tcp state is maintained 



3-Way handshake validation

VPP maintains the state of TCP connection for both directions (i and r)

VPP will store the ISN of the initial SYN packet on i-flow and programs the session

Flow table entries would have the control plane re-direct bit set for the packets to continue to reach the VPP

This will happen till the VPP determines the session moves to EST state.

Transition to the EST state will happen only if the SYN+ACK and ACK match the respective ISN exchanged prior.

After this the connection tracking would be turned on in the session table.


FIN/RST Sequence validation


P4-pipeline will forward FIN/RST packets to the VPP for validation.

VPP will validate these packets based on the sequence number tracked in P4 for a particular direction of flow post EST.

In case of VSX deployments this validation will be done in both nodes and packet will be dropped if it fails to get validated.

RST packets will be sent back to P4-pipeline for processing after the validation.

VPP would keep track of the FINs exchanged.

When the second FIN packet is validated VPP would move to “Bi-Dir FIN seen” state; at this state P4 will treat the next ACK packet as a trigger for closing the session.



Configuration and changes

From netagent, connection tracking will be enabled by default for both VSX and non-VSX deployments

Session tracking is enabled once the sessions move to EST state from handshake.

Session tracking will help P4 pipeline to store and update the sequence number and acknowledgement number as it forwards packets of a session

Pdsagent related changes

Connection tracking in policy config is always enabled by netagent as PSM will not allow to disable it for both VSX and non-VSX deployments

Configuration and changes (contd..)


Full sync related changes

In prior releases a full resync is done when a TCP session goes down either because of ISL flap or other node reboot(in vsx setup).

In current release a selective resync is performed only for the sessions in established state.


TCP fast open is not supported in this release.

Other TCP options are not parsed only sequence number is tracked.

Simultaneous open is not supported as our policies can be asymmetric.



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





spec = importlib.util.spec_from_file_location("module.name", "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/netmiko.py")
netmiko = importlib.util.module_from_spec(spec)
spec.loader.exec_module(netmiko)



sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev  libncursesw5-dev xz-utils tk-dev


export PEN_SYSTEST="/home/jayk/vrfclitest/"

wget https://www.python.org/ftp/python/3.9.13/Python-3.9.13.tgz   









