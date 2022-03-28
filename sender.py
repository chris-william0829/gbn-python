#sender.py

import socket
import PDU
import UDT
import _thread
import timer
import sys
import packet
import crc16
import time
import threading
interval=1


ack_expected=0      #累计确认，只用维护一个
num_packets=0
send_timer=timer.timer(interval)
log_filename=""
mutex = _thread.allocate_lock()
UDTER=UDT.UDT(0.0001,0.0001)
def send(sock,filename,IP_PORT,RECEIVER_ADDR):
    global UDTER
    global mutex
    global ack_expected
    global num_packets
    global send_timer
    global log_filename
    log_filename=IP_PORT[0]+"_"+str(IP_PORT[1])+"_"+"log_file.txt"
    log_file=open(log_filename,"a+")
    file=open(filename,"rb")
    log_file.write("-------------------------------\n")
    log_file.write("%s send %s to %s\n" % (IP_PORT[0]+" "+str(IP_PORT[1]),filename,RECEIVER_ADDR[0]+" "+str(RECEIVER_ADDR[1])))
    packets=[]
    seq_num=0
    while True:
        data=file.read(512)    #data size
        if not data:
            break
        crc_num=crc16.crc16xmodem(data)    #calculate crc
        pdu=packet.make(seq_num,crc_num,data)    #make packet
        packets.append(pdu)
        seq_num+=1
    num_packets = len(packets)
    log_file.write("total %d packets(512bytes)\n" %(num_packets))
    print('I gots', num_packets)
    window_size=200
    next_frame_to_send=0

    #start receive ack thread
    THREAD=threading.Thread(target=receive,args=(sock,))
    THREAD.start()
    overtime_flag=0
    scale=50
    start = time.perf_counter()
    pre=start
    while ack_expected<len(packets):
        mutex.acquire()
        while next_frame_to_send<ack_expected+window_size:
            if next_frame_to_send>=len(packets):
                break
            #print('Sending packet', next_frame_to_send)
            if overtime_flag==0:
                log_file.write("%s: Send PDU=%d,STATUS=New,ACKed=%d to %s\n" % (time.ctime(),next_frame_to_send,ack_expected,str(RECEIVER_ADDR)))
            elif overtime_flag==1:
                log_file.write("%s: Send PDU=%d,STATUS=TO,ACKed=%d to %s\n" % (time.ctime(),next_frame_to_send,ack_expected,str(RECEIVER_ADDR)))
            send_timer.satrt(next_frame_to_send)
            UDTER.send(packets[next_frame_to_send],sock,RECEIVER_ADDR)
            next_frame_to_send+=1
        overtime_flag=0
        if send_timer.overtime(ack_expected):
            #print("overtime")
            overtime_flag=1
            next_frame_to_send=ack_expected
        
        if (time.perf_counter()-pre) > 1:
            pre=time.perf_counter()
            param = (int) (num_packets/50)
            i = (int) (next_frame_to_send/param)
            a='*' *i
            b='.'*(scale-i)
            c=(i/scale)*100
            dur=pre-start
            print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
        mutex.release()
    print("\nover")
    UDTER.send(packet.make_empty(), sock, RECEIVER_ADDR)
    log_file.write("send succeed\n") 
    log_file.write("-------------------------------\n\n\n")
    file.close()
    log_file.close()

def receive(sock):

    global mutex
    global ack_expected
    global num_packets
    
    while True:
        ack,_=UDTER.recvack(sock)

        #print('Got Ack',ack)
        if ack>=ack_expected:
            mutex.acquire()
            ack_expected=ack+1
           # print('ack_expected',ack_expected)
            mutex.release()
        if ack_expected>=num_packets:
            break

