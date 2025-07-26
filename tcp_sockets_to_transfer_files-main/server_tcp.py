""" import socket
import os
import datetime
import locale

HOST = "192.168.8.115"
PORT = 4455

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

def open_server(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    with open('serverlog.txt', 'a') as log:
            date = datetime.datetime.now()
            format_date = date.strftime('[%d/%m/%Y, %H:%M:%S]')
            log.write(f'{format_date} TCP Server wait connection on {PORT} port...\n')

    print('TCP Server wait connection on %d port...' % (PORT))

    try:
        while True:
            conn, addr = s.accept()
            ip, port = addr
            
            with open('serverlog.txt', 'a') as log:
                date = datetime.datetime.now()
                format_date = date.strftime('[%d/%m/%Y, %H:%M:%S]')
                log.write(f"{format_date} Connected estabilished with {ip}:{port}\n")

            print(f"Connected estabilished with {ip}:{port}")
            
            filename = conn.recv(1024).decode('utf-8')

            if filename:
                conn.send('OK'.encode('utf-8'))

                current_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(current_dir, 'transfer', filename)

                with open(file_path, 'wb') as arq:
                    while True:
                        data = conn.recv(1024)
                        if data == b'FILE_TRANSFER_COMPLETE':
                            break
                        arq.write(data)
                
                with open('serverlog.txt', 'a') as log:
                    date = datetime.datetime.now()
                    format_date = date.strftime('[%d/%m/%Y, %H:%M:%S]')
                    log.write(f'{format_date} File {filename} saved\n')
                    
                print('File receive and saved')

    except KeyboardInterrupt:
        with open('serverlog.txt', 'a') as log:
            date = datetime.datetime.now()
            format_date = date.strftime('[%d/%m/%Y, %H:%M:%S]')
            log.write(f'{format_date} Server closed.\n')
        print('Server closed')

    conn.close()

open_server(HOST, PORT)
 """
""" def handle_client(conn, addr):
    ip, port = addr
    log_message(f"Connected established with {ip}:{port}")
    print(f"Connected established with {ip}:{port}")
    
    try:
        filename = conn.recv(1024).decode('utf-8')
        
        if filename:
            conn.send('OK'.encode('utf-8'))
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            transfer_dir = os.path.join(current_dir, 'transfer')
            os.makedirs(transfer_dir, exist_ok=True)  # Ensure the directory exists
            
            file_path = os.path.join(transfer_dir, filename)
            
            with open(file_path, 'wb') as arq:
                while True:
                    data = conn.recv(1024)
                    if data == b'FILE_TRANSFER_COMPLETE':
                        break
                    arq.write(data)
            
            log_message(f"File {filename} saved")
            print('File received and saved')
    except Exception as e:
        log_message(f"Error with client {ip}:{port} - {str(e)}")
        print(f"Error with client {ip}:{port} - {str(e)}")
    finally:
        conn.close()
        log_message(f"Connection closed with {ip}:{port}")
        print(f"Connection closed with {ip}:{port}") """
        
        
import socket
import os
import datetime
import locale
import threading

HOST = "192.168.8.115"
PORT = 4455

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

def log_message(message):
    with open('serverlog.txt', 'a') as log:
        date = datetime.datetime.now()
        format_date = date.strftime('[%d/%m/%Y, %H:%M:%S]')
        log.write(f"{format_date} {message}\n")



def handle_client(conn, addr):
    ip, port = addr
    log_message(f"Connected established with {ip}:{port}")
    print(f"Connected established with {ip}:{port}")
    
    try:
        while True:  # Keep the connection alive
            filename = conn.recv(1024).decode('utf-8')

            if filename == 'quit()':  # Client signals to terminate the connection
                log_message(f"Client {ip}:{port} requested to close the connection.")
                print(f"Client {ip}:{port} requested to close the connection.")
                break

            if filename:
                conn.send('OK'.encode('utf-8'))
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                transfer_dir = os.path.join(current_dir, 'transfer')
                os.makedirs(transfer_dir, exist_ok=True)  # Ensure the directory exists
                
                file_path = os.path.join(transfer_dir, filename)
                
                with open(file_path, 'wb') as arq:
                    while True:
                        data = conn.recv(1024)
                        if data == b'FILE_TRANSFER_COMPLETE':
                            break
                        arq.write(data)
                
                log_message(f"File {filename} saved")
                print(f"File {filename} received and saved")
    except Exception as e:
        log_message(f"Error with client {ip}:{port} - {str(e)}")
        print(f"Error with client {ip}:{port} - {str(e)}")
    finally:
        conn.close()
        log_message(f"Connection closed with {ip}:{port}")
        print(f"Connection closed with {ip}:{port}")

def open_server(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)  # Allow up to 5 pending connections
    log_message(f"TCP Server waiting for connections on port {PORT}...")
    print(f"TCP Server waiting for connections on port {PORT}...")

    try:
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True  # Ensure the thread closes when the main program exits
            client_thread.start()
    except KeyboardInterrupt:
        log_message("Server closed.")
        print("Server closed")
    finally:
        s.close()

open_server(HOST, PORT)
