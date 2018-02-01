#!/usr/bin/env python

import socket
import protocol_client as pc

TCP_IP = '127.0.0.1'
TCP_PORT = 5006
BUFFER_SIZE = 1024

def send_to_server(sckt, msg):
    sckt.sendto(msg.encode(), (TCP_IP,TCP_PORT))
    print("> Client:", msg)

def save_file(content, fname):
    new_file = open('./files/'+fname, "wb")
    new_file.write(content)
    new_file.close()
    print("< Server: File sent")

def receive_file(sckt, fs):
    num = fs//BUFFER_SIZE + 1
    data = b''
    i=1
    while i < num:
        part = sckt.recv(BUFFER_SIZE)
        data += part
        i += 1
    return data

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print('Connection created with server: ')
print('Server IP: ', TCP_IP)
print('Server PORT: ', TCP_PORT)
print('\nPress CTRL-C at any moment to stop the send\n')

# Ask for files list
send_to_server(s, pc.START)
data = s.recv(BUFFER_SIZE)
files = data.decode()
print("< Server: This is the list of files available:")
print(files)

# Ask for specific file
send_to_server(s, pc.SEND_FILE)
filename = input("Type the filename that you desire: ")
send_to_server(s, filename)

# Receive file
data = s.recv(BUFFER_SIZE)
file_start = data.decode()
print("< Server:", file_start)
file_size = int(file_start.split(":")[1])
send_to_server(s, pc.OK)
data = receive_file(s, file_size)
save_file(data, filename)

# End connection
send_to_server(s, pc.END)
s.close()
