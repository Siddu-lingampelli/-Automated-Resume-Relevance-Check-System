import streamlit as st

def resume_card(name, score, verdict):
    st.markdown(f"**{name}** - Score: {score}, Verdict: {verdict}")
