import sys
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

# HEX_FILTER is a string containing all printable characters, non-printable characters are replaced by '.'
HEX_FILTER = ''.join(
    [(len(repr(chr(1))) == 3) and chr(i) or '.'
     for i in range(256)])

# Function to display content in hexadecimal format with a translation to printable characters
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()  # If 'src' is in bytes, decode it to string
    
    results = list()  # List to store the hexdump result
    for i in range(0, len(src), length):
        word = str(src[i:i+length])  # Extract a "word" (substring) of content up to the 'length' limit
        printable = word.translate(HEX_FILTER)  # Replace non-printable characters with '.'
        hexa = ''.join([f'{ord(c):02X}' for c in word])  # Convert each character to its hexadecimal value
        hexwidth = length * 3  # Define the width of the hexadecimal field based on word length
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')  # Format the result and append to the list
    
    if show:
        for line in results:  # If 'show' is True, print each line of the result
            print(line)
    else:
        return results  # Otherwise, return the results for later use

# Function to receive data from a connection
def receive_from(connection):
    buffer = b""  # Initialize an empty buffer to store received data
    connection.settimeout(10)  # Set a timeout of 10 seconds for the connection
    
    try:
        while True:
            data = connection.recv(4096)  # Try to receive up to 4096 bytes of data
            if not data:  # If no data is received, break the loop
                break
            
            buffer += data  # Append the received data to the buffer
    except Exception as e:
        print("Error ", e)  # Print the error if something goes wrong
        pass

    return buffer  # Return the buffer containing the received data

# Function to handle incoming request packets (for example, packet modification like fuzzing, auth testing, finding creds, etc.)
def request_handler(buffer):
    return buffer  # Return the buffer (could be modified before returning)

# Function to handle outgoing response packets (for example, packet modification like fuzzing, auth testing, finding creds, etc.)
def response_handler(buffer):
    return buffer  # Return the buffer (could be modified before returning)

# Function to handle the proxy operations (not implemented in the original code, just a placeholder)
# def proxy_handler(client_socket, remote_host, remote_port, receive_first)

# Function for the server loop where the communication between the client and the remote server happens
# def server_loop(local_host, local_port, remote_host, remote_port, receive_first)

# Main function, responsible for starting the script
def main():
    # Check if the necessary arguments were provided when running the script
    if len(sys.argv[1:]) < 5:
        print("Usage: .tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]")
        print("Example: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # Assign the arguments passed into local variables
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # Check if the 'receivefirst' argument was passed as True or False
    if "True" in sys.argv[5]:
        receive_first = True
    else:
        receive_first = False

    # Start the server loop with the provided parameters
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

# Check if the script is being executed directly
if __name__ == '__main__':
    main()
