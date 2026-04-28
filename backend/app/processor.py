import json
from app.llm import get_llm


# ✅ SAFE LIST CONVERTER
def ensure_list(value):
    if isinstance(value, list):
        return value
    elif isinstance(value, str) and value.strip():
        return [value]
    else:
        return []


def process_transcript(transcript: str):

    parsed = {}

    try:
        llm = get_llm()

        prompt = f"""
        Analyze the interview transcript and return ONLY valid JSON.

        Format:
        {{
          "summary": "short paragraph",
          "strengths": ["point1", "point2"],
          "improvements": ["point1", "point2"],
          "recommendation": "Best Fit / Good Fit / Partial Fit / Not Fit"
        }}

        Rules:
        - strengths and improvements MUST be bullet points (list)
        - Keep points short and clear
        - Do NOT return anything outside JSON

        Transcript:
        {transcript}
        """

        response = llm.invoke(prompt)
        content = response.content.strip()

        # ✅ Handle ```json blocks
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content.replace("json", "", 1).strip()

        # ✅ Parse JSON
        parsed = json.loads(content)

    except Exception as e:
        print("🔥 LLM ERROR:", e)

        # ✅ fallback
        parsed = {
            "summary": transcript[:300] if transcript else "No summary available",
            "strengths": [],
            "improvements": [],
            "recommendation": "Unknown"
        }

    # ✅ FINAL SAFE OUTPUT (NO BREAKAGE ANYWHERE)
    return {
        "summary": parsed.get("summary", ""),
        "strengths": ensure_list(parsed.get("strengths", [])),
        "improvements": ensure_list(parsed.get("improvements", [])),
        "recommendation": parsed.get("recommendation", "Unknown")
    }