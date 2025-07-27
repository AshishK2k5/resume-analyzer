import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import re
import pandas as pd
import docx

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Career Toolkit",
    page_icon="🏆",
    layout="wide"
)

# --- Initialize Session State ---
if 'general_result' not in st.session_state:
    st.session_state.general_result = ""
if 'ats_result' not in st.session_state:
    st.session_state.ats_result = ""
if 'roadmap_result' not in st.session_state:
    st.session_state.roadmap_result = ""
if 'opportunity_result' not in st.session_state:
    st.session_state.opportunity_result = ""
if 'enhanced_resume' not in st.session_state:
    st.session_state.enhanced_resume = ""
if 'cover_letter_result' not in st.session_state:
    st.session_state.cover_letter_result = ""
if 'trends_result' not in st.session_state:
    st.session_state.trends_result = None
if 'app_started' not in st.session_state:
    st.session_state.app_started = False

# --- AI Model Configuration ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    generation_config = genai.types.GenerationConfig(temperature=0.2)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error configuring AI model: {e}")
    st.stop()

# --- Helper Functions ---
def extract_text_from_file(file):
    try:
        if file.name.endswith('.pdf'):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in doc)
        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            st.error("Unsupported file type.")
            return None
        
        if not text.strip():
            st.error("Error: This file contains no text.")
            return None
        return text
    except Exception as e:
        st.error("An error occurred while reading the file.")
        st.exception(e)
        return None

# --- Main Application UI ---
st.title("AI-Powered Career Toolkit 🏆")
st.write("Your all-in-one assistant for resume feedback, career planning, and job applications.")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    st.session_state.app_started = True

if not st.session_state.app_started:
    st.info("💡 Upload your resume to unlock your personalized AI career toolkit!")
    st.subheader("Features:")
    st.markdown("""
    - **📄 Resume Feedback:** Get a general score or a specific ATS score against a job description.
    - **✨ Resume Enhancement:** Rewrite your resume for maximum impact with one click.
    - **🗺️ Learning Roadmap:** Receive a personalized plan to bridge your skill gaps for a target role.
    - **🎯 Career Insights:** Discover unique job roles and future market trends for your desired career.
    - **✍️ Cover Letter Generator:** Create a tailored cover letter for any job description.
    """)

if st.session_state.app_started and uploaded_file is not None:
    resume_text = extract_text_from_file(uploaded_file)
    if resume_text:
        st.header("Interactive Resume Editor & Toolkit")
        
        target_job = st.text_input("Enter a Target Job Title for Analysis (used across all tabs)")

        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Edit Your Resume Text")
            edited_text = st.text_area(
                "Resume Content",
                resume_text,
                height=700,
                label_visibility="collapsed"
            )

        with right_column:
            tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume Feedback", "🗺️ Learning Roadmap", "🎯 Career Insights", "✍️ Cover Letter"])

            with tab1:
                st.subheader("Resume Analysis")
                
                st.markdown("##### Get General Feedback")
                st.info("Get an overall score and general feedback from our AI recruiter.")
                if st.button("Run General Analysis"):
                    with st.spinner("Running general analysis..."):
                        live_editor_prompt = f"""
                        You are a top-tier executive recruiter from a leading tech firm like Google or Goldman Sachs, known for your brutally honest but invaluable feedback. Your task is to conduct a professional-grade analysis of the following resume.
                        **Analysis Steps:**
                        1.  **Headline:** Provide a single, powerful headline that describes the candidate's professional identity.
                        2.  **Overall Resume Score:** Provide a score on its own line in the format: `Resume Score: [score]/100`.
                        3.  **Candidate Archetype:** Classify the candidate into a professional archetype (e.g., 'The Specialist', 'The Generalist', 'The Rising Star', 'The Career Transitioner') and provide a one-sentence justification.
                        4.  **Verdict:** In one bolded sentence, state whether you would move forward with this candidate for an interview and why.
                        5.  **Strengths vs. Weaknesses:** Create a two-column Markdown table. The left column will list the top 3 strengths. The right column will list the top 3 weaknesses.
                        6.  **Actionable Improvements:** Provide a bulleted list of the three most critical, specific, and actionable pieces of advice the candidate can implement right now.
                        **Perform this analysis on the following resume text:**
                        ---
                        {edited_text}
                        ---
                        """
                        try:
                            response = model.generate_content(live_editor_prompt, generation_config=generation_config)
                            st.session_state.general_result = response.text
                            st.session_state.ats_result = "" 
                        except Exception as e:
                            st.error(f"An error occurred during analysis: {e}")
                
                if st.session_state.general_result:
                    response_text = st.session_state.general_result
                    score = 0
                    match = re.search(r'(\d+)\s*/\s*100', response_text)
                    if match:
                        score = int(match.group(1))
                        st.metric(label="General Score", value=f"{score} / 100")
                    with st.expander("See Detailed General Feedback"):
                        st.markdown(response_text)

                st.divider()

                st.markdown("##### Get ATS Compatibility Score")
                st.info("Paste a job description to get a specific ATS score and keyword analysis.")
                job_desc_for_ats = st.text_area("Paste the Job Description here for ATS Analysis")
                if st.button("Run ATS Analysis", disabled=not job_desc_for_ats):
                    with st.spinner("Running ATS simulation..."):
                        ats_prompt = f"""
                        You are an advanced Applicant Tracking System (ATS) combined with an expert HR recruiter. Your primary goal is to analyze the provided resume against the provided job description.
                        **Analysis Steps:**
                        1.  **ATS Compatibility Score:** Provide an ATS compatibility score on its own line in the format: `ATS Score: [score]/100`.
                        2.  **Keyword Analysis:** Compare the resume to the job description. Create a two-column Markdown table. The left column will list the top 5-7 most important keywords missing from the resume. The right column will list the top keywords that are correctly included.
                        3.  **Formatting Check:** Analyze the resume for any formatting that could be problematic for an ATS.
                        4.  **Actionable Feedback:** Provide a bulleted list of the top 3 most critical changes the user must make to improve their ATS score for this specific job.
                        **Perform this ATS analysis:**
                        ---
                        **USER'S RESUME:**
                        {edited_text}
                        ---
                        **TARGET JOB DESCRIPTION:**
                        {job_desc_for_ats}
                        ---
                        """
                        try:
                            response = model.generate_content(ats_prompt, generation_config=generation_config)
                            st.session_state.ats_result = response.text
                            st.session_state.general_result = "" 
                        except Exception as e:
                            st.error(f"An error occurred during analysis: {e}")
                elif not job_desc_for_ats:
                    st.warning("Please paste a job description to enable ATS Analysis.")
                
                if st.session_state.ats_result:
                    response_text = st.session_state.ats_result
                    score = 0
                    match = re.search(r'(\d+)\s*/\s*100', response_text)
                    if match:
                        score = int(match.group(1))
                        st.metric(label="ATS Score", value=f"{score} / 100")
                    with st.expander("See Detailed ATS Feedback"):
                        st.markdown(response_text)

                st.divider()

                if st.button("✨ Generate Enhanced Version"):
                    with st.spinner("Rewriting your resume for maximum impact..."):
                        enhancement_prompt = f"""
                        You are a world-class resume writer and editor for a top tech company. Your task is to take the user's resume text and rewrite it from scratch to be as powerful, professional, and impactful as possible.
                        **Instructions:**
                        1.  Preserve all original facts, job titles, companies, and dates. Do not invent new experiences.
                        2.  Rewrite every bullet point to use the STAR (Situation, Task, Action, Result) method. Emphasize quantifiable results.
                        3.  Ensure the language is professional, confident, and uses strong action verbs.
                        4.  Correct any spelling or grammar mistakes.
                        5.  Structure the output in a clean, standard resume format.
                        **Rewrite this resume:**
                        ---
                        {edited_text}
                        ---
                        """
                        try:
                            response = model.generate_content(enhancement_prompt, generation_config=generation_config)
                            st.session_state.enhanced_resume = response.text
                        except Exception as e:
                            st.error(f"An error occurred during enhancement: {e}")

                if st.session_state.enhanced_resume:
                    with st.expander("View AI-Enhanced Resume Version", expanded=True):
                        st.code(st.session_state.enhanced_resume)
                        st.download_button(
                            label="Download Enhanced Resume as TXT",
                            data=st.session_state.enhanced_resume,
                            file_name="enhanced_resume.txt",
                            mime="text/plain"
                        )

            with tab2:
                st.subheader("Your Personalized Learning Roadmap")
                roadmap_personalization = st.text_area("Add any personalizations (e.g., 'create a 60-day plan', 'focus on free courses')")
                if st.button("Generate My Roadmap", disabled=not target_job):
                    with st.spinner(f"Building your roadmap for {target_job}..."):
                        roadmap_prompt = f"""
                        You are a world-class academic advisor and career coach from an elite university's career services department. Your task is to create a personalized, flexible learning roadmap for a user who wants to become a "{target_job}".
                        **Instructions:**
                        1.  Analyze the user's resume to identify their current skill level.
                        2.  Identify the top 3 most critical **technical skill gaps**.
                        3.  Identify the single most important **soft skill** they should develop for this role.
                        4.  For each of the 3 technical gaps, create a "Learning Module" containing a concept, a recommended paid course, a free resource, and a portfolio project idea.
                        5.  Create a final "Soft Skill Development" module with actionable advice.
                        6.  **Personalization:** The user has provided the following special request: "{roadmap_personalization}". You must incorporate this request into the plan.
                        **Generate this roadmap based on the following resume text:**
                        ---
                        {edited_text}
                        ---
                        """
                        try:
                            roadmap_response = model.generate_content(roadmap_prompt, generation_config=generation_config)
                            st.session_state.roadmap_result = roadmap_response.text
                        except Exception as e:
                            st.error(f"An error occurred during roadmap generation: {e}")
                elif not target_job:
                    st.warning("Please enter a Target Job Title above to enable this feature.")

                if st.session_state.roadmap_result:
                    st.markdown(st.session_state.roadmap_result)

            with tab3:
                st.subheader("Career Opportunity & Market Insights")
                if st.button("Find My Opportunities", disabled=not target_job):
                    with st.spinner("Scanning for career paths..."):
                        opportunity_prompt = f"""
                        You are a seasoned career strategist and futurist. Analyze the resume for the target role of "{target_job}".
                        **Analysis:**
                        1.  **Fit Score for Target Role:** Provide a "Fit Score" from 1-100 and a brief justification.
                        2.  **Recruiter's Red Flag:** Identify the single biggest potential "red flag" a recruiter might see in this resume for this specific role and suggest how to mitigate it.
                        3.  **Career Suggestions:** Suggest and score three career opportunities:
                            * **Obvious Fit:** The most direct path. Provide an 'Opportunity Score' (1-100) and justification.
                            * **Related Fit:** A similar role in a different industry. Provide score and justification.
                            * **Wildcard Fit:** An unexpected but high-potential role. Provide score and justification.
                        **Perform this analysis on the following resume text:**
                        ---
                        {edited_text}
                        ---
                        """
                        try:
                            response = model.generate_content(opportunity_prompt, generation_config=generation_config)
                            st.session_state.opportunity_result = response.text
                        except Exception as e:
                            st.error(f"An error occurred during analysis: {e}")
                elif not target_job:
                    st.warning("Please enter a Target Job Title above to enable this feature.")

                if st.session_state.opportunity_result:
                    st.markdown(st.session_state.opportunity_result)

                st.divider()
                st.subheader("Job Market Future Trends")
                if st.button("Analyze Market Trends", disabled=not target_job):
                    with st.spinner(f"Analyzing future trends for a {target_job}..."):
                        trends_prompt = f"""
                        Act as a senior market analyst from Gartner providing a direct report.
                        Your task is to generate a job market trend analysis for the role of "{target_job}".
                        **Output Requirements:**
                        1.  **Executive Summary:** A concise, one-paragraph summary of the future outlook for this role. This summary must describe strong, positive growth.
                        2.  **Data Table:** A Markdown table with columns 'Year' and 'Demand Growth (%)', showing plausible data for the last 3 years and a forecast for the next 3.
                        **CRITICAL RULE:** For a high-growth role like AI Engineer or Data Scientist, the numbers in the 'Demand Growth (%)' column MUST show a generally increasing trend for future years. Do not show a declining trend. All numbers must be positive.
                        **Constraint:**
                        - Do not include any conversational introductions, questions, or conclusions.
                        - Your entire output must consist of only the Executive Summary and the Markdown Data Table.
                        Generate the report now.
                        """
                        try:
                            response = model.generate_content(trends_prompt, generation_config=generation_config)
                            st.session_state.trends_result = response.text
                        except Exception as e:
                            st.error(f"An error occurred during trend analysis: {e}")
                elif not target_job:
                    st.warning("Please enter a Target Job Title above to enable this feature.")

                if st.session_state.trends_result:
                    trends_text = st.session_state.trends_result
                    st.markdown(trends_text)
                    try:
                        table_rows = re.findall(r'\|\s*(\d{4})\s*\|\s*([\d.-]+)\s*\|', trends_text)
                        if table_rows:
                            df = pd.DataFrame(table_rows, columns=['Year', 'Demand Growth (%)'])
                            df['Demand Growth (%)'] = pd.to_numeric(df['Demand Growth (%)'])
                            df = df.set_index('Year')
                            st.line_chart(df)
                        else:
                            st.info("Could not find table data in the response to generate a graph.")
                    except Exception as e:
                        st.info("Could not generate a graph from the analysis.")
            
            with tab4:
                st.subheader("AI Cover Letter Generator")
                job_description = st.text_area("Paste the job description here")
                if st.button("Generate Cover Letter", disabled=not job_description):
                    with st.spinner("Writing a tailored cover letter..."):
                        cover_letter_prompt = f"""
                        You are a professional career writer. Your task is to write a concise and compelling cover letter and suggest an email subject line.
                        **Instructions:**
                        1.  Write a professional email subject line for the application.
                        2.  Write a cover letter (no more than 250 words) that highlights the top 2-3 most relevant skills from the resume that match the job description.
                        **User's Resume:**
                        ---
                        {edited_text}
                        ---
                        **Target Job Description:**
                        ---
                        {job_description}
                        ---
                        """
                        try:
                            response = model.generate_content(cover_letter_prompt, generation_config=generation_config)
                            st.session_state.cover_letter_result = response.text
                        except Exception as e:
                            st.error(f"An error occurred during cover letter generation: {e}")
                elif not job_description:
                    st.warning("Please paste a job description to enable this feature.")

                if st.session_state.cover_letter_result:
                    st.code(st.session_state.cover_letter_result)
                    st.download_button(
                        label="Download Cover Letter as TXT",
                        data=st.session_state.cover_letter_result,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )