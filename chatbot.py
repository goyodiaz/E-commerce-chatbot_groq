import os
import streamlit as st
import opik
import opik.config as config

os.environ["OPIK_API_KEY"] = "123456"
config_ = config.get_from_user_inputs(
    project_name='Wizard Chatbot Demo1', workspace='wizard-bot1', url_override=None
)
st.write(config_)
st.write(config_.api_key)
client = opik.Opik(project_name='Wizard Chatbot Demo1', workspace='wizard-bot1')

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
