# Libraries
import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading

# Constants
format = logging.Formatter('%(message)s')
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"
host_key = paramiko.RSAKey(filename=r'C:\Users\raksh\Downloads\honeynet\server.key')

# Loggers and Logging Files
ip_logger = logging.getLogger('iplogger')
ip_logger.setLevel(logging.INFO)
ip_handler = RotatingFileHandler('ip.log', maxBytes=2000, backupCount=5)
ip_handler.setFormatter(format)
ip_logger.addHandler(ip_handler)

cmd_logger = logging.getLogger('cmdlogger')
cmd_logger.setLevel(logging.INFO)
cmd_handler = RotatingFileHandler('commands.log', maxBytes=2000, backupCount=5)
cmd_handler.setFormatter(format)
cmd_logger.addHandler(cmd_handler)

# Emulated Shell
def emu_shell(channel, client_ip):
    channel.send(b'secured-system$\n')
    command = b""
    while True:
        char = channel.recv(1)
        if not char:
            break
        
        command += char
        channel.send(char)
        
        if char == b'\r':
            command = command.strip()
            if command == b'exit':
                response = b'\nbye-bye\n'
                channel.send(response)
                channel.close()
                return
            elif command == b'pwd':
                response = b'\n\\user\\local\\\n'
            elif command == b'ls':
                response = b'\nfile1.txt  file2.txt  directory1\n'
            elif command == b'cd':
                response = b'\n'
            elif command == b'cd ..':
                response = b'\n'
            elif command == b'ls -l':
                response = b'\n-rw-r--r-- 1 user group 1234 file1.txt\n-rw-r--r-- 1 user group 5678 file2.txt\n'
            elif command == b'mkdir newdir':
                response = b'\n'
            elif command == b'rmdir newdir':
                response = b'\n'
            elif command == b'touch newfile.txt':
                response = b'\n'
            elif command == b'cp file1.txt file2.txt':
                response = b'\n'
            elif command == b'mv file1.txt file3.txt':
                response = b'\n'
            elif command == b'rm file2.txt':
                response = b'\n'
            elif command == b'cat file1.txt':
                response = b'\nThis is the content of file1.txt\n'
            elif command == b'grep searchterm file1.txt':
                response = b'\nsearchterm: found in file1.txt\n'
            elif command == b'echo Hello':
                response = b'\nHello\n'
            elif command == b'clear':
                response = b'\n'
            elif command == b'whoami':
                response = b'\nuser\n'
            elif command == b'uname -a':
                response = b'\nLinux localhost 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 09:54:23 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux\n'
            elif command == b'top':
                response = b'\nTop command output\n'
            elif command == b'ps aux':
                response = b'\nUSER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND\nuser 1234 0.0 0.0 1234 1234 ? S 12:34:56 /bin/bash\n'
            elif command == b'ifconfig':
                response = b'\neth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500\n'
            elif command == b'ssh user@host':
                response = b'\nThe authenticity of host \'host (192.168.1.1)\' can\'t be established.\n'
            elif command == b'passwd':
                response = b'\nChanging password for user.\n'
            else:
                response = b'\ncommand not found\n'
            
            # Log the command with client IP
            cmd_logger.info(f"{client_ip}: {command.decode()}")  # Log command
            channel.send(response)
            channel.send(b'secured-system$ ')
            command = b""

# SSH Server + Sockets
class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password

    def check_channel_request(self, kind, channel):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        if self.input_username and self.input_password:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        return True

def client_handle(client, addr, username, password):
    client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")
    
    # Log IP address of incoming connection
    ip_logger.info(f"Connection from: {client_ip}")  # Log IP Address
    
    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip=client_ip, input_username=username, input_password=password)
        transport.add_server_key(host_key)
        transport.start_server(server=server)
        channel = transport.accept(100)
        if channel is None:
            print("Connection timed out")
            return
        standard_banner = "Welcome to the most secured system in the world\r\n\r\n"
        channel.send(standard_banner.encode())
        emu_shell(channel, client_ip=client_ip)
        
    except Exception as error:
        print(error)
        print("System got corrupted")
    finally:
        try:
            transport.close()
        except Exception as error:
            print(error)
            print("Error closing transport")

# Provision SSH-Based Honeypot
def honeypot(address, port, username, password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(100)
    print(f'SSH server is listening on port {port}.')
    while True:
        try:
            client, addr = socks.accept()
            ssh_honey_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
            ssh_honey_thread.start()
        except Exception as error:
            print(error)

honeypot('127.0.0.1', 2223, 'admin', 'password')
