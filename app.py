import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from openai import OpenAI
import json
import ast
import re


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Gemini Input Parsing
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

#GPT input parsing
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "system", "content": "You are an expert ATS evaluation system for tech resumes."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

def get_custom_response(prompt_template, resume_text, jd_text, model_choice):
    full_prompt = prompt_template.format(text=resume_text, jd=jd_text)
    if model_choice == "Gemini":
        return get_gemini_response(full_prompt)
    else:
        return get_gpt_response(full_prompt)
    
#Response Parsing (JSON)
def clean_json_response(raw_response):
    # Remove Markdown code fences if present
    cleaned = re.sub(r"^```.*?\n", "", raw_response.strip())  # Remove starting ```
    cleaned = re.sub(r"\n```$", "", cleaned)                 # Remove ending ```
    return cleaned

def parse_json_safe(raw_response):
    try:
        cleaned = clean_json_response(raw_response)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            # Handle case like GPT giving stringified lists
            return ast.literal_eval(cleaned)
        except Exception:
            return None
    
# Prompt Templates
input_prompt = """
I need you to act as an expert State of the Art ATS (Applicant Tracking System) with a deep understanding of the tech field, Software roles, AI roles, ML roles, NLP/LLM roles, Data Science/Engineering Roles, etc. You need to evaluate the resume based on the given job description. Assign a match percentage based on the Job Description and any missing words with high accuracy but make sure these missing words are really important and relevant.
resume: {text}
Job-description: {jd}

The response NEEDS to be a single string in the structure:
{{"Description Match":"[int]%", "Missing Keywords":"[]", "Suggestions for improvement":""}}
Please only respond with a valid JSON object. Do not include explanations, markdown, or extra text.
"""
COVER_LETTER_PROMPT = """
I need you to act as an expert Cover Letter Writer with a deep understanding of the tech field, Software roles, AI roles, ML roles, NLP/LLM roles, Data Science/Engineering Roles, etc. You need to evaluate the resume based on the given job description and write a ATS-optimized cover letter tailored for this role.The Cover letter should be very hearty and human, your tone, grammar and vocabulary should be as human as possible. Use bullet points to highlight the main points of relevance, and it should have an intro and conclusion, no need to add writer details, directly start from Dear... . ONLY PROVIDE THE COVER LETTER AND NO ADDITIONAL TEXT, NO EMOJIS Please format the cover letter using proper Markdown.

Resume:
{text}

Job Description:
{jd}
"""
RESUME_POINTS_PROMPT = """
I need you to act as an expert Resume Maker with a deep understanding of the tech field, Software roles, AI roles, ML roles, NLP/LLM roles, Data Science/Engineering Roles, etc. You need to evaluate the resume based on the given job description and suggest specific, ready-to-paste bullet points that can be added or edited into the resume to improve its ATS score and relevance for this job.

Resume:
{text}

Job Description:
{jd}
"""

# Streamlit UI
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .appview-container .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Resume ATS Evaluator")
st.text("This app will help you determine how good your resume is for a given job description and provide suggestions to improve it.")

jd = st.text_area("Paste the Job Description here!")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload your resume as a PDF.")

if st.button("Submit"):
    if uploaded_file and jd:
        st.session_state.submitted = True
        st.session_state.resume_text = input_pdf_text(uploaded_file)
        st.session_state.jd = jd
        final_prompt = input_prompt.format(text=st.session_state.resume_text, jd=jd)

        with st.spinner("Getting Gemini response..."):
            gemini_raw = get_gemini_response(final_prompt)

        with st.spinner("Getting GPT response..."):
            gpt_raw = get_gpt_response(final_prompt)

        try:
            st.session_state.gemini_json = parse_json_safe(gemini_raw)
            st.session_state.gpt_json = parse_json_safe(gpt_raw)

        except Exception as e:
            st.error("Could not parse one of the responses as JSON.")
            st.text("Gemini raw response:")
            st.code(gemini_raw)
            st.text("GPT raw response:")
            st.code(gpt_raw)

if "gemini_json" in st.session_state and "gpt_json" in st.session_state:
    gemini_json = st.session_state.gemini_json
    gpt_json = st.session_state.gpt_json

    st.subheader("🔍 Comparison Results")
    col1, col2 = st.columns(2)
            
    with col1:
        st.markdown("### Gemini Response")
        st.metric("Match %", gemini_json["Description Match"])

        st.markdown("**Missing Keywords:**")
        mk = gemini_json["Missing Keywords"]

        # Try parsing if it's a stringified list
        if isinstance(mk, str):
            try:
                mk = ast.literal_eval(mk)
            except:
                mk = [mk]  # fallback to single-item list

        if isinstance(mk, list):
            if mk:
                st.markdown("- " + "\n- ".join(mk))
            else:
                st.markdown("_None_")
        else:
            st.markdown("_Invalid format_")

        st.markdown("**Suggestions for Improvement:**")
        st.markdown(gemini_json["Suggestions for improvement"])

    with col2:
        st.markdown("### GPT Response")
        st.metric("Match %", gpt_json["Description Match"])

        st.markdown("**Missing Keywords:**")
        mk = gpt_json["Missing Keywords"]

        # Try parsing if it's a stringified list
        if isinstance(mk, str):
            try:
                mk = ast.literal_eval(mk)
            except:
                mk = [mk]  # fallback to single-item list

        if isinstance(mk, list):
            if mk:
                st.markdown("- " + "\n- ".join(mk))
            else:
                st.markdown("_None_")
        else:
            st.markdown("_Invalid format_")

        st.markdown("**Suggestions for Improvement:**")
        st.markdown(gpt_json["Suggestions for improvement"])


if st.session_state.get("submitted"):
    st.markdown("---")
    st.markdown("### ✨ Improve Your Application")

    # Model toggle
    model_choice = st.radio("Choose a model for additional suggestions:", ["Gemini", "GPT"], index=0)

    # Generate Cover Letter
    if st.button("📄 Generate Cover Letter"):
        with st.spinner("Generating cover letter..."):
            st.session_state.cover_letter = get_custom_response(
                COVER_LETTER_PROMPT,
                st.session_state.resume_text,
                st.session_state.jd,
                model_choice
            )

    # Always show if it exists
    if "cover_letter" in st.session_state:
        st.subheader("📬 Generated Cover Letter")
        st.markdown(st.session_state.cover_letter)

    # Generate Resume Bullet Points
    if st.button("📝 Generate Resume Points to Add/Edit"):
        with st.spinner("Crafting impactful resume lines..."):
            st.session_state.resume_suggestions = get_custom_response(
                RESUME_POINTS_PROMPT,
                st.session_state.resume_text,
                st.session_state.jd,
                model_choice
            )

    # Always show if it exists
    if "resume_suggestions" in st.session_state:
        st.subheader("🎯 Suggested Resume Points")
        st.markdown(st.session_state.resume_suggestions)