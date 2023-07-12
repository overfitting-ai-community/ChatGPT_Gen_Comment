import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]
SYSTEM_CONTENT = st.secrets["system_content"]

st.title("📝DCM comment generator")
st.text("Situation, Action, Result를 간략하게 입력하면,ChatGPT가 자기평가 comment를 생성합니다.")

with st.form("form"):
    user_input_situ = st.text_input("Situation", "올해 매출 목표는 작년 대비 150%를 달성해야 하는 도전적인 목표였음.")
    user_input_act = st.text_input("Action", "나는 목표를 달성하기 위해서 세미나에서 신규 고객 발굴하고 기존고객은 지속방문하는 방안을 동원했음.")
    user_input_res = st.text_input("Result", "올해 목표의 150%를 달성하지 못함. 130% 달성하였음")
    submit = st.form_submit_button("Generate")

if submit and user_input_situ and user_input_act and user_input_res:
    user_input = " <Situation> "+ user_input_situ + " <Action> " + user_input_act + " <Result> " + user_input_res
    #st.write(user_input)
    gpt_prompt = [{
        "role": "system",
        "content": SYSTEM_CONTENT
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt,
            stream=True,
             )
    # iterate through the stream of events
    t = st.empty()
    content = ""
    #st.session_state.content = ""
    counter = 0
    for completions in gpt_response:
        counter += 1
        if "content" in completions.choices[0].delta:
            content += completions.choices[0].delta.get("content")
        t.markdown(" %s " % content)
        #st.write(st.session_state.content) 
