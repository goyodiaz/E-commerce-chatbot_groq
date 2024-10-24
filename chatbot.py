import streamlit as st
import opik

def opik_trace(input_data, output, context):
    trace = opik_client.trace(
        name='chat',
        input={'user_input': input_data},
        output={'response': output}
    )

    trace.span(
        name='llm_call',
        type='llm',
        input={'context': context},
        output={'response': output}
    )

if st.button("Make the call"):
    client = opik.Opik(project_name='Wizard Chatbot Demo1', workspace='wizard-bot1')
    opik_trace("__PROMPT__", "__MSG__", [])
