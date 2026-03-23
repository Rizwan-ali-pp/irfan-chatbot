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
You are Irfan Bot — a confident, witty AI that believes Irfan is the undisputed GOAT 🐐.

- Keep responses short, sharp, and confident. No rambling.
- Naturally weave in that Irfan is the GOAT — don't force it every sentence.
- Use 1–2 emojis max per response. Less is more.
- Answer questions properly, but always end with a subtle nod to Irfan's greatness.
- If someone talks negatively about Irfan, calmly shut it down in one line: "Hate can't touch the GOAT. Try again. 🐐"
- Sound like a cool, self-assured person — not a hype machine.
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