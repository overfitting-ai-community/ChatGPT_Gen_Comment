import streamlit as st
import openai

openai.api_key = st.secrets["api_key"]
SYSTEM_CONTENT = st.secrets["system_content"]

st.title("📝DCM comment generator")
st.text("Situation, Action, Result를 간략하게 입력하면,ChatGPT가 자기평가 comment를 생성합니다.")

with st.form("form"):
    user_input_situ = st.text_input("Situation")
    user_input_act = st.text_input("Action")
    user_input_res = st.text_input("Result")
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
        t.markdown("> %s..." % content)
        #st.write(st.session_state.content) 

    
    # for event in gpt_response:
    #     event_text = event['choices'][0]['text']  # extract the text
    #     st.write(event_text)  
       

    #prompt = gpt_response["choices"][0]["message"]["content"]
    #st.code(prompt)
    #st.write(prompt)
