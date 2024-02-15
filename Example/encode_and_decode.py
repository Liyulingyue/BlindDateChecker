from CheckerTools.Crypt.crypt import encrypt, decrypt

import random

password = str(random.randint(10000000, 99999999))  # 随机生成的八位数整数待加密数据
plaintext = 'hello world'  # 待加密数据
print("密码", password)
print("明文", plaintext)

encrypted_text, encrypted_password = encrypt(plaintext, password)
print("加密后的密码", encrypted_password)
print("加密后的明文", encrypted_text)
# 之后会将按照二进制流，例如open("example.txt", "wb") as f:的方式写入文件，读取文件需要使用open("example.txt", "rb") as f:

decrypted_text = decrypt(encrypted_text, encrypted_password)
print("解密后的明文", decrypted_text)