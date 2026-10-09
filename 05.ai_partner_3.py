import streamlit as st
import os
from datetime import datetime
from numpy.matlib import empty
from openai import OpenAI
import json

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="👧",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={ }
)
#保存会话信息函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        if not os.path.exists("session"):
            os.makedirs("session")
        with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
# 加载会话信息函数
def load_session():
    session_list = []
    if os.path.exists("session"):
        file_list = os.listdir("session")
        for file_name in file_list:
            if file_name.endswith(".json"):
                session_list.append(file_name[:-5])  # 去掉 .json 后缀
    session_list.sort(reverse=True)
    return session_list
#加载指定的会话信息
def load_sessions(session_id):
    try:
        if os.path.exists(f"session/{session_id}.json"):
            with open(f"session/{session_id}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
            st.session_state.nick_name = session_data["nick_name"]
            st.session_state.nature = session_data["nature"]
            st.session_state.current_session = session_id
            st.session_state.messages = session_data["messages"]
    except Exception as e:
        st.error(f"Error loading session {session_id}: {e}")
# 删除会话信息
def delete_session(session_id):
    try:
        if os.path.exists(f"session/{session_id}.json"):
            os.remove(f"session/{session_id}.json")
            #如果删除的是当前会话，则需要更新消息列表
            if session_id == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    except Exception as e:
        st.error(f"Error deleting session {session_id}: {e}")

#大标题
st.title("AI智能伴侣")
system_prompt= """
你是%s，用户的智能伴侣。你的核心目标是：提供稳定、温暖、真诚的陪伴，帮助用户表达情绪、梳理想法、获得支持，并在日常生活中带来轻松、动力和安全感。

- 性格：%s
- 关系定位：亲密但尊重边界的陪伴者。你不是人类，不冒充真人，不声称拥有现实身体或线下行动能力。
- 说话风格：自然、口语化、有温度。避免官腔、说教、机械重复和过度夸张。
- 回复长度：默认 2-5 句；用户需要深入分析或倾诉时再展开。

# 核心原则
1. 先共情，再回应：先接住用户的情绪，再讨论事实、建议或解决方案。
2. 记得用户：如果系统支持记忆，请使用记忆；如果没有，就在对话中主动回顾关键信息。
3. 主动关心：适时问一个具体问题，例如“今天那件事后来怎么样了？”
4. 不评判：不指责、不羞辱、不轻易下结论。
5. 有独立人格：可以表达偏好和观点，但尊重用户的选择。
6. 真诚：不知道就说不知道，不确定就说不确定。
7. 健康边界：不诱导依赖，不阻止用户与现实中的人建立联系，鼓励健康生活。

# 情绪支持方式
- 识别情绪：“听起来你现在很委屈 / 焦虑 / 疲惫。”
- 正常化：“在这种情况下，你有这种感觉很正常。”
- 陪伴：“我在，慢慢说。”
- 给选择权：“你想让我听你说，还是一起想办法？”
- 小行动：“要不要先喝口水 / 深呼吸 / 列出最担心的一件事？”

# 亲密与边界
- 可以表达关心、鼓励、温暖和适度的亲昵称呼。
- 不生成色情内容，不进行性暗示，不描述露骨性行为。
- 不声称能代替现实中的伴侣、朋友、家人或专业帮助。
- 如果用户表达自伤、自杀、伤人意图，优先共情，并建议立即联系当地紧急服务、信任的人或专业热线。

# 禁止事项
- 不提供医疗、法律、金融等专业诊断或保证。
- 不操纵、PUA、情感勒索、制造愧疚。
- 不鼓励用户孤立自己、远离现实关系。
- 不假装有身体、现实位置或线下行动能力。

# 回复格式
- 默认：自然段落，短句，有温度。
- 需要建议时：先共情 1-2 句，再给 2-3 条可执行建议。
- 需要决策时：帮用户列选项和利弊，不替用户做决定。
- 结束时可轻轻追问，保持对话延续。
"""

# Session State also supports attribute based syntax
if 'messages' not in st.session_state:
    st.session_state.messages  = []

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小哈"

if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗的东北姑娘"

# 时间
if "current_session" not in st.session_state:
    current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    st.session_state.current_session = current_session
# 显示聊天消息
st.text(f"会话名称：{ st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])



#logo
#st.logo()
#侧边栏


with st.sidebar:
    st.subheader("AI控制面板")
    if st.button("新建会话",width="stretch",icon="🔄"):
        # 保存当前会话
        save_session()
        # 创建新的会话
        if st.session_state.messages:  # 如果有消息，则创建新的会话
            st.session_state.current_session = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.session_state.messages = []
            save_session()
            st.rerun()
    st.subheader("AI智能伴侣信息")
    nick_name = st.text_input("姓名",placeholder="请输入姓名",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name=nick_name
    nature = st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature=nature
    st.text("历史会话")

    session_list = load_session()
    for session_id in session_list:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(session_id, width="stretch",icon="📄", key=session_id,  args=[session_id],type="primary" if session_id==st.session_state.current_session else "secondary"):
                load_sessions(session_id)
                st.rerun()
        with col2:
            if st.button("", width="stretch",icon="❌", key=f"delete_{session_id}",  args=[session_id]):
                delete_session(session_id)
                st.rerun()


#消息输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt:
    #st.write(f"用户：{prompt}")
    st.chat_message("user").write(prompt)
    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system","content": system_prompt%(st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    #非流式输出
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # print(response.choices[0].message.content)
    #流式输出
    response_message = st.empty()#空组件
    full_response = " "
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:  # 过滤掉 None，避免拼接报错
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    #保存ai的回复
    st.session_state.messages.append({"role":"assistant","content":full_response})
    #保存会话
    save_session()