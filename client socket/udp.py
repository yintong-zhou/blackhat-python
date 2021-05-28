import socket

target_host = "127.0.0.1"
target_port = 9997

# create a socket object - we change the socket type to SOCK_DGRAM
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data - passing in the data and the server you want to send the data to
client.sendto(b"AAABBBCCC",(target_host,target_port))

# receive some data - Because UDP is a connectionless protocol, there is no call to connect() beforehand. The last step is to call recvfrom() to receive UDP data back.
data, addr = client.recvfrom(4096) 

print(data.decode())
client.close()