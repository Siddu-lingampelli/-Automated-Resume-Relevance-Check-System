import streamlit as st

def score_badge(score):
    color = "�" if score >= 75 else "�" if score >= 50 else "�"
    st.write(f"{color} {score}")
