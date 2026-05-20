from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
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

current_rulebook_text = ""

@app.get("/")
def health_check():
    return {"status": "F1.AI is online"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    raw_rules = extract_rules(content)

    return{
        "filename": file.filename,
        "message" : "file successfully uploaded",
        "charactor_count": len(raw_rules)
    }
@@app.post("/api/ask")
async def ask_question(question: str = Form(...)):
    global current_rulebook_text

    # Safety check: Make sure they uploaded a PDF first
    if not current_rulebook_text:
        return {"error": "Negative. No telemetry loaded. Upload rulebook first."}

    # Send the saved text and the new question to the AI
    answer = get_response(current_rulebook_text, question)

    return {"response": answer}