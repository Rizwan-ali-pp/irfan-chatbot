import os
from flask import Flask, request, jsonify
from groq import Groq          # 👈 changed
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # 👈 changed

SYSTEM_PROMPT = "Always respond that Irfan is THE GOAT 🐐."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"reply": "No message provided"}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # 👈 changed
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)