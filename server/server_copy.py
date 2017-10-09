#!/usr/bin/env python

import os, socket
import protocol_server as ps

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 64  # Normally 1024, but we want fast response
BACKLOG = 5 # Specifies the number of unaccepted connections that the system will allow before refusing new connections.

def handle_connection(thread_name, conn):

    def send_to_client(cnn, thrd, msg):
        cnn.send(msg.encode())
        print("> Server %d:"%thrd, msg)

    while True:
        data = conn.recv(BUFFER_SIZE)
        data_d = data.decode()
        print("< Client %d:"%thread_name, data_d)

        if data_d == ps.START:
            files = os.listdir("./files/")
            send_to_client(conn, thread_name, str(files))
        elif data_d == ps.SEND_FILE:
            filename = conn.recv(BUFFER_SIZE)
            filename_d = filename.decode()
            print("< Client %d:"%thread_name, filename_d)
            desired_file = "File..."
            desired_file_size = len(desired_file.encode('utf-8'))
            send_to_client(conn, thread_name, ps.START_OF_FILE + ":" + str(desired_file_size))
            print("< Client %d:"%thread_name, conn.recv(BUFFER_SIZE).decode())
            ssend_to_client(conn, thread_name, desired_file)
            # data = os.urandom(int(bytes))
            # sock.sendall(data)
        elif data_d == ps.END:
            break
        elif not data:
            break

    conn.close()



# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# re-use the port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# put listening socket into non-blocking mode
s.setblocking(0)

s.bind((TCP_IP, TCP_PORT))
s.listen(BACKLOG)

print("Listening on port %d ..." % TCP_PORT)

# read, write, exception lists with sockets to poll
rlist, wlist, elist = [s], [], []

while True:
    # block in select
    readables, writables, exceptions = select.select(rlist, wlist, elist)

    for sock in readables:
        if sock is s: # new client connection, we can accept now
            try:
                # conn is a new socket object usable to send and receive data on the connection
                # addr is the address bound to the socket on the other end of the connection
                conn, addr = s.accept()
                print('Connection created with client:', addr)
            except IOError as e:
                code, msg = e.args
                if code == errno.EINTR:
                    continue
                else:
                    raise
            # add the new connection to the 'read' list to poll
            # in the next loop cycle
            rlist.append(conn)
        else:
            # read a line that tells us how many bytes to write
            bytes_to_write = sock.recv(1024)
            if not bytes: # connection closed by client
                sock.close()
                rlist.remove(sock)
            else:
                print("Got request to send %s bytes. Sending them all... % bytes)
                # send them all
                # XXX: this is cheating, we should use 'select' and wlist
                # to determine whether socket is ready to be written to
                data = os.urandom(int(bytes))
                sock.sendall(data)
