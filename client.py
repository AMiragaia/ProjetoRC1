import socket

ip_addr = "198.142.128.2"
tcp_port = 5005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_addr, tcp_port))

request1 = "Request number one"
request2 = "Request with fifty bytes of data                  "
request3 = "Request with ninety bytes of data                                                         "
requestQ = "quit"

while True:
    client_input = input("Press ENTER to send a request (or Q to quit):")
    if client_input.lower() == 'q':
        client.send(requestQ.encode())
        break
    elif client_input == '':
        client_choice = input("1 - Send 18 Bytes\n2 - Send 50 Bytes\n3 - Send 90 Bytes\n")
        if client_choice == '1':    
            client.send(request1.encode())
        if client_choice == '2':
            client.send(request2.encode())
        if client_choice == '3':
            client.send(request3.encode())
        data = client.recv(1024)
        print(data.decode())
client.close()