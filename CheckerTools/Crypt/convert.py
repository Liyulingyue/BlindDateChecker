import random
import string


# 加密函数
def encrypt(key, data):
    if len(key) != 8 or len(data) != 8:
        raise ValueError("Both key and data must be 8-digit integers.")

        # 将密钥和数据交错拼接起来
    interleaved = ''.join([c1 + c2 for c1, c2 in zip(key.zfill(8), data.zfill(8))])

    # 将数字转换为26进制的字母表示
    encrypted = ''
    for i in range(0, 16, 2):
        num = int(interleaved[i:i + 2])
        if num < 26:
            encrypted += "A"+string.ascii_uppercase[num]  # 0-25 转换为 A-Z
        else:
            # 对于大于25的数，需要特殊处理为两位字母
            first_digit = num // 26  # 计算高位数字
            second_digit = num % 26  # 计算低位数字
            encrypted += string.ascii_uppercase[first_digit] + string.ascii_uppercase[second_digit]

    return encrypted


# 解密函数
def decrypt(key, encrypted_text):
    if len(key) != 8 or len(encrypted_text) != 16:
        raise ValueError("Invalid input for decryption.")

    # 用于存储解密出的数字的列表
    decrypted_nums = []
    for i in range(0, 16, 2):
        char1 = encrypted_text[i]
        char2 = encrypted_text[i+1]
        num1 = string.ascii_uppercase.index(char1)
        num2 = string.ascii_uppercase.index(char2)
        num = num1*26+num2
        de_num = num%10
        decrypted_nums.append(str(de_num))

    # 将加密数据的数字序列转换回原始的八位数整数
    decrypted_data = ''.join(decrypted_nums)
    if len(decrypted_data) != 8:
        raise ValueError("Decrypted data must be 8-digit integers.")

    return decrypted_data


if __name__=="__main__":
    # 示例用法：
    key = "13415926"  # 人工配置的八位数整数密钥
    shuffle_key = "12345678"

    data = str(random.randint(10000000, 99999999))  # 随机生成的八位数整数待加密数据
    print("Original Data:", data)

    encrypted_text = encrypt(key, data)
    print("Encrypted Text:", encrypted_text)

    decrypted_data = decrypt(key, encrypted_text)
    print("Decrypted Data:", decrypted_data)
    assert decrypted_data == data  # 确保加密和解密是可逆的（对于给定的密钥）