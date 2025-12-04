import streamlit as st
import fitz
from groq import Groq

# ← ВСТАВЬ СВОЙ КЛЮЧ СЮДА ↓↓↓
client = Groq(api_key="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")

SYSTEM_PROMPT = """
You are a cover letter template generator bot. Your only task is to generate a clean English cover letter template based on the user's resume.

Rules:
- Generate ONLY the template text, no comments or questions.
- Use [placeholders] like [Position], [Company Name], etc.
- If no resume — reply: "Hi! Please send your resume (text or PDF) to generate the template."
"""

def extract_resume(input_data):
    if isinstance(input_data, str):
        return input_data
    else:
        try:
            doc = fitz.open(stream=input_data.read(), filetype="pdf")
            return "".join(page.get_text() for page in doc)
        except:
            return "Error reading PDF"

def generate_template(resume_text):
    response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Resume:\n{resume_text}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()

st.title("Cover Letter Bot")

input_text = st.text_area("Paste resume here", height=200)
uploaded_file = st.file_uploader("Or upload PDF", type=["pdf"])

if input_text or uploaded_file:
    resume = extract_resume(input_text or uploaded_file)
    with st.spinner("Generating..."):
        template = generate_template(resume)
    st.markdown(template)
else:
    st.info("Hi! Please send your resume (text or PDF) to generate the template.")
