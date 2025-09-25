import subprocess

CA_KEY = "ca.key"
CA_CERT = "ca.crt"

def run(cmd):
    subprocess.run(cmd, check=True)

def create_key_and_csr(key_file, csr_file, subj):
    run(["openssl", "genrsa", "-out", key_file, "2048"])
    run(["openssl", "req", "-new", "-key", key_file, "-out", csr_file, "-subj", subj])

def sign_csr(csr_file, cert_file):
    run([
        "openssl", "x509", "-req",
        "-in", csr_file,
        "-CA", CA_CERT,
        "-CAkey", CA_KEY,
        "-CAcreateserial",
        "-out", cert_file,
        "-days", "365"
    ])

create_key_and_csr("server.key", "server.csr", "/C=US/ST=State/L=City/O=PSG/CN=server")
sign_csr("server.csr", "server.crt")

create_key_and_csr("client.key", "client.csr", "/C=US/ST=State/L=City/O=PSG/CN=client")
sign_csr("client.csr", "client.crt")

create_key_and_csr("tc.key", "tc.csr", "/C=US/ST=State/L=City/O=PSG/CN=TC")
sign_csr("tc.csr", "tc.crt")