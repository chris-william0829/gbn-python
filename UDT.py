#UDT.py

import random
import time
import socket

class UDT:
    def __init__(self,lost,err):
        random.seed(time.time())    #random seed
        self.LOST_PROB=lost         #set lost prob and err prbo
        self.ERR_PROB=err
    # Send a packet across the unreliable channel
    # Packet may be lost
    def send(self,packet, sock, addr):
        if random.random()<self.ERR_PROB:
            packet=self.make_error(packet)
        if random.random()>self.LOST_PROB:
            sock.sendto(packet, addr)
        return

    # Receive a packet from the unreliable channel
    def recv(self,sock):
        packet, addr = sock.recvfrom(1024)
        return packet, addr


    def sendack(self,ack,sock,addr):
        ack_bytes = ack.to_bytes(4, byteorder = 'little', signed = True)
        if random.random()>self.LOST_PROB:
            sock.sendto(ack_bytes, addr)
        return

    def recvack(self,sock):
        ack_bytes, addr = sock.recvfrom(1024)
        ack= int.from_bytes(ack_bytes, byteorder = 'little', signed = True)
        return ack, addr

    def make_error(self,packet):
        ErrData=b''
        for i in range(len(packet)-8):
            byte=random.randint(65,121)
            ErrData=ErrData+byte.to_bytes(1, byteorder = 'little', signed = True)
        return packet[0:8]+ErrData
    