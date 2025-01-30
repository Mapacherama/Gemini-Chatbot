import google.generativeai as genai
import os
from flask import Flask, request, jsonify

# Load API key from environment variable (or set it directly)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Flask web app setup
app = Flask(__name__)

from flask import render_template

@app.route("/")
def home():
    return render_template("index.html")

chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()

        if not user_input:
            return jsonify({"error": "Empty message"}), 400

        # Correct API call format
        response = model.generate_content([{"role": "user", "parts": [{"text": user_input}]}])

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)