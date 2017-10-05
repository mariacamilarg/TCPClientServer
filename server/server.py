#!/usr/bin/env python

import socket
import protocol_server as ps

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 64  # Normally 1024, but we want fast response

def send_to_client(cnn, msg):
    conn.send(msg.encode())
    print("> SERVER:", msg)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for connections...")

# conn is a new socket object usable to send and receive data on the connection
# addr is the address bound to the socket on the other end of the connection
conn, addr = s.accept()
print('Connection created:', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    data_d = data.decode()
    print("< CLIENT:", data_d)

    if data_d == ps.START:
        files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
        send_to_client(conn, str(files))
    elif data_d == ps.SEND_FILE:
        filename = conn.recv(BUFFER_SIZE)
        filename_d = filename.decode()
        print("< CLIENT:", filename_d)
        desired_file = "File..."
        desired_file_size = len(desired_file.encode('utf-8'))
        send_to_client(conn, ps.START_OF_FILE + ":" + str(desired_file_size))
        print("< CLIENT:", conn.recv(BUFFER_SIZE).decode())
        send_to_client(conn, desired_file)
    elif data_d == ps.END:
        break
    elif not data:
        break

conn.close()
