import socket
import socketserver
import time
import selectors

class MyTCPServer(socketserver.TCPServer):
    timeout = 15
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    allow_reuse_address = False

    #Variables defined in this class
    selectObject = selectors.DefaultSelector()
    keep_running = True

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass
        #self.__is_shut_down = threading.Event()
        #self.__shutdown_request = False

        # localSocket overrrides the accept method to return NON Blocking socket for a new connection
        self.socket = socket.socket(self.address_family, self.socket_type)
        if bind_and_activate:
            try:
                self.socket.bind(self.server_address)
                self.socket.listen(self.request_queue_size)
                self.socket.setblocking(False)
                print("TCP server running on PORT#", server_address[1])
            except:
                self.socket.close()
                raise
    def getSocketName(self):
        return self.socket

    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """

        #Below code-line returns a key.
        #Inputs are -> which socket to monitor, which type of event do you want to monitor, third is optional
        try:
            self.selectObject.register(self.socket, selectors.EVENT_READ, self.accept)
        except ValueError:
            print("events is invalid")
        except KeyError:
            print("fileobj is already registered")
        except OSError:
            print("fileobj is closed or otherwise is unacceptable to the underlying system call if a system call is made")
        while self.keep_running:#Server waiting for incoming request
            print('waiting for I/O')
            for key, event in self.selectObject.select():#Runs ans return (key, mask) when there is something to read at server port
                callback = key.data#data is "accept()" method, event is Read/Write event(1 for READ)
                callback(key.fileobj, event)#key.fileobj is server socket

    def accept(self, sock, mask):
        "Callback for new connections"
        new_connection, addr = sock.accept()
        print('accept({})'.format(addr))
        #new_connection.setblocking(False)
        #new_connection.settimeout(15)
        self.selectObject.register(new_connection, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        try:
            data = conn.recv(1024)
            if data:
                outData=MyTCPServer.reverse(data)
                print('sending', repr(outData), 'to', conn)
                conn.send(outData)  # Hope it won't block
            else:
                pass#commented because we do not want to terminate connection from server
                """
                print('closing', conn)
                self.selectObject.unregister(conn)
                conn.close()
                """
        except:
            print("Connection closed by client")
            self.selectObject.unregister(conn)
            conn.close()
    @staticmethod
    def reverse(inputString):
        inputString = inputString[::-1]
        return inputString
"""
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            outString=self.reverse(self.data)
            print(outString)
            self.request.sendall(outString)

    def reverse(self, inputString):
        inputString = inputString[::-1]
        return inputString
"""
if __name__ == "__main__":
    HOST, PORT = "localhost", 8888

    # Server listening on port 8888
    with MyTCPServer((HOST, PORT), """MyTCPHandler""") as server:
        server.serve_forever()
