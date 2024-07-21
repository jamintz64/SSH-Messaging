# SSH-Messaging
# Secure Messaging Client-Server System
## Overview
This repository contains a client-server system that enables secure messaging between two users, User-A and User-B, using the Ascon-128 encryption algorithm.

## Files
### client.py
This file contains the client-side code that establishes a connection to the server and enables secure messaging with User-B.
The client generates a random key (Key-AB) and sends it to the server.
The client encrypts messages using the Ascon-128 algorithm with the Key-AB, nonce, and associated data.
The client decrypts responses from the server using the Key-BA received from the server.
### server.py
This file contains the server-side code that accepts connections from clients and enables secure messaging with User-A.
The server generates a random key (Key-BA) and sends it to the client.
The server decrypts messages from the client using the Key-AB received from the client.
The server encrypts responses to the client using the Key-BA.
## Usage
### Running the Client
Run python client.py in a terminal.
Enter the server's IP address and port number when prompted.
Enter messages to send to User-B.
### Running the Server
Run python server.py in a terminal.
Enter the server's IP address and port number when prompted.
The server will start listening for incoming connections.
## Dependencies
ascon library for Ascon-128 encryption algorithm
socket library for network communication
threading library for handling multiple client connections on the server
## Note
This is a basic implementation of a secure messaging system and should not be used for production purposes without further security auditing and testing.
The Ascon-128 encryption algorithm is used for demonstration purposes only and may not be suitable for all use cases.
