import socket

host = "127.0.0.1"
port = 9998

# create a socket object - We first create a socket object with the AF_INET and SOCK_STREAM parameters.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client - The AF_INET parameter indicates we’ll use a standard IPv4 address or hostname, and SOCK_STREAM indicates that this will be a TCP client.
client.connect((host, port))

# send some data - We then connect the client to the server and send it some data as bytes
client.send(b"Hello world!")

# receive some data - The last step is to receive some data back and print out the response and then close the socket.
response = client.recv(4096)

print(response.decode)
client.close()