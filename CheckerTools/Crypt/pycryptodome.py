from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

def encrypt(plaintext, password):
    # plaintext为str，password为str，输出为btypes，因此输出必须采用with open('example.txt','rw+')来进行读写
    # 确保密码长度是16的倍数（AES-128）
    if len(password) > 16:
        password = password[:16]
    elif len(password) < 16:
        password += '\0' * (16 - len(password))

    key = password.encode()  # 在实际应用中，应该使用更安全的密钥派生函数
    plaintext = plaintext.encode()
    iv = get_random_bytes(16)  # 初始化向量

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    iv_ciphertext = iv+ciphertext
    return iv_ciphertext

def decrypt(iv_ciphertext, password):
    # password为str，iv_ciphertext为btypes，输出为str，因此iv_ciphertext必须采用with open('example.txt','rw+')来进行读写
    # 确保密码长度是16的倍数（AES-128）
    if len(password) > 16:
        password = password[:16]
    elif len(password) < 16:
        password += '\0' * (16 - len(password))

    key = password.encode()  # 在实际应用中，应该使用更安全的密钥派生函数

    iv = iv_ciphertext[:16]
    ciphertext = iv_ciphertext[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    plaintext = plaintext.decode()

    return plaintext

if __name__=="__main__":
    password = 'BBASAAAAAAAAAAAA'  # 注意：密码应该是安全的，并且在实际应用中不应该硬编码

    plaintext = "加密文字！"
    print("Original Data:", plaintext)

    encrypted_text = encrypt(plaintext, password)
    print("Encrypted Text:", encrypted_text)

    decrypted_text = decrypt(encrypted_text, "BBASAAAAAAAAAAAA")
    print("Decrypted Data:", decrypted_text)
    assert decrypted_text == plaintext  # 确保加密和解密是可逆的（对于给定的密钥）