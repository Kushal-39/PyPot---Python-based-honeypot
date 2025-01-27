import socket
import paramiko
import threading
import os
import json

class SSH_Server(paramiko.ServerInterface):
    def check_auth_password(self,username,password):
        print(f"Username: {username} Password: {password}")
        return paramiko.AUTH_FAILED
        
        
    def check_auth_publickey(self,username,key):
        return paramiko.AUTH_FAILED
    
    def log_attempt(self,username,password):
        log_entry = {
            "username": username,
            "password": password,
            "timestamp": os.path.getctime(self.log_file)
        }
        with open(self.log_file, "a") as log_file:
            log_file.write(json.dumps(log_entry))
            log_file.write("\n")
    
def handle_connection(client_sock,server_key):
    transport= paramiko.Transport(client_sock)
    transport.add_server_key(server_key)
    ssh= SSH_Server()
    transport.start_server(server=ssh)
        
def main():
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(('0.0.0.0',22))
    server_socket.listen(100)
    
    server_key=paramiko.RSAKey.generate(2048)
    log_file="ssh_attempts.log"
    
    while True:
        client_sock,addr=server_socket.accept()
        print(f"Connection from {addr[1]} to {addr[0]} established")
        t= threading.Thread(target=handle_connection,args=(client_sock,server_key))
        t.start()
        
if __name__=="__main__":
    main() 
    