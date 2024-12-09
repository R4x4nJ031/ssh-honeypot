# ssh-honeypot
SSH Honeypot GitHub Manual
Overview
This project is an emulated SSH server designed to simulate a real SSH environment to attract and monitor malicious activity. It logs incoming IP addresses and commands executed during interactions with the server. It can be used as a part of a cybersecurity training lab or a honeypot in production for detecting and mitigating attacks.

Prerequisites
Before setting up the SSH honeypot, make sure you have the following tools and software installed:

Python 3.x: Required for running the honeypot script.

Install Python from python.org.
Paramiko Library: A Python implementation for SSH. This library is used for handling SSH connections.

Install Paramiko via pip:
bash
Copy code
pip install paramiko
Logging: Python's built-in logging module is used to capture incoming IP addresses and the commands executed by attackers.

SSH Key: A valid RSA private key for the server. This key is used for the server's authentication process and should be placed in the directory where the honeypot script is located.

Generate the RSA key if you don't already have one using:
bash
Copy code
ssh-keygen -t rsa -b 2048 -f server.key
Project Structure
Here’s an overview of the project structure:

bash
Copy code
/honeypot
├── honeypot.py              # The main honeypot script
├── server.key               # The private RSA key for the server
├── ip.log                   # Log file for tracking incoming IP addresses
├── commands.log             # Log file for tracking commands executed
└── README.md                # Documentation for the project
Setup and Configuration
1. Clone the Repository
Start by cloning the repository containing the honeypot to your local machine.

bash
Copy code
git clone https://github.com/R4x4nJ031/ssh-honeypot.git
cd ssh-honeypot
2. Edit Configuration
The main configuration file is embedded within the honeypot.py script. If you want to customize the honeypot's behavior (e.g., changing the SSH port, username, or password), edit the following lines in honeypot.py:

SSH Port:

python
Copy code
honeypot('127.0.0.1', 2223, 'admin', 'password')
Replace 2223 with the desired port number on which you want to run the honeypot.

Username and Password: Update the default username and password in the script to match your configuration:

python
Copy code
honeypot('127.0.0.1', 2223, 'admin', 'password')
SSH Banner: If you'd like to modify the server's greeting banner, change the SSH_BANNER constant:

python
Copy code
SSH_BANNER = "SSH-2.0-MySSHServer_1.0"
Log File Location: The logs for the incoming IP addresses and executed commands are saved to ip.log and commands.log respectively. You can change their location by modifying the logging configuration:

python
Copy code
ip_handler = RotatingFileHandler('ip.log', maxBytes=2000, backupCount=5)
cmd_handler = RotatingFileHandler('commands.log', maxBytes=2000, backupCount=5)
3. Generate the RSA Key
If you don't already have an RSA private key for your honeypot, you can generate one using the following command:

bash
Copy code
ssh-keygen -t rsa -b 2048 -f server.key
The key will be stored in server.key, and you should place this file in the same directory as your honeypot script.

4. Run the Honeypot
To start the honeypot, simply run the following Python command:

bash
Copy code
python honeypot.py
This will start the SSH server listening on the specified address and port (default 127.0.0.1:2223). It will log incoming IP addresses to ip.log and commands executed by the attackers to commands.log.

SSH Command Emulation
The honeypot provides an emulated shell where malicious users can execute various commands. The following commands are supported:

exit: Closes the session.
pwd: Prints the working directory.
ls: Lists the files in the current directory.
cd: Changes the current directory.
mkdir: Creates a new directory.
rmdir: Removes a directory.
touch: Creates a new file.
cp: Copies a file.
mv: Moves a file.
rm: Removes a file.
cat: Displays the contents of a file.
echo: Outputs text to the screen.
top: Displays system information.
ps aux: Displays processes.
ifconfig: Displays network interface details.
ssh user@host: Simulated SSH connection prompt.
passwd: Changes the user’s password (simulated).
When any of these commands are executed, the output is sent back to the user, and the command is logged to commands.log.

Logging Information
1. IP Address Logging
Every time a connection is made to the honeypot, the IP address of the connecting client is logged into ip.log. The IP is logged in the following format:

csharp
Copy code
Connection from: <IP_ADDRESS>
2. Command Logging
All commands executed by the attacker are logged into commands.log. The log contains the client’s IP address followed by the command they entered:

php
Copy code
<client_ip>: <command>
Running the Honeypot as a Background Service
If you'd like to run the honeypot as a background service or daemon, you can use a tool like nohup or set it up as a systemd service (Linux only).

Example using nohup:
Run the honeypot in the background with nohup:

bash
Copy code
nohup python honeypot.py &
This will allow the honeypot to continue running in the background even after closing the terminal.

Example using systemd (Linux):
Create a systemd service file for your honeypot:

bash
Copy code
sudo nano /etc/systemd/system/ssh-honeypot.service
Add the following configuration:

ini
Copy code
[Unit]
Description=SSH Honeypot

[Service]
ExecStart=/usr/bin/python /path/to/honeypot.py
Restart=always

[Install]
WantedBy=multi-user.target
Enable and start the service:

bash
Copy code
sudo systemctl enable ssh-honeypot
sudo systemctl start ssh-honeypot
Troubleshooting
1. Port Already in Use
If you encounter the error Address already in use, ensure that no other process is running on the same port. You can check which process is using the port by running:

bash
Copy code
sudo lsof -i :<port_number>
Replace <port_number> with the port you're using (e.g., 2223).

2. Permission Denied Errors
If you receive a Permission denied error when attempting to run the honeypot, ensure that the RSA key has the correct permissions and that you're running the script with the appropriate privileges.

To fix the key permissions, run:

bash
Copy code
chmod 600 server.key
Security Considerations
Since this honeypot is designed to simulate a real SSH server, it is important to secure the system where it is deployed. Running a honeypot on a public server can attract malicious users, so make sure to isolate the honeypot in a secure environment.

Additionally, ensure that:

The honeypot runs in a controlled network environment.
It's monitored for unusual activity.
It's regularly updated to handle potential vulnerabilities.
Conclusion
This SSH honeypot is a powerful tool for cybersecurity research, penetration testing, or just experimenting with SSH and honeypot technology. The logs will give you valuable insight into what attackers are trying to do. Make sure to configure and monitor it properly to make the most out of the project.

If you have any questions or need assistance, feel free to open an issue or contribute to the project on GitHub.
