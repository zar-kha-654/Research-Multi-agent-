import streamlit as st
from crewai import LLM


def get_llm():
    return LLM(
        model="openai/gpt-oss-120b",
        api_key=st.secrets["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
        temperature=0.2,
    )
