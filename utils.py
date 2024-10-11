import opik

opik_client = opik.Opik()

def opik_trace(user_input, response):
    trace = opik_client.trace(name='chat', input={'user_input': user_input}, output={'response': response})
    trace.span(name='llm_call', input={'context': user_input}, output={'response': response})
