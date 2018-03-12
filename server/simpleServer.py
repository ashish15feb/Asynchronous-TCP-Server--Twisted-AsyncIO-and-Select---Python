# Asynchronous TCP Server using core socket functions and "Select"

import socket
import select
import string

#Function to send message to client
def send_data(sock, message):
    #Send message to client.
    #print("Connection is--",sock,"----Message is----", message)
    try:
        sock.send(message)
    except ConnectionResetError:
        print("Connection Closed by Client")
#Reverse the string received from server
def reverse(inputString):
    inputString = inputString[::-1]
    return inputString

if __name__ == "__main__":

    # List to keep track of socket descriptors
    CONNECTION_LIST = []

    # Create, bind and listening on the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8888))
    #server_socket.settimeout(15)
    server_socket.listen()
    # Add server socket to the list of readable connections
    print(server_socket)
    CONNECTION_LIST.append(server_socket)

    print("TCP server running on PORT#8888")

    while True:
        # Check which sockets are ready to be read using select.select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        #print(read_sockets, "---", write_sockets, "---", error_sockets)
        for sock in read_sockets:
            #print("Socket is :", sock)
            if sock == server_socket:
                # if true, new connection received on server_socket
                sockfd, addr = server_socket.accept()
                sockfd.setblocking(1)
                sockfd.settimeout(15)#Does not work because Python Doc -> "18.1.4.2. Timeouts and the accept method"
                CONNECTION_LIST.append(sockfd)
                #print(CONNECTION_LIST)
                #print(sockfd,"---",addr)
            else:# Data received from client, process it
                try:
                    # Sometimes TCP program closes abruptly resulting in "Connection reset by peer" exception
                    data = sock.recv(1024)
                    #print("Client Data ---  ",data)
                    if(len(data)==0):
                        send_data(sock, data)
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        continue
                except:
                    send_data(sock, ("Client (%s, %s) is offline" % addr).encode())
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

                #print("Client (%s, %s) connected" % addr)
                outString = reverse(data)
                #print("Received---", data)
                #print("Sending---", outString)
                send_data(sock, outString)
                #sock.close()
                #CONNECTION_LIST.remove(sock)

    server_socket.close()