
import socket
import threading
import signal
import sys
import struct

import socket

ip_addr = "198.142.128.2"
tcp_port = 5005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

import socket
import threading
import signal
import sys
import struct

total_recv = 0

def signal_handler(sig,frame):
    print('\nDone!')
    sys.exit(0)

def handle_client_connection(client_socket,address,sizes_dic):
    global total_recv
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            print("Client Request: ",request)
            if request == "quit":
                print("Client {}:{} has disconnected".format(address[0], address[1]))
                break
            if('{}:{}'.format(address[0],address[1]) in sizes_dic.keys()):
                sizes_dic['{}:{}'.format(address[0], address[1])] += len(request)
            else:
                sizes_dic['{}:{}'.format(address[0], address[1])] = len(request)

            total_recv += len(request)         
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            msg = "Server Hostname: {}\nServer local IP: {}\nClient Session Total Payload Bytes: {} B\nServer Session Total Bytes Received: {} B".format(hostname,ip,sizes_dic['{}:{}'.format(address[0],address[1])],total_recv).encode()
            client_socket.send(msg)
            print("Total Bytes Received: ",total_recv)
    except(socket.timeout, socket.error):
        print('Client {} error!'.format(address))
    finally:
        client_socket.close()

def main():
    signal.signal(signal.SIGINT,signal_handler)
    print('Press Ctrl+C to exit...')
    
    sizes_dic = {}

    ip_addr = "0.0.0.0"
    tcp_port = 5005
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_addr,tcp_port))
    server.listen(10) 

    while True:
         client_socket, address = server.accept()
         client_handler = threading.Thread(target=handle_client_connection,args=(client_socket,address,sizes_dic),daemon=True)
         client_handler.start()

if __name__ == '__main__':
    main()
