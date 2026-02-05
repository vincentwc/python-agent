import os
import time

import streamlit as st
from dotenv import load_dotenv
from agent.react_agent import ReactAgent

# 加载环境变量
load_dotenv()


# 配置页面
st.set_page_config(
    page_title="智扫通机器人客服",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 侧边栏
with st.sidebar:
    st.header("🤖 智扫通设置")
    st.markdown("欢迎使用智扫通机器人客服。")

    if st.button("🗑️ 清空对话记录"):
        st.session_state["message"] = []
        st.rerun()

    st.divider()
    st.markdown("### 关于")
    st.markdown("本系统基于LangChain和通义千问大模型构建。")
    st.markdown("版本: v1.0.0")

# 主标题
st.title("🤖 智扫通机器人客服")
st.caption("您的智能扫地机器人助手，随时为您解答疑问。")
st.divider()

# 初始化Agent
if "agent" not in st.session_state:
    with st.spinner("正在初始化智能客服系统..."):
        try:
            st.session_state["agent"] = ReactAgent()
        except Exception as e:
            st.error(f"系统初始化失败: {str(e)}")
            st.stop()

# 初始化消息历史
if "message" not in st.session_state:
    st.session_state["message"] = []

# 显示历史消息
for message in st.session_state["message"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
prompt = st.chat_input("请输入您的问题...")

if prompt:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 处理回复
    response_messages = []
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 调用智能体处理用户输入
                res_stream = st.session_state["agent"].execute_stream(prompt)

                # 定义流式输出捕获函数
                def capture(generator, cache_list):
                    full_response = ""
                    for chunk in generator:
                        full_response += chunk
                        cache_list.append(chunk)
                        # 模拟打字效果
                        for char in chunk:
                            time.sleep(0.005)  # 稍微快一点
                            yield char

                # 流式输出
                st.write_stream(capture(res_stream, response_messages))

                # 缓存完整的回复
                full_content = "".join(response_messages)
                st.session_state["message"].append(
                    {"role": "assistant", "content": full_content}
                )
            except Exception as e:
                st.error(f"生成回复时发生错误: {str(e)}")
