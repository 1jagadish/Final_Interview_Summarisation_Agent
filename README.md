<<<<<<< HEAD
# Final_Interview_Summarisation_Agent
This is interview summarization agent for fetching strengths, weakness, areas of improvement from given interview transcripts and The generated data stored in excel sheet file for real time tracking
=======
# Interview Summarization Agent (POC)

## Features
- Select interview transcript
- AI-based analysis (Azure OpenAI)
- Summary + strengths + weaknesses + recommendation
- Stores results in Excel

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Add .env file
(Add Azure credentials)

### 3. Run backend
uvicorn app.main:app --reload

### 4. Run frontend
streamlit run frontend/app.py

## Output
- Excel file stored in backend/data/results.xlsx
>>>>>>> 8a7ea84 (Initial commit: Interview Summarization Agent (Backend + Frontend))
