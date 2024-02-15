from .convert import encrypt as convert_en
from .convert import decrypt as convert_de
from .sort import encrypt as sort_en
from .sort import decrypt as sort_de
from .pycryptodome import encrypt as str_en
from .pycryptodome import decrypt as str_de
from .configure import *

def encrypt(plaintext, password, sort_key=sort_key, convert_key=convert_key):
    # 对密码和明文进行加密
    # 将八位数字字符串加密
    encrypted_password = sort_en(sort_key, password)
    encrypted_password = convert_en(convert_key ,encrypted_password)
    # 对明文加密
    encrypted_text = str_en(plaintext, password)
    return encrypted_text, encrypted_password

def decrypt(encrypted_text, encrypted_password, sort_key=sort_key, convert_key=convert_key):
    # 将加密后的密码进行
    password = convert_de(convert_key, encrypted_password)
    password = sort_de(sort_key, password)
    # 对密文进行解密
    plaintext = str_de(encrypted_text, password)
    return plaintext

if __name__=="__main__":
    import random
    password = str(random.randint(10000000, 99999999))  # 随机生成的八位数整数待加密数据
    print("Original password:", password)
    plaintext = "啦啦啦啦，这是一段即将被加密的明文。"
    print("Original plaintext:", plaintext)

    encrypted_text, encrypted_password = encrypt(plaintext, password)
    print("Encrypted password:", encrypted_password)
    print("Encrypted text:", encrypted_text)

    decrypted_data = decrypt(encrypted_text, encrypted_password)
    print("Decrypted Data:", decrypted_data)
    # assert decrypted_data == data  # 确保加密和解密是可逆的（对于给定的密钥）

