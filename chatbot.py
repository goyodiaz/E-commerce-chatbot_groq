import streamlit as st
import opik

def opik_trace(input_data, output, context):
    trace = client.trace(
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

client = opik.Opik(project_name='Wizard Chatbot Demo1', workspace='wizard-bot1')

if st.button("Make the call"):
    # opik_trace("__PROMPT__", "__MSG__", [])
    input_data = "__PROMPT__"
    output = "__MSG__"
    context = []
    trace = client.trace(
        name='chat',
        input={'user_input': input_data},
        output={'response': output}
    )
