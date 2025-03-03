import socket

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

target_host = "127.0.0.1"
target_port = 80

# Create a UDP socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data to the server
client.sendto(b"This is test data", (target_host, target_port))

# Receive some data from the server
data, addr = client.recvfrom(4096)  # Receive up to 4096 bytes
print(f"Received: {data.decode()}")  # Print the response
