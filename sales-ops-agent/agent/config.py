import os
import streamlit as st


def get_openai_key():

    try:
        return st.secrets["OPENAI_API_KEY"]

    except Exception:
        return os.getenv("OPENAI_API_KEY")
    

def get_tavily_key():

    try:
        return st.secrets["TAVILY_API_KEY"]

    except Exception:
        return os.getenv("TAVILY_API_KEY")