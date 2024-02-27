import Agently
from CheckerTools.GradioTools.configure import ernie_access_token

agent_factory = Agently.AgentFactory()

# using ERNIE(文心4.0)
agent_factory\
    .set_settings("current_model", "ERNIE")\
    .set_settings("model.ERNIE.auth", { "aistudio": ernie_access_token })

agent = agent_factory.create_agent()
agent\
    .set_role("角色", "相亲信息登记员")\
    .set_role("姓名", "红娘")\
    .set_role(
        "信息收集方法",
        "对于一些事实性的信息，例如姓名、年龄，可以从用户对话中抽取，或者直接询问。" +
        "但对于一些具有抽象特征的信息，例如脾气、心态、性格等，需要从对话中，根据言谈特征自行总结。"
    )\
    .general(
        "为什么要进行对话"+\
        "在每个人进行相亲之前，都需要先录入自己的信息，但是自己对自己的评价可能较为主观。"+\
        "因此，通过对话、一问一答的方式，除了能够获取这个人的个人信息之外，还能够挖掘这个人的能够更好地采集到这个人的性格特征。"
    )

# 开场
can_stop = False
chat_history = []
customer_information = ""
opening = agent\
    .info({
        "用户信息": customer_information,
    })\
    .output({
        "开场白": (
            "String",
            "关于这次对话的开场白，并且为这种对话式信息收集的方式进行解释。"+\
            "比如说，你的姓名，我们希望收集哪些新信息，并且请用户进行一些介绍，或者问一些问题以了解这个用户的喜好、性格特点。"
        ),
    })\
    .start()
print("[Survey Agent]: ", opening["开场白"])
# Update logic to suit some models require chat history strictly follow the
# order: user-assistant-user-assistant
chat_history.extend([
    { "role": "user", "content": "hi" },
    { "role": "assistant", "content": opening["开场白"] }
])
# 循环对话
while not can_stop:
    customer_response = input(f"[Customer]:  ")
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
    print(f"[用户信息]: {customer_information}")
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
    print("[Survey Agent]: ", question["回复内容"])
    chat_history.extend([
        {"role": "user", "content": customer_response},
        {"role": "assistant", "content": question["回复内容"]}
    ])
    if question["结束判断"]:
        can_stop = True

# 对话示例如下
'''
[Customer]:   我叫Liyulingyue，今年30岁
[用户信息]: Liyulingyue，30岁。目前提供的信息较少，无法准确判断性格特点和情绪状态。需要进一步交流以获取更多信息。
[Survey Agent]:  很高兴认识您，Liyulingyue。除了年龄之外，能否请您再分享一些关于自己的信息？比如您的职业、兴趣爱好，或者您希望在相亲对象身上看到的特质？这些信息能帮助我们更好地为您匹配合适的相亲对象。
[Customer]:   我平时喜欢写代码，个人比较无趣，很闲散，很吵闹，没有太多有趣的话题，但是自己又比较怕孤独
[用户信息]: Liyulingyue，30岁。喜欢写代码，这可能意味着他/她具有一定的逻辑思维能力和专注力。用户形容自己无趣、闲散、吵闹，这可能反映了他/她在某些情况下的自我评价较低，或者在尝试以自嘲的方式表达自己。同时，用户表示自己怕孤独，这可能意味着他/她在社交方面有一定的需求，但可能由于某些原因感到难以与他人建立深入的联系。总的来说，用户可能是一个在寻找自我认同和社交归属感的过程中感到有些迷茫的人。
[Survey Agent]:  感谢您分享的个人信息，Liyulingyue。了解到您喜欢写代码，这确实体现了您的逻辑思维和专注力。同时，您也提到了自己的一些性格特点，比如无趣、闲散和吵闹。虽然您这样形容自己，但我相信每个人都有自己独特的魅力。您还提到自己怕孤独，这说明您渴望社交和与他人的联系。为了更好地了解您，我能否再询问一些关于您的生活习惯、兴趣爱好或者对相亲对象的期望等方面的信息呢？这些信息将有助于我们为您推荐更合适的相亲对象。
[Customer]:   我平时可能会晚睡，但是会早起。早起比较像是一种习惯一样。但晚睡可能是受到了手机的诱惑，或者玩电脑的诱惑。希望另一半可以早睡早起督促我！
[用户信息]: Liyulingyue，30岁，喜欢写代码，具有一定的逻辑思维能力和专注力。他形容自己无趣、闲散、吵闹，这反映了他可能存在一定的自我认知挑战或独特的自嘲式幽默感。他怕孤独，表明他渴望社交和亲密关系。他提到自己晚睡但早起，晚睡可能是因为受到电子设备诱惑，早起则像是种习惯。他希望另一半能早睡早起督促他，这显示了他对改善生活习惯的渴望和对未来伴侣的期待。在寻找自我认同和社交归属感方面，他可能正经历一些迷茫，但同时也在积极寻求改变和进步。
[Survey Agent]:  了解到您晚睡早起的情况，也明白您希望另一半能帮助您调整作息。这是个很实际的需求，相信很多自律的相亲对象都能满足。除了作息习惯，您对未来伴侣还有其他方面的期待吗？比如性格、兴趣爱好或者生活态度等方面的要求？
[Customer]:   希望对方比较认真，又比较闲散。可能有点矛盾，但是我们总是在认真的人身上看到闪光。但我并不是一个非常卷的人，所以我希望有很多机会和她一起玩乐，做一些开心的事情。
[用户信息]: Liyulingyue，30岁，喜欢写代码，具有一定的逻辑思维能力和专注力。他形容自己无趣、闲散、吵闹，但同时也在寻求认真与闲散之间的平衡。他害怕孤独，渴望社交和亲密关系，希望与伴侣一起玩乐，享受开心时光。他晚睡早起，希望另一半能帮助他调整作息。在性格上，他可能既有自我认知挑战的一面，也有积极寻求改变和进步的一面。他对未来的伴侣有着明确的期待，既希望她认真闪光，又能与他一起享受闲散的生活。
[Survey Agent]:  明白了，您希望找到一个既认真又闲散，能与您一起享受生活的伴侣。这是个很美好的愿景。我想进一步了解一下，您对未来伴侣在生活习惯上有什么具体的期待吗？比如饮食习惯、运动习惯或者其他方面的生活习惯。
[Customer]:   我可能不太能接收武汉的甜豆腐脑，除此之外，我不太能吃辣。所以我希望我的对象不会是一定要吃辣椒的人。
[用户信息]: Liyulingyue，30岁，喜欢写代码，具有一定的逻辑思维能力和专注力。他形容自己无趣、闲散、吵闹，但同时也在寻求认真与闲散之间的平衡。他害怕孤独，渴望社交和亲密关系，希望与伴侣一起玩乐，享受开心时光。在饮食习惯上，他不太能接受武汉的甜豆腐脑，也不太能吃辣，希望未来的伴侣不会是一定要吃辣椒的人。他晚睡早起，希望另一半能帮助他调整作息。在性格上，他可能既有自我认知挑战的一面，也有积极寻求改变和进步的一面。他对未来的伴侣有着明确的期待，既希望她认真闪光，又能与他一起享受闲散的生活，同时在饮食习惯上能够相互适应和迁就。
[Survey Agent]:  了解到您在饮食习惯上的偏好，这对我们为您寻找合适的相亲对象很有帮助。除了饮食习惯，您对未来伴侣在生活习惯、性格、兴趣爱好等方面还有哪些具体的期待吗？请随时告诉我，我们会尽力满足您的需求。
[Customer]:   性格上希望对方温柔一些。如果她也喜欢打游戏，我们有共同话题当然很好，如果没有也无妨。另外，我希望她不是一个喜欢说粗口的人。
[用户信息]: Liyulingyue，30岁，喜欢写代码，具有一定的逻辑思维能力和专注力。他形容自己无趣、闲散、吵闹，但同时也在寻求认真与闲散之间的平衡。他害怕孤独，渴望社交和亲密关系，希望与伴侣一起玩乐，享受开心时光。在饮食习惯上，他不太能接受甜豆腐脑和辣椒，希望未来的伴侣能在这方面迁就他。他晚睡早起，希望另一半能帮助他调整作息。在性格上，他希望找到一个温柔、不说粗口的伴侣，最好有共同的游戏爱好，如果没有也无妨。Liyulingyue可能既有自我认知挑战的一面，也有积极寻求改变和进步的一面。他对未来的伴侣有着明确的期待，既希望她认真闪光，又能与他一起享受闲散的生活，同时在饮食和生活习惯上能够相互适应和迁就。
[Survey Agent]:  好的，我已经了解了您对未来伴侣的期望，包括性格上的温柔、不说粗口，以及共同的游戏爱好（如果有的话）。同时，您也提到了在饮食和生活习惯上的期望。我会根据您的需求，尽力为您寻找合适的相亲对象。如果有任何问题或需要进一步的帮助，请随时告诉我。

'''