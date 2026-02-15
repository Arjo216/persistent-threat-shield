import socket
import threading
import paramiko
import logging
import time
from datetime import datetime
from colorama import Fore, Style, init

# Initialize Color for cool terminal output
init(autoreset=True)

# Configure Logging (The Audit Trail)
logging.basicConfig(
    filename='pts_audit_trail.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Generate a dummy host key (Required for SSH)
HOST_KEY = paramiko.RSAKey.generate(2048)

class ChameleonServer(paramiko.ServerInterface):
    """
    The Deception Interface. 
    It pretends to be a legitimate SSH server but records everything.
    """
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # STRATEGY: We let EVERYONE in. That's the trap.
        log_msg = f"🛑 INTRUSION ATTEMPT: IP={self.client_ip} | User={username} | Pass={password}"
        print(f"{Fore.RED}{log_msg}{Style.RESET_ALL}")
        logging.info(log_msg)
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    # --- NEW METHODS ADDED BELOW TO FIX PTY ERROR ---
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

def handle_connection(client, addr):
    client_ip = addr[0]
    print(f"{Fore.YELLOW}[!] Incoming Connection from {client_ip}... Engaged.")
    
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = ChameleonServer(client_ip)
        
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            print("[-] SSH Negotiation Failed.")
            return

        # Wait for authentication
        channel = transport.accept(20)
        if channel is None:
            print("[-] No channel.")
            return

        # Wait for the user to ask for a shell (Fixes the PTY error)
        server.event.wait(10)
        if not server.event.is_set():
            print("[-] Client never asked for a shell.")
            channel.close()
            return

        print(f"{Fore.GREEN}[+] Intruder Captured in Shell Environment.")
        channel.send("Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-1035-aws x86_64)\r\n\r\n")
        channel.send("System Maintenance in progress. Activity is monitored.\r\n")
        
        # The Infinite Loop of Deception
        # The Infinite Loop of Deception
        while True:
            # --- NEW: CHECK FOR KILL ORDER ---
            try:
                with open("blacklist.txt", "r") as f:
                    if client_ip in f.read():
                        print(f"{Fore.RED}⚡ EXECUTIONER: Banning {client_ip} by AI Order.")
                        channel.send(f"\r\n{Fore.RED}⛔ AEGIS SYSTEM: THREAT DETECTED. CONNECTION TERMINATED.\r\n")
                        channel.close()
                        break
            except FileNotFoundError:
                pass # No bans yet
            # ---------------------------------

            channel.send("admin@pts-secure:~# ")
            command = ""
            
            # Non-blocking receive loop so we can keep checking the blacklist
            while not command.endswith("\r"):
                if channel.closed: break 
                if channel.recv_ready():
                    transport = channel.recv(1024)
                    channel.send(transport)
                    command += transport.decode("utf-8")
                else:
                    time.sleep(0.1) # Wait briefly
                    # Re-check blacklist while waiting for user input
                    try:
                        with open("blacklist.txt", "r") as f:
                            if client_ip in f.read():
                                channel.close()
                                break
                    except: pass
            
            if channel.closed: break
            
            command = command.strip()
            if command == "exit":
                break
            
            # Log the command
            print(f"{Fore.CYAN}[Attacker Command] {command}")
            logging.info(f"CMD EXEC: {client_ip} -> {command}")
            
            # Fake Responses
            if command == "ls":
                channel.send("\r\nsecret_db.sql  passwords.txt  config.yaml\r\n")
            elif command == "whoami":
                channel.send("\r\nroot\r\n")
            elif command == "pwd":
                channel.send("\r\n/root\r\n")
            else:
                channel.send(f"\r\nbash: {command}: command not found\r\n")

        channel.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")

def start_trap(port=2223):
    print(f"{Fore.BLUE}🛡️ PERSISTENT THREAT SHIELD: TRAP ACTIVE")
    print(f"{Fore.BLUE}Listening on 0.0.0.0:{port}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(100)
    
    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(client, addr)).start()

if __name__ == "__main__":
    start_trap()