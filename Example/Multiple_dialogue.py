from CheckerTools.LLM.ernie import ErnieClass
from CheckerTools.GradioTools.configure import ernie_access_token

# 该py文件用户实现多轮对话，但是效果不是特别好。

agent_1 = ErnieClass(access_token=ernie_access_token)
agent_2 = ErnieClass(access_token=ernie_access_token)

max_loop = 10

role_1 = "大家好，我是刘婷，今年29岁，现在是一家时尚杂志的编辑。我的性格比较外向，喜欢社交和聚会，业余时间我会和朋友一起逛街、看电影或者旅行。我认为生活应该是多姿多彩的，充满了欢笑和惊喜。对于我的另一半，我希望他能够陪我一起享受生活，给我足够的关心和浪漫。我希望我们的生活能够充满乐趣和爱意，而不是单调和乏味。"
role_2 = "大家好，我是王磊，今年32岁，目前在一家大型企业担任高级工程师。我的性格比较内向，喜欢安静的环境，业余时间多用来研究新技术和编程。我认为生活应该简单而有条理，不喜欢太过复杂和混乱的事物。对于我的另一半，我希望她能够温柔、贤惠，能够理解和支持我的工作。我不希望她过多地干涉我的生活，更希望我们能够有各自的空间和自由。"

start_prompt_1 = (f"你需要扮演一个人和相亲对象聊天，你需要通过聊天来增进自己对对方的了解，这次对话将帮助你判断这次相亲对象是否合适。"
                  f"你需要在这场对话中尽可能地展现个性，并尽可能了解对方的特点，这些特点包括了言谈举止、生活习惯、爱好、发展规划等方面。"
                  f"请尽可能在{max_loop}轮对话内，收集足够的信息，请注意，你们的对话将作为你判断这个相亲对象是否合适的标准。"
                  f"你扮演的人的个人信息是{role_1}。"
                  f"如果明白，请回复好的。")
start_prompt_2 = (f"你需要扮演一个人和相亲对象聊天，你需要通过聊天来增进自己对对方的了解，这次对话将帮助你判断这次相亲对象是否合适。"
                  f"你需要在这场对话中尽可能地展现个性，并尽可能了解对方的特点，这些特点包括了言谈举止、生活习惯、爱好、发展规划等方面。"
                  f"请尽可能在{max_loop}轮对话内，收集足够的信息，请注意，你们的对话将作为你判断这个相亲对象是否合适的标准。"
                  f"你扮演的人的个人信息是{role_2}。"
                  f"现在，请由你开始对话。你可以简单介绍自己，并问对方一些你感兴趣的问题。")

answer_1 = agent_1.chat(start_prompt_1)
answer_2 = agent_2.chat(start_prompt_2)

max_loop = 10
for i in range(max_loop):
    answer_1 = agent_1.chat(answer_2)
    answer_2 = agent_2.chat(answer_1)
    print(f"{i}/{max_loop}")

end_prompt = f'''
请根据你和你的相亲对象的对话内容，判断你的相亲对象和你之间是否合适。判断结果通过json的格式返回。
返回内容是一个字典{"{"}"判断结果":bool{"}"}。其中，判断结果为True时，表明双方较为合适，有进一步发展的可能；False表明双方不适合。
'''

answer_1 = agent_1.chat(end_prompt)
answer_2 = agent_2.chat(end_prompt)

print(agent_1.chat_history)
print(answer_1)
print(agent_2.chat_history)
print(answer_2)


