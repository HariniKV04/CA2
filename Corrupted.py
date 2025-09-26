#Run this first in the terminal
""" Make a 64-byte text file
echo "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz!!" > plain.txt

# Key & IV (128-bit each, hex)
KEY="00112233445566778899aabbccddeeff"
IV="0102030405060708090a0b0c0d0e0f10"

# Encrypt in different modes
openssl enc -aes-128-ecb -e -in plain.txt -out ecb.bin -K $KEY -nopad
openssl enc -aes-128-cbc -e -in plain.txt -out cbc.bin -K $KEY -iv $IV -nopad
openssl enc -aes-128-cfb -e -in plain.txt -out cfb.bin -K $KEY -iv $IV
openssl enc -aes-128-ofb -e -in plain.txt -out ofb.bin -K $KEY -iv $IV"""


import subprocess, shutil, os

key = "00112233445566778899aabbccddeeff"
iv  = "0102030405060708090a0b0c0d0e0f10"
modes = {
    "ECB": "-aes-128-ecb",
    "CBC": "-aes-128-cbc",
    "CFB": "-aes-128-cfb",
    "OFB": "-aes-128-ofb"
}

def corrupt(fname, byte_index=29):
    with open(fname, "rb+") as f:
        data = bytearray(f.read())
        data[byte_index] ^= 0x01
        f.seek(0); f.write(data)

for name, opt in modes.items():
    enc = f"{name.lower()}.bin"
    dec = f"{name.lower()}_dec.txt"

    # fresh copy before corruption
    shutil.copyfile(enc, f"{name.lower()}_corrupt.bin")
    corrupt(f"{name.lower()}_corrupt.bin")

    # decrypt
    cmd = ["openssl","enc",opt,"-d",
           "-in",f"{name.lower()}_corrupt.bin","-out",dec,
           "-K",key]
    if name != "ECB": cmd += ["-iv",iv]
    subprocess.run(cmd, check=True)

    print(f"\n{name} decrypted output (after 1-bit error):")
    print(open(dec).read())
    print("-"*50)