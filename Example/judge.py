from CheckerTools.LLM.ernie import ErnieClass

decrypted_data1 = "大家好，我是张悦，今年28岁，现在在一家教育机构做英语老师。我的性格比较开朗，喜欢笑，也喜欢尝试新鲜的事物。业余时间我会去学习舞蹈和烹饪，我觉得这些都能给我的生活带来乐趣。对于我的另一半，我希望他有责任心、上进心，并且对生活充满热情。我不需要他有多么英俊，但希望我们能够有相似的价值观，能够在一起分享生活的点滴，共同创造美好的未来。"
decrypted_data2 = "大家好，我叫李昊，今年30岁，目前在一家互联网公司从事产品经理的工作。我性格比较外向，喜欢与人沟通，业余时间喜欢阅读、跑步和旅行。我认为生活应该是充实而有趣的，所以总是尽量找时间去体验不同的事物。对于相亲对象，我希望她善良、独立、有理想。长相不是最重要的，我更看重的是两个人在一起时的感觉，以及是否能够相互理解和支持。我期待的生活是两人可以共同成长，一起面对生活的挑战。"

ernie_access_token = "********" # 获取方式见reademe
llm = ErnieClass(access_token=ernie_access_token)
prompt = f"""
你是一个相亲判断机器人，你将获得两个人的个人信息，对对方的要求等信息。请你综合两个人的信息进行判断。判断结果通过json的格式返回。
返回内容是一个字典{"{"}'判断结果':bool{"}"}。其中，判断结果为True时，表明双方较为合适，有进一步发展的可能；False表明双方不适合。
相亲人1的信息是：{decrypted_data1}。
相亲人2的信息是：{decrypted_data2}。
"""
json_dict = llm.get_llm_json_answer(prompt)
check_result = json_dict["判断结果"]
print(check_result) # True为两个人合适，False为不合适