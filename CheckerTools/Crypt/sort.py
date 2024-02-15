import random

# 加密函数
def encrypt(key, data):
    if len(str(data)) != 8 or len(key) != 8 or not all("1" <= k <= "8" for k in key):
        raise ValueError("Both key and data must be sequences of 8 digits, and key must contain numbers from 1 to 8.")

        # 将数据转换为字符串并确保它是八位数
    data_str = str(data).zfill(8)

    # 根据密钥重新排列数据
    encrypted_text = [None] * 8
    for i, k in enumerate(key):
        encrypted_text[int(k) - 1] = data_str[i]

        # 连接重新排列后的字符以形成加密文本
    return ''.join(encrypted_text)


# 解密函数
def decrypt(key, encrypted_text):
    if len(encrypted_text) != 8 or len(key) != 8 or not all("1" <= k <= "8" for k in key):
        raise ValueError(
            "Both key and encrypted_text must be sequences of 8 characters, and key must contain numbers from 1 to 8.")

        # 根据密钥反向映射以恢复原始数据
    decrypted_text = [None] * 8
    for i, k in enumerate(key):
        decrypted_text[i] = encrypted_text[int(k) - 1]

        # 连接字符以形成解密后的数据，并转换为整数
    return ''.join(decrypted_text)

if __name__=="__main__":
    # 示例用法
    # 生成一个1-8的随机组合序列作为密钥
    key = ''.join([str(x) for x in random.sample(range(1, 9), 8)])
    print("Key:", key)

    # 八位数密文（这里为了演示，我们用一个固定的数）
    data = "42894361"
    print("Original Data:", data)

    # 使用正确的密钥解密
    decrypted_data = decrypt(key, data)
    print("Encrypted Text:", decrypted_data)

    # 加密一个明文数据（这里为了演示，我们用之前解密的数）
    plain_text = decrypted_data
    encrypted_data = encrypt(key, plain_text)
    print("Decrypted Data:", encrypted_data)