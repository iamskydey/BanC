import socket               # Import socket module
from numpy import asarray
from numpy import save
from numpy import load
import csv

s1 = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port1 = 55550                # Reserve a port for your service.
port2 = 55551 
port3 = 55552
def ap(dt,port):
	s1.connect((host, port))
	s1.sendall(str(dt).encode("utf-8"))
	s1.close()  


data=load("data.npy")
print(data)

if data[0]==0:
	ap(data[1],port1)
elif data[0]==1:
	ap(data[1],port2)
else:
	ap(data[1],port3)


