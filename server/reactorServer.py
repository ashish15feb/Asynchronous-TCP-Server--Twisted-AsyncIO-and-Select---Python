
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class reverse_string(Protocol):
    def dataReceived(self, data):
        #As soon as any data is received, write back reverse of input string.
        outString = self.reverse(data)
        self.transport.write(outString)
        #Disconnect
        #self.transport.loseConnection()

    #Function to reverse the input string
    def reverse(self, inputString):
        inputString = inputString[::-1]
        return inputString

def main():
    fact = Factory()
    fact.protocol = reverse_string
    reactor.listenTCP(8888, fact)
    print("Twisted TCP server running on PORT#8888")
    reactor.run()

if __name__ == '__main__':
    main()
