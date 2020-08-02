import socket               # Import socket module
from numpy import asarray
from numpy import save
from numpy import load
import csv
RSSIth1=50 
port1 = 55550                
port2 = 55551 
port3 = 55552 
def ap(dt,port):
	s=socket.socket()
	host = socket.gethostname()
	s.connect((host, port))
	s.sendall(str(dt).encode("utf-8"))
	s.close()  

# def aps(port):
# 	s1 = socket.socket() 
# 	host = socket.gethostname()
# 	s1.connect((host, port))
# 	r=int(s1.recv(1024))
# 	s1.close()
# 	return r 

# rssi1=aps(port1)
# rssi2=aps(port2)
# rssi3=aps(port3)
data="c" 

# print("AP1 RSSI: ",rssi1)
# print("AP2 RSSI: ",rssi2)
# print("AP3 RSSI: ",rssi3)
# AP=[rssi1,rssi2,rssi3]
# #print(AP)
# save('rssi.npy',AP)
rssi1=int(input("ap1: "))
rssi2=int(input("ap2: "))
rssi3=int(input("ap3: "))

AP=[rssi1,rssi2,rssi3]
print(AP)
save('rssi.npy',AP)
BestAP=AP.index(max(AP))
if AP[BestAP] >= RSSIth1 :
	#dt=[BestAP,AP[BestAP]]
	save("active.npy",BestAP)	

if BestAP==0:
	ap(data,port1)
elif BestAP==1:
	ap(data,port2)
else:
	ap(data,port3)

