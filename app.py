import time
import streamlit as st
from agent.react_agent import ReactAgent

# 标题
st.title("智扫通机器人客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        # 调用智能体处理用户输入
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                # 模拟打字效果
                for char in chunk:
                  time.sleep(0.05)
                  yield char

        # 显示助手回复
        st.chat_message("assistant").write_stream(
            capture(res_stream, response_messages)
        )

        # 缓存最新的助手回复
        st.session_state["message"].append(
            {"role": "assistant", "content": "".join(response_messages[-1])}
        )
        
        st.rerun()
