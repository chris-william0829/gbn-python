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

UDTER=UDT.UDT(0,0)
ip=("localhost",8080)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ip) 
cmd,addr=UDTER.recvcmd(sock)
print(cmd)
print(addr)
