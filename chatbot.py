import streamlit as st
import utils

if st.button("Make the call"):
    utils.opik_trace("__PROMPT__", "__MSG__", [])
