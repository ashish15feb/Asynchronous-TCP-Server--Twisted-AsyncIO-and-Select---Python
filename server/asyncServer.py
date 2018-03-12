#Asynchronous server using "asyncio"

import asyncio

#Handle for one comm channel
async def handle_reverse_string(reader, writer):
    # Here,"await" halts the execution of current process till there is some data to read, and moves to execute the next process
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    outString = reverse(message)
    #print("Send: %r" % outString)
    writer.write(outString.encode())
    await writer.drain()
    #print("Close the client socket")
    try:
        await asyncio.wait_for(reader.read(1024), timeout=15)
    except asyncio.TimeoutError:
        print("Timeout, closing connection")
        writer.close()

#String reversal function
def reverse(inputString):
    inputString = inputString[::-1]
    return inputString

#Start "ayncio" event loop
loop = asyncio.get_event_loop()
#Define co-routine having handle/task to execute again and again
coro = asyncio.start_server(handle_reverse_string, '127.0.0.1', 8888, loop=loop)
print("AsyncIO TCP server running on PORT#8888")

server = loop.run_until_complete(coro)
#loop.set_debug(enabled=True)
#print(coro,"---",server)

#print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()