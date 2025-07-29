download the file and open your CMD prompt application.

open multiple instances of the CMD

run this for server: python3 server_tcp.py 

run this for client python3 client_tcp.py 

you can run multiple cmd windows for multiple clients. this simulates a multi-client environment which is a requirement of the project.

in the client_tcp.py file you can add the path to the file you want to send and press enter, then the file is sent to the repository's "transfer" folder.

example run client:

C:\Users\User\Desktop\tcp_sockets_to_transfer_files-main>python3 client_tcp.py_tcp.py File Path: C:\Users\User\Desktop\test1.txt File Path: C:\Users\User\Desktop\test2.txt File Path: quit()

finally you can kill the connection with the quit() command.
