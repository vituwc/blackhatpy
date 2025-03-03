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

target_host = "google.com"
target_port = 80

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client.connect((target_host, target_port))

# Send a properly formatted HTTP request
request = b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(request)

# Receive the response
response = client.recv(4096)

print(response.decode())  # Decode the response for readable text
