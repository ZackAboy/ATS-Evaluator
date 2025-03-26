<h1 align="center">📄 Resume ATS Evaluator</h1>

<p align="center">
  An AI-powered resume evaluator and enhancer built with Streamlit, Gemini, and GPT.
</p>

---

## 🚀 Overview
This app helps job seekers optimize their resumes by comparing them against any job description using the power of Large Language Models (LLMs). It provides:
- 🔍 ATS-style scoring & keyword analysis
- 🤖 Side-by-side comparison using **Gemini** and **GPT-4o** (OpenAI)
- 📄 Cover letter generation
- ✍️ Resume improvement suggestions

---

## 🧠 Tech Stack
- **Frontend/UI:** Streamlit
- **LLMs:** Google Gemini 2.0 Flash & OpenAI GPT-4o (via `o3-mini`)
- **PDF Parsing:** PyPDF2
- **Environment Config:** python-dotenv

---

## ✨ Features

### ✅ Resume vs Job Description Analysis
Upload your resume and paste the job description. The app:
- Parses your resume
- Evaluates keyword match and missing skills
- Provides suggestions to improve your resume
- Compares Gemini and GPT responses side-by-side

### 📬 Cover Letter Generator
Generates a custom, markdown-formatted cover letter that:
- Is ATS-optimized
- Has a human tone
- Highlights relevant skills in bullet points
- Begins directly with "Dear..." (no boilerplate fluff!)

### 📝 Resume Point Generator
Get ready-to-paste bullet points crafted by LLMs to:
- Match the job description better
- Improve ATS keyword matching
- Align with industry-standard phrasing

### 🔀 Model Selector
Choose between **Gemini** or **GPT-4o** for generation tasks.

---

## 📸 App Demo
> _Add screenshots or GIFs of the UI here once deployed_

---

## 🛠 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/resume-ats-evaluator.git
cd resume-ats-evaluator
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup your environment variables
Create a `.env` file with your API keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
resume-ats-evaluator/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Project dependencies
├── .env.example           # API key template
└── README.md              # This file
```

