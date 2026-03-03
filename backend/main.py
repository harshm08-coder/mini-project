from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import analyze_resume
import time
import pdfplumber
import docx

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing text-based endpoint
class ResumeRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: ResumeRequest):
    try:
        start_time = time.time()
        result = analyze_resume(request.text)
        end_time = time.time()
        return {
            "analysis": result,
            "response_time": round(end_time - start_time, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW FILE UPLOAD ENDPOINT ---
@app.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    """
    Accepts a resume file (.pdf, .docx, .txt), extracts text, and sends it to AI for analysis.
    """
    try:
        start_time = time.time()

        # Extract text from PDF
        text = ""
        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        # Extract text from DOCX
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file.file)
            for para in doc.paragraphs:
                text += para.text + "\n"

        # Extract text from TXT
        else:
            text = (await file.read()).decode("utf-8")

        if not text.strip():
            raise HTTPException(status_code=400, detail="File contains no readable text.")

        # Send text to your AI service
        result = analyze_resume(text)

        end_time = time.time()

        return {
            "analysis": result,
            "response_time": round(end_time - start_time, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))