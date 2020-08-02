import socket               # Import socket module
import random
s1 = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 55550                # Reserve a port for your service.
s1.bind((host, port))        # Bind to the port
print("AP1 Running")
s1.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s1.accept()     # Establish connection with client.
   print ("Got connection from", addr)
   output = random.randint(40,100)
   #print("Rssi: ",output)

   c.sendall(str(output).encode("utf-8"))
   rec=c.recv(1024)
   if (rec==b'c'):print("BanC is Connected")
   elif(rec!=b''):print("BanC is Connected"," and recived hertrate: ",int(rec))

   c.close()                # Close the connection