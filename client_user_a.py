import random
import socket
import sys
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
    

def start_client(server_ip,server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, int(server_port)))
        print(f"Connected to server {server_ip}:{server_port}")
        key_ba = client.recv(1024).decode('utf-8')
        print("Recieved Key-BA From User-B : {}".format(key_ba))    
        key_ab = str(random.randint(10**15, (10**16)-1)) 
        print("Key-AB Generated :", key_ab)
        client.send(key_ab.encode('utf-8'))
        while True:
            message = input("Type A Message To User B: ")
            if message.lower() == 'exit':
                break
            print("User-A Message In PlainText : {}".format(message))
            cypher_text = call_ascon_encrypt(key_ab,message)
            print("User-A Message In CypherText : {}".format(cypher_text))
            client.send(cypher_text)
            server_response = client.recv(1024)
            message_b = server_response
            print("User-B Message In CypherText : {}".format(message_b))
            print(f"--------- Decrypting Using Key-BA --------- ")
            decypher_text = call_ascon_decrypt(key_ba,message_b)
            print("User-B Message In PlainText : {}".format(decypher_text))
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("Closing connection From User B")
        client.close()

if __name__ == "__main__":
    server_addr=input("Please Enter Server Ip Address :")
    server_prt=input("Please Enter The Port No :")
    if server_addr == "" or server_prt == ""  or server_addr == " " or server_prt == " " or server_addr is None or server_prt is None:
        print("Missing Inputs. Please Input Values Correctly.")
        sys.exit(1)
    else:
        start_client(server_addr,server_prt)
