import argparse  # Parses user arguments and displays options
import socket
import shlex
import subprocess
import sys
import textwrap
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

def execute(cmd):  # Executes the given command
    cmd = cmd.strip()  # Removes leading and trailing spaces from the command
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()  # Decodes and returns the command output

class NetCat:
    def __init__(self, args, buffer=None):
        """
        Initializes the NetCat class.
        :param args: Command-line arguments.
        :param buffer: Optional data to send immediately after connecting.
        """
        self.args = args
        self.buffer = buffer
        # Creates a TCP socket (IPv4)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows reusing the same address without waiting for timeout
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        """
        Determines whether to start in listener mode or to send data as a client.
        """
        if self.args.listen:
            self.listen() # Start listening for incoming connections
        else:
            self.send() # Connect to a remote host and send data

    def send(self):
        """
        Establishes a connection to the target and handles data transmission.
        If a buffer is provided, it sends the buffer first.
        Then, it continuously receives and sends data, simulating an interactive shell.
        """
        self.socket.connect((self.args.target, self.args.port))  # Connect to the target

        if self.buffer:
            self.socket.send(self.buffer)  # Send the initial buffer if provided

        try:
            while True:
                recv_len = 1
                response = ""

                # Receive data in chunks and assemble the response
                while recv_len:
                    data = self.socket.recv(4096)  # Receive up to 4096 bytes
                    recv_len = len(data)
                    response += data.decode()

                    if recv_len < 4096:  # Stop if we receive less than 4096 bytes (end of message)
                        break

                if response:
                    print(response)  # Print the received response
                    
                    # Get user input and send it to the target
                    buffer = input("> ")  
                    buffer += "\n"
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print("User terminated.")
            self.socket.close()
            sys.exit()

    def listen(self):
        """
        Binds the socket to the target address and port, then listens for incoming connections.
        Each new client connection is handled in a separate thread.
        """
        self.socket.bind((self.args.target, self.args.port))  # Bind to the specified address and port
        self.socket.listen(5)  # Start listening, allowing up to 5 queued connections

        while True:
            client_socket, _ = self.socket.accept()  # Accept an incoming connection
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()  # Handle the client in a new thread

        
    def handle(self, client_socket):
        """
        Handles an incoming client connection based on the specified mode:
        - Execute a command if --execute is provided.
        - Receive and save a file if --upload is provided.
        - Provide an interactive command shell if --command is provided.
        """
        
        # If execution mode is enabled, run the command and send the output
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())  # Fixed missing parentheses in encode()

        # If upload mode is enabled, receive and save the file
        elif self.args.upload:
            file_buffer = b''

            while True:
                data = client_socket.recv(4096)  # Receive file data in chunks
                if data:
                    file_buffer += data
                    print(len(file_buffer))  # Print received data size (debugging)
                else:
                    break  # Stop receiving when no more data is sent

            # Write received data to the specified file
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)

            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())  # Notify client that the file was saved

        # If command mode is enabled, provide an interactive shell
        elif self.args.command:
            cmd_buffer = b''

            while True:
                try:
                    client_socket.send(b' #> ')  # Prompt for command input

                    # Receive command input until a newline is found
                    while b'\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(64)

                    response = execute(cmd_buffer.decode())  # Execute the command

                    # Send the command output back to the client
                    if response:
                        client_socket.send(response.encode())

                    cmd_buffer = b''  # Reset buffer for next command

                except Exception as e:
                    print(f"Server killed: {e}")  # Print error message
                    self.socket.close()  # Close the server socket
                    sys.exit()  # Exit the program

# This structure is commonly used to ensure the script runs only when executed directly
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example usage:
            netcat.py -t 192.168.1.108 -p 5555 -l -c  # Start a command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt  # Upload a file
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"  # Execute a command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135  # Send text to server port 135
            netcat.py -t 192.168.1.108 -p 5555  # Connect to a server
        ''')
    )

    # Define the possible command-line arguments
    parser.add_argument('-c', '--command', action='store_true', help='Start a command shell')
    parser.add_argument('-e', '--execute', help='Execute a specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='Listen for incoming connections')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Port to connect/listen on')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='Target IP address')
    parser.add_argument('-u', '--upload', help='Upload a file')

    args = parser.parse_args()  # Parse command-line arguments

    # If listening mode is enabled, no buffer is needed
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()  # Read input from stdin for sending

    # Instantiate the NetCat class and start it
    nc = NetCat(args, buffer.encode())
    nc.run()