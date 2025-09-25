import socket
import subprocess

HOST = "127.0.0.1"
PORT = 65432

PRIVATE_KEY = "private.pem"  
PUBLIC_KEY = "public.pem"  

def run(cmd):
    subprocess.run(cmd, check=True)


run(["openssl", "genrsa", "-out", PRIVATE_KEY, "4096"])
run(["openssl", "rsa", "-pubout", "-in", PRIVATE_KEY, "-out", PUBLIC_KEY])

def encrypt_message(message, output_path="message.enc"):
    with open("message.txt", "w") as f:
        f.write(message)
    run([
        "openssl", "pkeyutl",
        "-encrypt",
        "-pubin",
        "-inkey", PUBLIC_KEY,
        "-in", "message.txt",
        "-out", output_path
    ])

def sign_message(message_file="message.txt", signature_file="message.sig"):
    run([
        "openssl", "dgst", "-sha256",
        "-sign", PRIVATE_KEY,
        "-out", signature_file,
        message_file
    ])

message = "Hello, secure world!"

with open("message.txt", "w") as f:
    f.write(message)


sign_message("message.txt", "message.sig")
encrypt_message(message, "msg.enc")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    with open("msg.enc", "rb") as f:
        encrypted_bytes = f.read()
    with open("message.sig", "rb") as f:
        signature_bytes = f.read()

    s.sendall(len(encrypted_bytes).to_bytes(4, 'big') + encrypted_bytes + signature_bytes)
    print("Encrypted message and signature sent!")
