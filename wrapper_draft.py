data2 ={
      "name": "tes_scale",
      "description": "rule1_policy",
      "priority": "",
      "rules": ""
      
    }
#print(data2)
n=10
while n<=20:
    data1 =       {
          "description": "rule2_sample",
          "name": "rules2",
          "proto-ports": 
            [{
              "ports": str(n),
              "protocol": "tcp"
            }]
          ,
          "action": "permit",
          "from-ip-addresses": [
            "192.168.0.1"
          ],
          "to-ip-addresses": [
            "192.168.1.1"
          ]
        }
      



    print(data1)

    data3=[data1]
    data2["rules"]=(data3)
    print(data2)
    n=n+1

#data2["rules"]=(data3)





    
    


    #data3={data1}

    #print(data3)





      



#for k,v in data1.items():
    #print (v)
    #while n<=20:
        #n=n+1






#print(data2)

