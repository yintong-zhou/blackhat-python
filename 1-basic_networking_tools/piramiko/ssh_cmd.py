# pip install paramiko (http://www.paramiko.org/)(https://github.com/paramiko/paramiko/)

import paramiko
import getpass

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()

    # set the policy to accept the SSH key for the SSH server we’re connecting to and make the connection
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    # run the command that we passed in the call to the ssh_command function
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())
    
if __name__ == '__main__':
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ') or '192.168.1.100'
    port = input('Enter port or <CR>: ') or 2222
    cmd = input('Enter command or <CR>: ') or 'id'

    # execute
    ssh_command(ip, port, user, password, cmd)