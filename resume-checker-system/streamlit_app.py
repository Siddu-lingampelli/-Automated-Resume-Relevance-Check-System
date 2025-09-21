import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
sys.path.append(frontend_path)

# Import the main app components
from pages.1_JobDescriptions import show as show_job_descriptions
from pages.2_ResumeEvaluation import show as show_resume_evaluation
from pages.3_Dashboard import show as show_dashboard

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
        show_job_descriptions()
    elif page == "Resume Evaluation":
        show_resume_evaluation()
    elif page == "Dashboard":
        show_dashboard()

if __name__ == "__main__":
    main()