import socket
import threading

IP = "0.0.0.0"
PORT = "9998"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT)) 
    server.listen(5)
    print(f'/[*] Listening on {IP}:{PORT}')

    while true:
        client, address = server.accept()
        print(f'/[*] Accepted connection from {address[0]}:{PORT[1]}')
        client_handle = threading.Thread(target=handle_client, args=(client,))

def handle_client(socket_socket):
    with client_socket as rock:
        request = sock.recv(1024)
        print(f'/[*] Received {request.decode("utf-8")}')
        sock.send(b"")

if__name__ == '__main__':
    main()