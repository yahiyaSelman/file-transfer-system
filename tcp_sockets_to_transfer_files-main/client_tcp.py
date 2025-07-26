import socket
import os
import time

HOST = "192.168.8.115"
PORT = 4455

def connect_server(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        filepath = input("File Path: ")

        if filepath == 'quit()':
            break

        try:
            file = open(filepath, 'rb')
        except FileNotFoundError:
            print("File not found. Try again.")
            continue

        filename = os.path.basename(filepath)
        s.sendall(filename.encode('utf-8'))

        data = s.recv(1024)
        if data.decode('utf-8') != 'OK':
            print("The client can't send filename for server.'")
            continue

        while True:
            data = file.read(1024)
            if not data:
                break
            s.sendall(data)

        time.sleep(0.1)
        s.sendall(b'FILE_TRANSFER_COMPLETE')
        time.sleep(0.1)

        file.close()

    s.close()

connect_server(HOST, PORT)
