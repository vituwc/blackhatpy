import socket
import threading

# ------------------------------------------------------------------------
# Author: vituwc
# Github: https://github.com/vituwc
# Purpose: Educational purposes and learning cybersecurity and Python
# Status: Beginner in cybersecurity and penetration testing
#
# Disclaimer: The code in this repository is for study and learning purposes 
# only. I am a beginner in the field of penetration testing and network 
# security. If you're using any of the scripts, make sure to do so in a 
# legal and ethical manner, with proper authorization. I am following 
# "Black Hat Python - 2nd Edition" as a reference for many of these concepts.
# ------------------------------------------------------------------------

IP = '0.0.0.0'  # Listen on all available network interfaces
PORT = 9998  # Port to listen on

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    server.bind((IP, PORT))  # Bind the server to IP and PORT
    server.listen(5)  # Start listening with a backlog of 5 connections
    print(f"[ * ] Listening on {IP}:{PORT}")

    while True:
        client, address = server.accept()  # Accept incoming connections
        print(f"[ * ] Accepted connection from {address[0]}:{address[1]}")
        
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)  # Receive up to 1024 bytes from the client
        
        # Fixed syntax error: changed `("utf-8")` to `('utf-8')`
        print(f"[ + ] Received: {request.decode('utf-8')}") 
        
        sock.send(b"ACK")  # Send acknowledgment to the client

if __name__ == '__main__':
    main()
