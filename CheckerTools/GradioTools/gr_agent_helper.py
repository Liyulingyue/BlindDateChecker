import Agently
from .configure import ernie_access_token
from .static_str import chatbot_init_value_custom, chatbot_init_value_agent

agent_factory = Agently.AgentFactory()

# using ERNIE(文心4.0)
agent_factory \
    .set_settings("current_model", "ERNIE") \
    .set_settings("model.ERNIE.auth", {"aistudio": ernie_access_token})

agent = agent_factory.create_agent()
agent \
    .set_role("角色", "相亲信息登记员") \
    .set_role("姓名", "红娘") \
    .set_role(
    "信息收集方法",
    "对于一些事实性的信息，例如姓名、年龄，可以从用户对话中抽取，或者直接询问。" +
    "但对于一些具有抽象特征的信息，例如脾气、心态、性格等，需要从对话中，根据言谈特征自行总结。"
) \
    .general(
    "为什么要进行对话：" + \
    "在每个人进行相亲之前，都需要先录入自己的信息，但是自己对自己的评价可能较为主观。" + \
    "因此，通过对话、一问一答的方式，除了能够获取这个人的个人信息之外，还能够挖掘这个人的能够更好地采集到这个人的性格特征。"
)

def init_gr_state():
    state = {
        "can_stop": False,
        "chat_history": [ # 初始化历史信息
            { "role": "user", "content": chatbot_init_value_custom},
            { "role": "assistant", "content": chatbot_init_value_agent}
        ],
        "customer_information": "",
    }
    return state

def fn_chatbot_input(gr_state, input_text, chat_bot_infor):
    customer_information = gr_state["customer_information"]
    can_stop = gr_state["can_stop"]
    chat_history = gr_state["chat_history"]

    customer_response = input_text
    # Filling the Form: Survey Agent Analyses the Response, Fills the Form and Replies.
    analysis = agent \
        .chat_history(chat_history) \
        .input({
        "用户回复": customer_response,
    }) \
        .info({"用户信息": customer_information}) \
        .output({
        "整理后的用户信息": (
            "String",
            "对{用户回复}进行分析，从中挖掘用户的信息，以及你对用户的评价（例如情绪、性格特点等），" + \
            "将这些信息补充到{用户信息}中，你也可以对{用户信息}中已有的信息进行修正。"
        ),
    }) \
        .start()
    if "整理后的用户信息" in analysis and analysis["整理后的用户信息"] not in (None, ""):
        customer_information = analysis["整理后的用户信息"]
    # print(f"[用户信息]: {customer_information}")
    # 回复
    question = agent \
        .chat_history(chat_history) \
        .instruct(
        "行为准则",
        [
            "1. 检查{用户信息}并考虑你是否从用户那里获取了足够的信息，从而支持你根据这份资料向其他人介绍这位相亲对象。",
            "2. 如果信息并不充分，请继续询问。",
            "3. 如果信息充分，则结束询问，输出中{结束判断}为True，否则结束判断都应为False",
            "4. 请检查对话历史，保证对话的连贯性，用户的最近一次回复在{用户回复}中，而非对话历史中",
        ]
    ) \
        .input({
        "用户信息": customer_information,
        "用户回复": customer_response,
    }) \
        .output({
        "结束判断": (
        "Boolean", "对话是否应当结束的标识符，如果你收集到了足够信息，对话应当结束，否则，你需要进一步进行对话。"),
        "回复内容": (
        "String", "如果{结束判断}为True，则输出对话结束语。否则，你需要进一步和用户进行对话，以收集更多的信息。"),
    }) \
        .start()
    # print("[Survey Agent]: ", question["回复内容"])
    chat_history.extend([
        {"role": "user", "content": customer_response},
        {"role": "assistant", "content": question["回复内容"]}
    ])
    if question["结束判断"]:
        can_stop = True

    gr_state["customer_information"] = customer_information
    gr_state["can_stop"] = can_stop
    gr_state["chat_history"] = chat_history
    chat_bot_infor.append((customer_response, question["回复内容"]))

    return gr_state, "", chat_bot_infor, customer_information

def fn_chatbot_reset():
    return init_gr_state(), [(chatbot_init_value_custom, chatbot_init_value_agent)], "", ""