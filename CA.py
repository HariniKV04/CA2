import subprocess

def run(cmd):
    subprocess.run(cmd, check=True)

run(["openssl", "genrsa", "-out", "ca.key", "4096"])
run([
    "openssl", "req", "-x509", "-new", "-nodes",
    "-key", "ca.key", "-sha256", "-days", "3650",
    "-subj", "/C=US/ST=State/L=City/O=PSG/CN=CA",
    "-out", "ca.crt"
])
