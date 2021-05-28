# You might want to use your own TCP server when writing command shells or crafting a proxy
import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # we pass in the IP address and port we want the server to listen on, we tell the server to start listening, with a maximum backlog of connections set to 5
    server.bind((IP, PORT)) 
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # When a client connects, we receive the client socket in the client variable and the remote connection details in the address variable
        client, address = server.accept() 
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handle = threading.Thread(target=handle_client, args=(client,))

        # We then start the thread to handle the client connection, at which point the main server loop is ready to handle another incoming connection
        client_handle.start() 

# The handle_client function performs the recv() and then sends a simple message back to the client
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'/[*] Received {request.decode("utf-8")}')
        sock.send(b"")

if __name__ == '__main__':
    main()
    