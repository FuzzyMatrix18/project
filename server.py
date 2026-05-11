import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

HOST = '127.0.0.1'
PORT = 65432

key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

print("RSA keys generated")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server listening...")

conn, addr = server.accept()
print("Connected by", addr)

conn.send(public_key.export_key())

encrypted_aes_key = conn.recv(256)

cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

print("AES Key received and decrypted:", aes_key)

nonce = conn.recv(16)
tag = conn.recv(16)
ciphertext = conn.recv(1024)

cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
message = cipher_aes.decrypt_and_verify(ciphertext, tag)

print("Decrypted message from client:", message.decode())

# Send encrypted reply
reply = b"Hello Client, message received!"

cipher_aes = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(reply)

conn.send(cipher_aes.nonce)
conn.send(tag)
conn.send(ciphertext)

conn.close()