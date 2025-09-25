import socket
import subprocess
import os

HOST = "127.0.0.1"
PORT = 65432

PRIVATE_KEY = "private.pem" 
PUBLIC_KEY_CLIENT = "public.pem"

def run(cmd):
    subprocess.run(cmd, check=True)

def decrypt_message(input_path="received.enc", output_path="decrypted.txt"):
    run([
        "openssl", "pkeyutl",
        "-decrypt",
        "-inkey", PRIVATE_KEY,
        "-in", input_path,
        "-out", output_path
    ])
    with open(output_path, "r") as f:
        return f.read()

def verify_signature(message_file="decrypted.txt", signature_file="message.sig"):
    try:
        run([
            "openssl", "dgst", "-sha256",
            "-verify", PUBLIC_KEY_CLIENT,
            "-signature", signature_file,
            message_file
        ])
        return True
    except subprocess.CalledProcessError:
        return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(8192)

        msg_len = int.from_bytes(data[:4], 'big')
        encrypted_data = data[4:4+msg_len]
        signature_data = data[4+msg_len:]

        with open("received.enc", "wb") as f:
            f.write(encrypted_data)
        with open("message.sig", "wb") as f:
            f.write(signature_data)

        decrypted = decrypt_message("received.enc")
        print("Decrypted message:", decrypted)

        with open("decrypted.txt", "rb") as f:
            with open("message.sig", "rb") as sig_f:
                sig_bytes = sig_f.read()
        if verify_signature("decrypted.txt", "message.sig"):
            print("Signature verified successfully!")
        else:
            print("Signature verification failed!")
