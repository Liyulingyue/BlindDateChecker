import gradio as gr

from .static_str import *
from .gr_convert_btn import fn_convert
from .gr_judge_btn import fn_judge, fn_plaintext_judge
from .gr_agent_helper import init_gr_state, fn_chatbot_input

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown(matchmaker_title)

    with gr.Tab("主页面"):
        gr.Markdown(intro_subtitle)
        with gr.Row():
            input_box = gr.Textbox(label=input_title, info=input_info, placeholder=input_example, lines=6, scale=3)
            convert_button = gr.Button(button_text, scale=1)
            download_file = gr.File(label=download_description, file_types=[".txt"], interactive=False, scale=1)

        gr.Markdown(workroom_subtitle)
        with gr.Row():
            upload1 = gr.File(label=upload_description1, file_types=[".txt"], interactive=True, height=10)
            upload2 = gr.File(label=upload_description2, file_types=[".txt"], interactive=True, height=10)
        judge_button = gr.Button(judge_button_text)

        gr.Markdown(result_subtitle)
        result_box = gr.Textbox(label=result_title, info=result_info)

        # 添加按钮事件
        convert_button.click(fn=fn_convert, inputs=[input_box], outputs=[download_file])
        judge_button.click(fn=fn_judge, inputs=[upload1, upload2], outputs=[result_box])

    with gr.Tab("明文判断"):
        gr.Markdown(plaintext_input_subtitle)
        with gr.Row():
            plaintext1_box = gr.Textbox(label=plaintext1_title, value=plaintext1_example, lines=6)
            plaintext2_box = gr.Textbox(label=plaintext2_title, value=plaintext2_example, lines=6)
        plaintext_judge_button = gr.Button(judge_button_text)

        gr.Markdown(plaintext_result_subtitle)
        plaintext_result_box = gr.Textbox(label=plaintext_result_title, info=plaintext_result_info)
        plaintext_reason_box = gr.Textbox(label=plaintext_reason_title, lines=6)

        gr.Examples(
            [[plaintext1_example, plaintext2_example], [plaintext1_example2, plaintext2_example2]],
            [plaintext1_box, plaintext2_box]
        )

        # 添加按钮事件
        plaintext_judge_button.click(fn=fn_plaintext_judge, inputs=[plaintext1_box, plaintext2_box], outputs=[plaintext_result_box, plaintext_reason_box])
    with gr.Tab("交互式生成个人评价"):
        gr.Markdown(generation_subtitle)
        agent_state = gr.State(value = init_gr_state())
        chatbot = gr.Chatbot(
            label = "历史对话",
            value = [("hi", "您好，我是相亲信息登记员红娘。非常感谢您选择我们的相亲服务。"
                             "为了更好地了解您的需求和期望，以便为您推荐更合适的相亲对象，我们需要收集一些您的个人信息。"
                             "这些信息包括您的姓名、年龄等基本情况，以及您的性格、兴趣爱好、生活习惯等方面的特点。"
                             "请放心，我们会严格保密您的个人信息。现在，可以请您先简单介绍一下自己吗？")])
        with gr.Row():
            chatbot_input_text = gr.Textbox(label="输入您的回复", scale=4)
            chatbot_input_button = gr.Button(value = "发送", scale=1)
        chatbot_output_text = gr.Textbox(label="抽取到的个人介绍", info="当结束对话后，可以将这段内容复制到主页面进行加密~")

        chatbot_input_button.click(fn=fn_chatbot_input,
                                   inputs=[agent_state, chatbot_input_text, chatbot],
                                   outputs=[agent_state, chatbot_input_text, chatbot, chatbot_output_text])


if __name__=="__main__":
    # 启动Gradio界面服务（开发模式下）
    demo.launch(debug=True)