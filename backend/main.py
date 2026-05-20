from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

# Import your custom functions
from pdf_extractor import extract_rules
from ai_integration import get_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Read and extract the text using your fixed extractor
    content = await file.read()
    extracted_text = extract_rules(content)
    with open("telemetry.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
    return {"message": "Rulebook ingested and saved to hard drive. Pit wall is online."}

@app.post("/api/ask")
async def ask_question(question: str = Form(...)):
    if not os.path.exists("telemetry.txt"):
        return {"error": "Negative. No telemetry loaded. Upload rulebook first."}
    with open("telemetry.txt", "r", encoding="utf-8") as f:
        saved_text = f.read()
    answer = get_response(saved_text, question)
    return {"response": answer}