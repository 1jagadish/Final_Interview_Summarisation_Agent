from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from app.processor import process_transcript
from app.excel import save_to_excel

app = FastAPI(title="Interview Summarization Agent")

# ✅ Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSCRIPTS_PATH = os.path.join(BASE_DIR, "data", "transcripts")


# ✅ Root route
@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


# ✅ List transcripts
@app.get("/transcripts")
def list_transcripts():
    try:
        files = os.listdir(TRANSCRIPTS_PATH)
        return {"files": files}
    except Exception as e:
        print("🔥 ERROR in /transcripts:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Safe metadata parser
def parse_transcript(content: str):
    lines = content.split("\n")

    name = "Unknown"
    role = "Unknown"
    date = "Unknown"

    try:
        if len(lines) > 0:
            name = lines[0].replace("Candidate Name:", "").strip()
        if len(lines) > 1:
            role = lines[1].replace("Role:", "").strip()
        if len(lines) > 2:
            date = lines[2].replace("Date:", "").strip()
    except Exception as e:
        print("🔥 Metadata parsing error:", e)

    transcript = "\n".join(lines[4:]) if len(lines) > 4 else content

    return name, role, date, transcript


# ✅ Preview transcript (NO AI CALL)
@app.get("/preview")
def preview(file_name: str):

    file_path = os.path.join(TRANSCRIPTS_PATH, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Transcript not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        name, role, date, transcript = parse_transcript(content)

        return {
            "meta": {
                "name": name,
                "role": role,
                "date": date
            },
            "transcript": transcript
        }

    except Exception as e:
        print("🔥 ERROR in /preview:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Analyze transcript (AI + Excel)
@app.get("/analyze")
def analyze(file_name: str):

    file_path = os.path.join(TRANSCRIPTS_PATH, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Transcript not found")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        name, role, date, transcript = parse_transcript(content)

        meta = {
            "name": name,
            "role": role,
            "date": date
        }

        # 🔥 AI Processing (this was crashing earlier)
        result = process_transcript(transcript)

        # 🔥 Save to Excel
        save_to_excel(meta, result)

        return {
            "meta": meta,
            "transcript": transcript,
            "summary": result.get("summary", ""),
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
            "recommendation": result.get("recommendation", "Unknown")
        }

    except Exception as e:
        print("🔥 ERROR in /analyze:", e)   # 👈 THIS WILL SHOW REAL ISSUE
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Download Excel
@app.get("/download")
def download_excel():

    file_path = os.path.join(BASE_DIR, "data", "results.xlsx")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="No Excel file found")

    return FileResponse(
        path=file_path,
        filename="Interview_Analysis.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )