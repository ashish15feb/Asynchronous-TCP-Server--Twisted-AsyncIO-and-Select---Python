import socket
import sys
server_ip, server_port = "127.0.0.1", 8888
data = "Hello! How are you?"

# TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.settimeout(15)
try:
# Establish connection to server and send data
    client_socket.connect((server_ip, server_port))
    client_socket.sendall(data.encode())
    #print(client_socket)

    # Read data from server and close the connection
    received = client_socket.recv(1024)
    while(len(received)>0):
        print(len(received)," bytes received. Message is -> ",received)
        received = client_socket.recv(1024)

except ConnectionRefusedError:
    print("Server not running")
except ConnectionResetError:
    print("An existing connection was forcibly closed by the remote host")
    client_socket.shutdown(socket.SHUT_RDWR)
    client_socket.close()

#print ("Bytes Sent:     {}".format(data))
#print ("Bytes Received: {}".format(received.decode()))