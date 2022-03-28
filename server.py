# server.py

import sender
import receiver
import socket
import sys
import threading

def main():

    IP=input("Please input the IP: ")
    PORT=eval(input("Please input the Port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    IP_PORT=(IP,PORT)
    
    sock.bind(IP_PORT) 
    while(True):
        option=input("Please input your option: send/receive/close: ")
        if option=="send":
            lock=threading.Lock()
            lock.acquire()
            filename=input("Please input the filepath you want to send: ")
            RECEIVER_IP=input("Please input the Receiver's IP: ")
            RECEIVER_PORT=eval(input("Please input the Receiver's Port: "))
            RECEIVER_IP_PORT=(RECEIVER_IP,RECEIVER_PORT)
            lock.release()
            
            send_thread=threading.Thread(target=sender.send,args=(sock,filename,IP_PORT,RECEIVER_IP_PORT))
            send_thread.start()
            send_thread.join()
            
        elif option=="receive":
            lock=threading.Lock()
            lock.acquire()
            filename=input("Please input the filepath you want to save: ")
            lock.release()
            receive_thread=threading.Thread(target=receiver.receive,args=(sock,filename,IP_PORT))
            receive_thread.start()
            receive_thread.join()
        elif option=="close":
            sock.close()
            break
        else:
            continue

if __name__=='__main__':
    main()