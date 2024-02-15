import os

from .configure import ernie_access_token

from ..Crypt.crypt import decrypt
from ..LLM.ernie import ErnieClass

def fn_judge(upload1, upload2):
    encrypted_password1 = os.path.basename(upload1)[:-4] # 移除.txt尾缀
    with open(upload1, 'rb') as f:
        encrypted_text1 = f.read()
    encrypted_password2 = os.path.basename(upload2)[:-4] # 移除.txt
    with open(upload2, 'rb') as f:
        encrypted_text2 = f.read()
    decrypted_data1 = decrypt(encrypted_text1, encrypted_password1)
    decrypted_data2 = decrypt(encrypted_text2, encrypted_password2)
    # print(decrypted_data1)
    # print(decrypted_data2)

    return "不合适"


def judge_by_both_infor(decrypted_data1, decrypted_data2):
    llm = ErnieClass(access_token=ernie_access_token)
