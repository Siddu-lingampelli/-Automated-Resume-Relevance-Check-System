# -*- coding: utf-8 -*-
import streamlit as st
from utils.api_client import upload_jd, get_jds
import PyPDF2
import docx
import io

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

st.title("Job Descriptions")

# Upload new JD section
st.subheader("Upload New Job Description")

# File upload option
uploaded_file = st.file_uploader("Upload Job Description (PDF/DOC/DOCX)", type=['pdf', 'doc', 'docx'])
extracted_text = ""

if uploaded_file:
    try:
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            extracted_text = extract_text_from_docx(uploaded_file)
        st.success("✅ File uploaded and text extracted successfully!")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

with st.form("jd_form"):
    title = st.text_input("Job Title")
    description = st.text_area("Job Description", value=extracted_text, height=200)
    location = st.text_input("Location (optional)")
    must_have = st.text_area("Must Have Skills (one per line)", height=100)
    good_to_have = st.text_area("Good to Have Skills (one per line)", height=100)
    
    submitted = st.form_submit_button("Upload Job Description")
    if submitted:
        must_have_list = [skill.strip() for skill in must_have.split("\n") if skill.strip()]
        good_to_have_list = [skill.strip() for skill in good_to_have.split("\n") if skill.strip()]
        
        jd_data = {
            "title": title,
            "description": description,
            "location": location if location else None,
            "must_have": must_have_list,
            "good_to_have": good_to_have_list
        }
        
        response = upload_jd(jd_data)
        if "error" in response:
            st.error(f"Error uploading JD: {response['error']}")
        else:
            st.success("✅ Job Description uploaded successfully!")

# View existing JDs section
st.subheader("Existing Job Descriptions")
jds = get_jds()
if isinstance(jds, dict) and "error" in jds:
    st.error(f"Error fetching JDs: {jds['error']}")
else:
    st.button("Refresh Job Listings")
    for jd in jds:
        try:
            with st.expander(jd.get("title", "Untitled Job")):
                st.write("Description:", jd.get("description", "No description provided"))
                if jd.get("location"):
                    st.write("Location:", jd["location"])
                
                must_have_skills = jd.get("must_have", [])
                if must_have_skills:
                    st.write("Must Have Skills:")
                    for skill in must_have_skills:
                        st.write(f"- {skill}")
                
                good_to_have_skills = jd.get("good_to_have", [])
                if good_to_have_skills:
                    st.write("Good to Have Skills:")
                    for skill in good_to_have_skills:
                        st.write(f"- {skill}")
        except Exception as e:
            st.error(f"Error displaying job: {str(e)}")