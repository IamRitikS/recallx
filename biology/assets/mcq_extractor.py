import sys
import re
import pdfplumber
import json
import time
from tqdm import tqdm
import google.generativeai as genai

# =========================
# CONFIG
# =========================
gemini_ai_api_key = None
model = None
MODEL = "gpt-4o-mini"
CHUNK_SIZE = 800   # words per chunk
DELAY = 1          # seconds between API calls (avoid rate limits)

# =========================
# 0. Setup configuration
# =========================
def load_config():
    global gemini_ai_api_key
    global model
    try:
        with open("gemini_ai_api_key.key", "r") as file:
            gemini_ai_api_key = file.read().strip()  # .strip() removes hidden newlines
            print(gemini_ai_api_key)
    except FileNotFoundError:
        print("Error: key file not found.")
        exit(0)
    genai.configure(api_key=gemini_ai_api_key)
    genai.list_models()
    model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# 1. Extract text from PDF
# =========================
def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# =========================
# 2. Chunk text
# =========================
def chunk_text(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    
    return chunks


# =========================
# 3. Build prompt
# =========================
def build_prompt(chunk):
    return f"""
You are an expert NEET biology MCQ generator.

Convert the following text into MAXIMUM possible MCQs.

Strict Requirements:
- Cover EVERY factual detail
- Include tricky questions
- Include assertion-reason questions
- Include statement-based MCQs
- Include close/confusing distractors
- Avoid repetition
- Ensure accuracy

Return ONLY JSON in this format:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "A",
    "type": "factual/assertion/statement",
    "level": "easy/medium/difficult"
  }}
]

TEXT:
{chunk}
"""


# =========================
# 4. Call AI
# =========================
def generate_mcqs(chunk):
    try:
        response = model.generate_content(build_prompt(chunk))
        return response.text

    except Exception as e:
        print(f"Error: {e}")
        return None


# =========================
# 5. Parse JSON safely
# =========================
def safe_parse(mcq_text):
    if not mcq_text:
        return []

    try:
        # 🔥 Step 1: Remove markdown
        cleaned = re.sub(r"```json", "", mcq_text)
        cleaned = re.sub(r"```", "", cleaned)

        # 🔥 Step 2: Find ALL JSON arrays
        json_blocks = re.findall(r"\[.*?\]", cleaned, re.DOTALL)

        all_mcqs = []

        for block in json_blocks:
            try:
                parsed = json.loads(block)
                if isinstance(parsed, list):
                    all_mcqs.extend(parsed)
            except:
                continue

        return all_mcqs

    except Exception as e:
        print("❌ JSON parse failed:", e)
        return []

# =========================
# 6. Full pipeline
# =========================
def pdf_to_mcqs(pdf_path):
    print("📄 Extracting text...")
    text = extract_text(pdf_path)

    print("✂️ Chunking text...")
    chunks = chunk_text(text)

    all_mcqs = []

    print(f"🤖 Generating MCQs for {len(chunks)} chunks...\n")

    for chunk in tqdm(chunks):
        mcq_text = generate_mcqs(chunk)
        if mcq_text:
            print(mcq_text)
            parsed = safe_parse(mcq_text)
            all_mcqs.extend(parsed)

        time.sleep(DELAY)

    return all_mcqs


# =========================
# 7. Save output
# =========================
def save_mcqs(mcqs, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mcqs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(mcqs)} MCQs to {filename}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    if len(sys.argv) > 2:
        pdf_path = sys.argv[1]
        print("Input file path provided:", pdf_path)

        mcqs_path = sys.argv[2]
        print("Output file path provided:", mcqs_path)

        load_config()
        mcqs = pdf_to_mcqs(pdf_path)
        save_mcqs(mcqs, mcqs_path)
    else:
        print("Sufficient arguments not provided.")