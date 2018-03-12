"""
This is to test multiple connection.
The program runs 100 iterations containing
100 tcp connections each, and returns the
time (in seconds) it took to run that iteration.
"""

import sys
import subprocess
import random
import time

procs = []#contains list of processes
for j in range(100):
    t = time.time()
    for i in range(100):
        #client.py contains the client side script
        proc = subprocess.Popen([sys.executable, 'client.py'])
        #proc.wait(random.randrange(1, 10))
        #print(proc)
        procs.append(proc)
    print("Iteration - ", j, " took ", time.time() - t, " seconds")
#print(procs)
