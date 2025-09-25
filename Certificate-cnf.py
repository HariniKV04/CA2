import subprocess
from pathlib import Path

# Configuration
PRIVATE_KEY_FILE = "private.key"
CERT_FILE = "cert.crt"
KEY_SIZE = 2048
VALIDITY_DAYS = 365
CNF_FILE = "/etc/ssl/openssl.cnf"  # Use your existing CNF

def run(cmd):
    subprocess.run(cmd, check=True)

def generate_private_key(path: Path, key_size=2048):
    if not path.exists():
        print(f"[*] Generating private key ({key_size} bits) at {path} ...")
        run(["openssl", "genrsa", "-out", str(path), str(key_size)])
        print("[+] Private key generated.")
    else:
        print(f"[*] Private key already exists: {path}")

def create_self_signed_cert(key_path: Path, cert_path: Path, cnf_path: str, days=365):
    print(f"[*] Creating self-signed certificate at {cert_path} using CNF {cnf_path} ...")
    run([
        "openssl", "req", "-new", "-x509",
        "-key", str(key_path),
        "-out", str(cert_path),
        "-days", str(days),
        "-config", cnf_path
    ])
    print("[+] Self-signed certificate created.")

def main():
    key_path = Path(PRIVATE_KEY_FILE)
    cert_path = Path(CERT_FILE)

    if not Path(CNF_FILE).exists():
        print(f"[ERROR] CNF file not found: {CNF_FILE}")
        return

    generate_private_key(key_path, KEY_SIZE)
    create_self_signed_cert(key_path, cert_path, CNF_FILE, VALIDITY_DAYS)

if __name__ == "__main__":
    main()