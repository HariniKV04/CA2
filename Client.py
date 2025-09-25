import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

CLIENT_KEY = "client.key"
CLIENT_CERT = "client.crt"
CA_CERT = "ca.crt"

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

with socket.create_connection((HOST, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname='localhost') as ssock:
        try:
            while True:
                msg = input("[Client] Message: ").encode()
                if not msg:
                    break
                ssock.sendall(msg)

                data = ssock.recv(1024)
                if not data:
                    break
                print(f"[Client] Received: {data.decode()}")
        except KeyboardInterrupt:
            print("[Client] Connection closed.")
