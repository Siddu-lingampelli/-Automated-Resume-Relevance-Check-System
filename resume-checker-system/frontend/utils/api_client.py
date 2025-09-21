import requests
import streamlit as st
from typing import Dict, Any, List, Union

# Get the backend URL from Streamlit secrets or use localhost for local development
BASE_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

def upload_jd(jd_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        r = requests.post(f"{BASE_URL}/jd/upload", json=jd_data)
        r.raise_for_status()  # Raise an error for bad status codes
        return r.json()
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_jds() -> Union[List[Dict[str, Any]], Dict[str, str]]:
    try:
        r = requests.get(f"{BASE_URL}/jd/list")
        r.raise_for_status()  # Raise an error for bad status codes
        return r.json()
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def upload_resume(file, jd_text: str):
    try:
        # Create file data with proper content type
        if file.type == "application/pdf":
            content_type = "application/pdf"
        elif file.type == "application/msword":
            content_type = "application/msword"
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            content_type = "application/octet-stream"

        files = {"file": (file.name, file, content_type)}
        data = {"jd": jd_text}
        
        r = requests.post(f"{BASE_URL}/resume/evaluate", files=files, data=data)
        r.raise_for_status()  # Raise an error for bad status codes
        return r.json()
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid response: {str(e)}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}