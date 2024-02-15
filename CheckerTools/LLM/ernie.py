import erniebot
import json

class ErnieClass(object):

    def __init__(self, access_token, api_type="aistudio"):
        super.__init__()
        erniebot.api_type = 'aistudio'
        erniebot.access_token = access_token

    def get_llm_answer_with_msg(self, msg):
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=msg,
            top_p=0,
            temperature = 0.1,
        )
        result = response.get_result()
        return result

    def get_llm_answer(self, prompt):
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content': prompt}],
            top_p=0,
            temperature=0.1,
        )
        result = response.get_result()
        return result

    def extract_json_from_llm_answer(self, result, start_str="```json", end_str="```", replace_list=["\n"]):
        s_id = result.index(start_str)
        e_id = result.index(end_str, s_id+len(start_str))
        json_str = result[s_id+len(start_str):e_id]
        for replace_str in replace_list:
            json_str = json_str.replace(replace_str,"")
        json_dict = json.loads(json_str)
        return json_dict

    def get_llm_json_answer(self, prompt):
        result = self.get_llm_answer(prompt)
        json_dict = self.extract_json_from_llm_answer(result)
        return json_dict