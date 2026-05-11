import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

HOST = '127.0.0.1'
PORT = 65432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

public_key_data = client.recv(1024)
public_key = RSA.import_key(public_key_data)

print("Received RSA Public Key")

aes_key = get_random_bytes(32)

cipher_rsa = PKCS1_OAEP.new(public_key)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)

client.send(encrypted_aes_key)

print("AES key sent securely")


message = b"Hello Server!"

cipher_aes = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(message)

client.send(cipher_aes.nonce)
client.send(tag)
client.send(ciphertext)


nonce = client.recv(16)
tag = client.recv(16)
ciphertext = client.recv(1024)

cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
reply = cipher_aes.decrypt_and_verify(ciphertext, tag)

print("Server reply:", reply.decode())

client.close()