import socket
import subprocess

HOST = "127.0.0.1"
PORT = 65432

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, check=True, text=True)
    return result.stdout.strip()

KEY = run(["openssl", "rand", "-hex", "16"])
IV  = run(["openssl", "rand", "-hex", "16"])

print("[+] Generated Key:", KEY)
print("[+] Generated IV :", IV)

message = "Hello, AES world with random key & IV!"

with open("plain.txt", "w") as f:
    f.write(message)

subprocess.run([
    "openssl", "enc", 
    "-aes-128-cbc", "-e",
    "-in", "plain.txt",
    "-out", "cipher.bin",
    "-K", KEY,
    "-iv", IV
], check=True)

with open("cipher.bin", "rb") as f:
    encrypted = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((KEY + "\n" + IV + "\n").encode())
    s.sendall(encrypted)
    print("[+] Encrypted message sent with key & IV!")
