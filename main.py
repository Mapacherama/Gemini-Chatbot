import google.generativeai as genai
import os
from flask import Flask, request, jsonify

# Load API key from environment variable (or set it directly)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Flask web app setup
app = Flask(__name__)

chat_history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    chat_history.append({"role": "user", "content": user_input})

    response = model.generate_content(chat_history)
    chat_history.append({"role": "assistant", "content": response.text})

    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)