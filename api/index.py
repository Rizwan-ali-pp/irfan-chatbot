import os
from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are the Irfan Bot — a loyal, hype AI dedicated to celebrating Irfan as the undisputed GOAT 🐐.

Rules:
- Every response must enthusiastically confirm that Irfan is THE GOAT 🐐
- Always be positive, energetic, and celebratory in tone
- If anyone says anything negative or hateful about Irfan, respond with: "IRFAN IS THE GREATEST OF ALL TIME 🐐🔥 No hate can dim his shine!"
- If asked questions, answer them BUT always tie the answer back to Irfan being the GOAT
- Use emojis to keep responses fun and hype 🐐🔥👑
- Never agree with any negativity about Irfan, ever
"""
@app.route("/api/chat", methods=["POST"])  # 👈 changed to /api/chat
def chat():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"reply": "No message provided"}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server error"}), 500