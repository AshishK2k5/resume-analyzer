✨ AI Career Toolkit 
Welcome to the official repository for the AI Career Toolkit, a project by Team Resume_Rangers for INNOHACK 2.0. This all-in-one web application is designed to be a personal co-pilot for the modern job seeker, leveraging the power of generative AI to provide expert-level career guidance.

🚀 Try the Live App
Our application is fully deployed and accessible to everyone.

➡️ Click here to try the live AI Career Toolkit - https://resume-analyzer-fsnawgnxuaxz8rwqvarjy.streamlit.app/

📸 Application Preview
<img width="1919" height="1079" alt="HackathonPro" src="https://github.com/user-attachments/assets/b09e3d79-9412-4da1-b00d-8451fab00f54" />

🎯 The Problem
The modern job hunt is broken. Talented candidates are often filtered out by automated systems (ATS), lack access to expert career advice, and suffer from application fatigue. Our project directly tackles these pain points.

✨ Core Features
Our platform integrates a full suite of tools to empower job seekers:

📄 Resume Feedback & ATS Analysis: Get an instant score and detailed feedback from an AI trained as a top-tier recruiter. Run a specific ATS analysis against a job description to identify and fix critical keyword gaps.

✨ One-Click Resume Enhancement: Automatically rewrite an entire resume for maximum impact, using the STAR method and professional, action-oriented language.

🗺️ Personalized Learning Roadmap: Receive a custom learning plan to bridge skill gaps for a target career, complete with course recommendations, free resources, and portfolio project ideas.

🎯 Career Insights & Market Trends: Discover unique job roles that match your skills—including "wildcard" suggestions—and view an AI-generated forecast of future market demand for your target career, complete with a data visualization.

✍️ AI Cover Letter Generator: Automate the most tedious part of job applications by generating a tailored, professional cover letter from your resume and a job description in seconds.

🛠️ Tech Stack
This project was built using a modern, efficient, and powerful tech stack:

Core Language: Python

Frontend Framework: Streamlit

AI Engine: Google Gemini API (gemini-1.5-flash)

Data Processing & Visualization: Pandas, PyMuPDF, python-docx

Version Control & Deployment: Git, GitHub, Streamlit Community Cloud

🔧 How to Run Locally
To run this project on your own machine, please follow these steps:

Clone the repository:

git clone https://github.com/AshishK2k5/resume-analyzer.git
cd resume-analyzer

Create and activate a virtual environment:

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Install the required libraries:

pip install -r requirements.txt

Set up your API key:

Create a folder named .streamlit in the main project directory.

Inside that folder, create a file named secrets.toml.

Add your Google Gemini API key to the file in this format:

GEMINI_API_KEY = "YOUR_API_KEY_HERE"

Run the application:

streamlit run app.py
