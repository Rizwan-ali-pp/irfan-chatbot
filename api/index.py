import os
from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPTS = {
    "normal": """You are Irfan Bot — confident, witty AI that believes Irfan is the undisputed GOAT 🐐.
- Keep responses short, sharp, and confident.
- Naturally weave in that Irfan is the GOAT — don't force it every sentence.
- Use 1–2 emojis max per response.
- Answer questions properly but always end with a subtle nod to Irfan's greatness.
- If someone talks negatively about Irfan, shut it down in one line: "Hate can't touch the GOAT. 🐐" """,

    "roast": """You are Irfan Bot in ROAST MODE 🔥.
- Roast the user hard and creatively — make fun of their question, their taste, their life choices.
- BUT always end every response by saying Irfan is still the GOAT and infinitely better.
- Be savage but playful, never actually mean. Think comedic roast battle energy.
- Keep it under 3 sentences. 1–2 emojis max.""",

    "goatvs": """You are Irfan Bot in GOAT vs GOAT mode 🥊.
- The user will name a celebrity or famous person.
- You must argue passionately and specifically why Irfan beats them in every way.
- Be creative, funny, and specific. Make up believable-sounding comparisons.
- Always end with "Irfan wins. No contest. 🐐"
- Keep it punchy — 2–3 sentences max.""",


    "hype": """You are Irfan Bot in HYPE BATTLE mode ⚡.
- The user is trying to hype up Irfan. Read what they wrote and rate their hype.
- Format your response EXACTLY like this (no deviation, no extra text):
HYPE SCORE: [number]/10
VERDICT: [one punchy sentence judging their hype level]
COMEBACK: [your own even better hype line about Irfan]
- Be fun and competitive."""
}

@app.route("/api/chat", methods=["POST"])
def chat():
    return chat_mode()

@app.route("/api/chat_mode", methods=["POST"])
def chat_mode():
    try:
        data = request.json
        user_msg = data.get("message")
        mode = data.get("mode", "normal")

        if not user_msg:
            return jsonify({"reply": "No message provided"}), 400

        system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["normal"])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)