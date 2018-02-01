#!/usr/bin/env python

import os, socketserver
import protocol_server as ps

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        BUFFER_SIZE = 64
        files_sizes = {'tiny.txt':184, 'small.txt':5242880, 'medium.txt':20971520, 'big.txt':52428800}

        def send_to_client(cnn, msg):
            cnn.send(msg.encode())
            print("> Server:", msg)

        # self.request is the TCP socket connected to the client
        conn = self.request
        print('Connection created with client: ')
        print(conn)
        print()

        while True:
            data = conn.recv(BUFFER_SIZE)
            data_d = data.decode()
            print("< Client:", data_d)

            if data_d == ps.START:
                files = os.listdir("./files/")
                send_to_client(conn, str(files))
            elif data_d == ps.SEND_FILE:
                filename = conn.recv(BUFFER_SIZE)
                filename_d = filename.decode()
                print("< Client:", filename_d)
                desired_file_size = files_sizes[filename_d]
                desired_file = open('./files/'+filename_d, 'rb') #open in binary
                send_to_client(conn, ps.START_OF_FILE + ":" + str(desired_file_size))
                print("< Client:", conn.recv(BUFFER_SIZE).decode())
                conn.sendall(desired_file.read())
                print("> Server: File sent")
            elif data_d == ps.END:
                break
            elif not data:
                break

if __name__ == "__main__":

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5006

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((TCP_IP, TCP_PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("Waiting for connections...")
        server.serve_forever()
