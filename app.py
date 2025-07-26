import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF

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
    st.error(f"Error configuring AI model: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error configuring the AI model: {e}")
    st.stop()

# --- Text Extraction Function ---
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        if not text.strip():
            st.error("Error: This PDF contains no text. It might be an image-based PDF.")
            return None
        return text
    except Exception as e:
        st.error("An error occurred while reading the PDF.")
        st.exception(e)
        return None

# --- Main Application UI ---
st.title("AI-Powered Resume & Career Analyzer")
st.write("Upload your resume to receive instant feedback, career suggestions, and more.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    if resume_text:
        st.header("Interactive Resume Editor & Analyzer")
        left_column, right_column = st.columns(2)

        # --- LEFT COLUMN: The Editor ---
        with left_column:
            st.subheader("Edit Your Resume Text")
            edited_text = st.text_area(
                "Resume Content", 
                resume_text, 
                height=600,
                label_visibility="collapsed"
            )

        # --- RIGHT COLUMN: The Live Analysis ---
        with right_column:
            st.subheader("Live AI Feedback")
            if st.button("Update Analysis"):
                with st.spinner("Analyzing updated text..."):
                    live_editor_prompt = f"""
                    You are a strict but fair hiring manager. Analyze the following resume text.
                    Provide a 'Resume Score' out of 100.
                    Then, give bullet-pointed feedback on:
                    - Clarity and Impact: Are the achievements quantified?
                    - Formatting: Is it easy to read?
                    - Biased Language: Flag any non-inclusive language and suggest alternatives.
                    
                    Format the entire response in Markdown.
                    ---
                    Resume Text:
                    {edited_text}
                    ---
                    """
                    try:
                        response = model.generate_content(live_editor_prompt)
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {e}")

        st.divider()

        # --- OPPORTUNITY SCORE FEATURE ---
        st.header("Career Opportunity Score 🔎")
        target_job = st.text_input("Enter Your Target Job Title (e.g., 'Data Scientist')")

        if st.button("Find My Opportunities"):
            if target_job:
                with st.spinner("Scanning for career paths..."):
                    opportunity_prompt = f"""
                    Based on the resume below, analyze the candidate's fit for the target role of "{target_job}".
                    Then, suggest and score three career opportunities:
                    1. **Obvious Fit:** The most direct career path that matches the resume.
                    2. **Related Fit:** A similar role in a different industry or a slightly different function.
                    3. **Wildcard Fit:** An unexpected but high-potential role that leverages the candidate's unique skills.
                    For each, provide an 'Opportunity Score' from 1-100 and a one-sentence justification.
                    ---
                    Resume Text:
                    {edited_text}
                    ---
                    """
                    try:
                        response = model.generate_content(opportunity_prompt)
                        st.subheader("Your Personalized Career Paths")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {e}")
            else:
                st.warning("Please enter a target job title to find opportunities.")