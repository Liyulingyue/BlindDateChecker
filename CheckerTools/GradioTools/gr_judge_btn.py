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
    check_result = judge_by_both_infor(decrypted_data1, decrypted_data2)
    output_text = "合适" if check_result else "不合适"
    return output_text


def judge_by_both_infor(decrypted_data1, decrypted_data2):
    llm = ErnieClass(access_token=ernie_access_token)
    prompt = f"""
    你是一个相亲判断机器人，你将获得两个人的个人信息，对对方的要求等信息。请你综合两个人的信息进行判断。判断结果通过json的格式返回。
    返回内容是一个字典{"{"}'判断结果':bool{"}"}。其中，判断结果为True时，表明双方较为合适，有进一步发展的可能；False表明双方不适合。
    相亲人1的信息是：{decrypted_data1}。
    相亲人2的信息是：{decrypted_data2}。
    """
    json_dict = llm.get_llm_json_answer(prompt)
    check_result = json_dict["判断结果"]
    return check_result
