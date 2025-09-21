import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
frontend_path = os.path.dirname(__file__)
sys.path.append(frontend_path)

# Import the main app components
from pages import (
    JobDescriptions as page_job_descriptions,
    ResumeEvaluation as page_resume_evaluation,
    Dashboard as page_dashboard
)

st.set_page_config(
    page_title="Resume Checker System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("Resume Checker System")
    
    # Navigation in sidebar
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Job Descriptions", "Resume Evaluation", "Dashboard"]
    )
    
    if page == "Job Descriptions":
        page_job_descriptions.show()
    elif page == "Resume Evaluation":
        page_resume_evaluation.show()
    elif page == "Dashboard":
        page_dashboard.show()

if __name__ == "__main__":
    main()