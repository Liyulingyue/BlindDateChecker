import gradio as gr

from .static_str import *
from .gr_convert_btn import fn_convert


# 生成界面的函数（这里只是一个占位符，你需要实现你自己的逻辑）
def dummy_func(text):
    return "这是你的个人介绍：" + text


def dummy_judge(file1, file2):
    return "判断结果：未知（需要实现判断逻辑）"


# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown(matchmaker_title)

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

if __name__=="__main__":
    # 启动Gradio界面服务（开发模式下）
    demo.launch(debug=True)