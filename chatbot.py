import streamlit as st
import opik

st.help(opik.Opik)
client = opik.Opik(project_name='Wizard Chatbot Demo1', workspace='wizard-bot1')
st.help(client)

if st.button("Make the call"):
    trace = client.trace(
        name='chat',
        input={'user_input': "__PROMPT__"},
        output={'response': "__MSG__"}
    )
    st.stop()
    trace.span(
        name='llm_call',
        type='llm',
        input={'context': []},
        output={'response': "__MSG__"}
    )
