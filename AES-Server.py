# aes_server.py
import socket
import subprocess

HOST = "127.0.0.1"
PORT = 65432

def run(cmd):
    subprocess.run(cmd, check=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[*] Listening on {HOST}:{PORT} ...")
    conn, addr = s.accept()
    with conn:
        print(f"[+] Connection from {addr}")

        received = b""
        while b"\n" not in received or received.count(b"\n") < 2:
            received += conn.recv(64)

        key, iv, rest = received.split(b"\n", 2)
        KEY = key.decode()
        IV = iv.decode()

        print("[+] Received Key:", KEY)
        print("[+] Received IV :", IV)

        with open("cipher.bin", "wb") as f:
            f.write(rest)
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                f.write(chunk)

        run([
            "openssl", "enc", "-aes-128-cbc", "-d",
            "-in", "cipher.bin",
            "-out", "decrypted.txt",
            "-K", KEY,
            "-iv", IV
        ])

        with open("decrypted.txt") as f:
            print("[+] Decrypted:", f.read())
