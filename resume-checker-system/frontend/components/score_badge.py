import streamlit as st

def score_badge(score):
    color = "í¿¢" if score >= 75 else "í¿¡" if score >= 50 else "í´´"
    st.write(f"{color} {score}")
