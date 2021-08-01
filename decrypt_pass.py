import os

from Crypto.Cipher import AES


def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")


def decrypt_file(file, key):
    with open(file, 'rb') as f:
        ciphertext = f.read()
    decr = decrypt(ciphertext, key)
    with open(os.path.basename(file)[:-4] + "_decrypted.txt", 'wb+') as f:
        f.write(decr)
    return os.path.basename(file)[:-4] + "_decrypted.txt"


def main():
    filepath = input("Input the path to the file to decrypt: ").strip(" \"")
    key = input("Input the decryption key: ").strip(" \"").encode()
    
    filename = decrypt_file(filepath, key)
    print(f"The decryption was successful. You can now open the file: {filename}")


main()
