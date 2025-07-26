import streamlit as st
import google.generativeai as genai
import fitz  # instead of PyMuPDF

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# --- AI Model Configuration ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error configuring AI model. Please check your API key.")
    st.stop()

# --- Text Extraction Function ---
def extract_text_from_pdf(pdf_file):
    try:
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text("text") for page in doc)
        pdf_file.seek(0)  # Reset pointer in case file is needed again
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None
    

# app.py (continued)

# --- Main Application UI ---
st.title("AI-Powered Resume & Career Analyzer")
st.write("Upload your resume to receive instant feedback, career suggestions, and more.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File Uploaded Successfully!")
    resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text:
        st.header("Your Extracted Resume Text")
        st.text_area("Resume Content", resume_text, height=300)

        if st.button("Analyze My Resume"):
            with st.spinner("Our AI is analyzing your resume... This may take a moment."):
                prompt = f"""
                You are an expert career coach. Analyze the following resume text and provide:
                1. A brief summary.
                2. Three key strengths.
                3. Three areas for improvement.
                Format the response in Markdown.

                Resume Text:
                ---
                {resume_text}
                ---
                """
                response = model.generate_content(prompt)
                st.header("Analysis Results")
                st.markdown(response.text)