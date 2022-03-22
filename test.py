import crc16
import packet
import sender
import timer
import time
import threading
import socket
import server
import UDT
import random
import sys


print("ssdasfsf")
scale=50
start = time.perf_counter()
while(1):
    if (time.perf_counter()-start) % 1 ==0:
        print(scale)