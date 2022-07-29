from re import X


import random
rule ={}
for i in range (10):

    #k="permit" if (i%2==0) else "deny"
    act_list=["permit", "deny"]
    rule["ports"]= str(random.choice(act_list))
    rule["proto-ports"] = [ { "protocol": "tcp", "ports": str(random.randint(1024,65530)) } ]
    print(rule)