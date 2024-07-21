import random
import sys
import socket
import threading
import ascon as ascon

nonce = "0000000000000000"
associateddata = "CS645/745 Modern Cryptography: Secure Messaging"

def call_ascon_encrypt(key,plaintext):
    key_bytes = key.encode('utf-8')
    nonce_bytes = nonce.encode('utf-8')
    associateddata_bytes = associateddata.encode('utf-8')
    plaintextdata_bytes=  plaintext.encode('utf-8')
    ascon_data_encrypt = ascon.ascon_encrypt(key_bytes, nonce_bytes, associateddata_bytes, plaintextdata_bytes, variant="Ascon-128")
    return ascon_data_encrypt

def call_ascon_decrypt(key,cyphertext):
    key_bytes = key.encode('utf-8')
    nonce_bytes = nonce.encode('utf-8')
    associateddata_bytes = associateddata.encode('utf-8')
    ascon_cypher=  cyphertext
    ascon_data_decrypt = ascon.ascon_decrypt(key_bytes, nonce_bytes, associateddata_bytes,ascon_cypher, variant="Ascon-128")
    return ascon_data_decrypt.decode('utf-8')
    
    
def handle_client(client_socket,key_ba):
    client_socket.send(key_ba.encode('utf-8'))
    key_ab = client_socket.recv(1024).decode('utf-8')
    print("Recieved Key-AB From User-A : {}".format(key_ab))    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Cypher Text Received From User-A: {data}")
            print(f"--------- Decrypting Using Key-AB --------- ")
            decypher_text = call_ascon_decrypt(key_ab,data)
            print("Decyphered Data : {}".format(decypher_text))
            message_to_send = input("Enter A Message To Send To User-A: ")
            print("User-B Message In PlainText : {}".format(message_to_send))
            cypher_text = call_ascon_encrypt(key_ba,message_to_send)
            print("User-B Message In CypherText : {}".format(cypher_text))
            client_socket.send(cypher_text)
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    print("Connection closed.")
    client_socket.close()

def start_server(server_ip,server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, int(server_port)))
    server.listen(5)
    print("Server Started: IP - {} On Port - {}".format(server_ip,server_port))
    key_ba = str(random.randint(10**15, (10**16)-1))
    print("Key-BA Generated :", key_ba)
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,key_ba))
        client_handler.start()

if __name__ == "__main__":
    server_addr=input("Please Enter Server Ip Address :")
    server_prt=input("Please Enter The Port No :")
    if server_addr == "" or server_prt == ""  or server_addr == " " or server_prt == " " or server_addr is None or server_prt is None:
        print("Missing Inputs. Please Input Values Correctly.")
        sys.exit(1)
    else:
        start_server(server_addr,server_prt)
