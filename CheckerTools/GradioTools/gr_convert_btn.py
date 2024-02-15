import random

from ..Crypt.crypt import encrypt

def fn_convert(plaintext):
    password = str(random.randint(10000000, 99999999))  # 随机生成的八位数整数待加密数据
    # print(plaintext)
    encrypted_text, encrypted_password = encrypt(plaintext, password)
    txt_path = encrypted_password+'.txt'
    with open(txt_path, 'wb') as f:
        f.write(encrypted_text)
    return txt_path
