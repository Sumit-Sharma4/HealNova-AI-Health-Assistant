import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_ai_doctor(disease, question):
    if not GEMINI_API_KEY:
        return "AI Doctor is unavailable (API key missing)."

    disease = (disease or "").strip()
    question = (question or "").strip()

    if not question:
        return "Please ask a health-related question."

    # 🔒 STRICT but Gemini-friendly prompt
    prompt = f"""
You are HeaLNova AI Doctor.

Rules:
- Answer ONLY health-related questions
- No diagnosis
- No medicine dosage
- Very short answers
- Max 4 bullet points
- One line per bullet
- EACH bullet MUST be ONE short sentence
- NO paragraphs
- NO explanations
- NO symbols like * or -
- Use plain text lines only
- Explain Disease in two lines only
- No greetings

Allowed topics:
- Disease overview
- Symptoms
- Causes
- Precautions
- Any Medicines Information provide if ask by user
- Remedies
- When to consult doctor

If question is NOT health-related:
- Say sorry
- Say you help only with health topics

Disease context: {disease}
User question: {question}

End with:
This is for health awareness only.
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1/models/gemini-2.5-flash:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()

        # 🔍 DEBUG (keep this during development)
        print("Gemini response:", data)

        if (
            "candidates" in data
            and len(data["candidates"]) > 0
            and "content" in data["candidates"][0]
            and "parts" in data["candidates"][0]["content"]
        ):
            return data["candidates"][0]["content"]["parts"][0]["text"]

        return "AI Doctor could not generate a response. Please rephrase your question."

    except Exception as e:
        print("Gemini API error:", e)
        return "AI Doctor is temporarily unavailable."
