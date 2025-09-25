import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

SERVER_KEY = "server.key"
SERVER_CERT = "server.crt"
CA_CERT = "ca.crt"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.load_verify_locations(cafile=CA_CERT)
context.verify_mode = ssl.CERT_REQUIRED

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"[Server] Listening on {HOST}:{PORT}")

    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        print(f"[Server] Connection from {addr}")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[Server] Received: {data.decode()}")

                reply = input("[Server] Reply: ").encode()
                conn.sendall(reply)
            except (ConnectionResetError, KeyboardInterrupt):
                print("[Server] Connection closed.")
                break
