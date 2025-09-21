# -*- coding: utf-8 -*-
import streamlit as st
from utils.api_client import upload_resume, get_jds
from typing import Dict, Any, List, Union, Optional
import PyPDF2
import docx
import io
from tempfile import NamedTemporaryFile
import os

# Type definitions
JobDescription = Dict[str, Union[str, List[str]]]
EvaluationResult = Dict[str, Any]

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def display_job_details(jd: JobDescription) -> None:
    """Display job details in a formatted way"""
    st.write("### 📋 Job Details")
    title = jd.get('title', 'No title') if isinstance(jd, dict) else 'No title'
    location = jd.get('location', 'No location') if isinstance(jd, dict) else 'No location'
    description = jd.get('description', 'No description') if isinstance(jd, dict) else 'No description'
    
    st.write(f"**Title:** {title}")
    st.write(f"**Location:** {location}")
    
    # Display description in a box with scrollable height
    # Display description in a box with scrollable height
    st.write("**Description:**")
    st.text_area("Job Description Text", value=description, height=200, disabled=True, key="jd_description", label_visibility="hidden")
    
    # Required Skills
    must_have = jd.get('must_have', []) if isinstance(jd, dict) else []
    if must_have:
        st.write("**Required Skills:**")
        for skill in must_have:
            st.markdown(f"- {skill}")
    
    # Preferred Skills
    good_to_have = jd.get('good_to_have', []) if isinstance(jd, dict) else []
    if good_to_have:
        st.write("**Preferred Skills:**")
        for skill in good_to_have:
            st.markdown(f"- {skill}")

def display_evaluation_results(result: EvaluationResult) -> None:
    """Display evaluation results in a formatted way"""
    st.write("### 📊 Evaluation Results")
    
    # Display scores in metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Match", f"{result.get('score', 0)}%")
    with col2:
        st.metric("Technical Score", f"{result.get('technical_score', 0)}%")
    with col3:
        st.metric("AI Score", f"{result.get('gemini_score', 0)}%")
    
    # Verdict with appropriate color
    verdict = result.get('verdict', 'No verdict')
    verdict_color = {
        'High': 'green',
        'Medium': 'orange',
        'Low': 'red'
    }.get(verdict, 'grey')
    st.markdown(f"**Verdict:** :{verdict_color}[{verdict} Match]")
    
    # Display strengths and improvements side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💪 Key Strengths")
        strengths = result.get('key_strengths', [])
        for strength in strengths:
            st.markdown(f"✓ {strength}")
    
    with col2:
        st.markdown("#### 🎯 Areas for Improvement")
        improvements = result.get('areas_for_improvement', [])
        for area in improvements:
            st.markdown(f"• {area}")
    
    # Missing skills section
    st.markdown("#### ❗ Missing Skills")
    missing = result.get('missing_skills', [])
    for skill in missing:
        st.markdown(f"◦ {skill}")
    
    # Suggestions section
    st.markdown("#### 💡 Recommendations")
    suggestions = result.get('suggestions', [])
    for suggestion in suggestions:
        st.markdown(f"→ {suggestion}")
    
    # Detailed feedback in an expander
    with st.expander("📝 See Detailed Analysis"):
        st.markdown(result.get('detailed_feedback', 'No detailed feedback available.'))

st.title("Resume Evaluation System")
st.markdown("---")

# Create two columns for the main layout
left_col, right_col = st.columns([1, 1], gap="large")

def get_selected_job() -> Optional[JobDescription]:
    """Get the selected job description from the available jobs"""
    try:
        # Get all job descriptions
        jds = get_jds()
        
        if isinstance(jds, dict) and "error" in jds:
            st.error(f"Error fetching JDs: {jds['error']}")
            return None
            
        if not isinstance(jds, list) or not jds:
            st.warning("No job descriptions available. Please add some jobs first.")
            return None
            
        # Select Job Description Section
        job_titles = []
        valid_jds = []
        
        for jd in jds:
            if isinstance(jd, dict):
                title = jd.get('title', 'Untitled')
                location = jd.get('location', 'No location')
                job_titles.append(f"{title} ({location})")
                valid_jds.append(jd)
        
        if not job_titles:
            st.warning("No valid job descriptions found.")
            return None
            
        selected_index = st.radio(
            "Available Positions", 
            range(len(job_titles)), 
            format_func=lambda x: job_titles[x],
            key="job_selector"
        )
        
        if 0 <= selected_index < len(valid_jds):
            return valid_jds[selected_index]
    except Exception as e:
        st.error(f"Error getting selected job: {str(e)}")
        return None
    return None

# Main layout
st.title("Resume Evaluation System")
st.markdown("---")

# Create two columns for the main layout
left_col, right_col = st.columns([1, 1], gap="large")

# Left column - Job Description
with left_col:
    st.header("Job Description")
    selected_jd = get_selected_job()
    if selected_jd:
        display_job_details(selected_jd)

# Right column - Resume Upload and Evaluation
with right_col:
    st.header("Resume Evaluation")
    
    if not selected_jd:
        st.info("👈 Please select a job description from the left panel to begin evaluation.")
        st.stop()
        
    description = str(selected_jd.get('description', ''))  # Ensure string type
    
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF/DOC/DOCX)", 
        type=['pdf', 'doc', 'docx'],
        key="resume_uploader"
    )
    
    if uploaded_file:
        try:
            # Preview the uploaded resume
            st.write("### 📄 Resume Preview")
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_docx(uploaded_file)
            st.text_area("Resume Content", value=text, height=200, disabled=True, key="resume_preview", label_visibility="hidden")
            
            # Evaluation button
            if st.button("🔍 Evaluate Resume", key="evaluate_button"):
                with st.spinner("Analyzing resume against job requirements..."):
                    result = upload_resume(uploaded_file, description)
                    
                    if isinstance(result, dict):
                        if "error" in result:
                            st.error(f"Error evaluating resume: {result['error']}")
                        else:
                            st.success("✅ Evaluation Complete!")
                            # Cast result to EvaluationResult type for display
                            display_evaluation_results(result)
                    else:
                        st.error("Invalid response from server")
                        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("👈 Please upload a resume in PDF, DOC, or DOCX format.")