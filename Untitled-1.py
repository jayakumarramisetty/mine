                    
                    
                    
import re
cli_output1='''
Distributed Services Modules 1/2
====================================
VRFs: pod1

Distributed Services Modules 1/1
====================================
VRFs: Demo-VRF-01'''                    
test_vrf1 = re.search("VRFs.*", cli_output1)
print(test_vrf1)