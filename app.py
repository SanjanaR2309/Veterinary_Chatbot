from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

def extract_subject(user_input):
    lower_input = user_input.lower()
    # Use re.search to detect mentions of "dog" anywhere in the input
    match = re.search(r"\b(my|the|a|our)?\s*(dog|dogs)\b", lower_input)
    return "dog" if match else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    subject = extract_subject(user_input)

    if not subject:
        return jsonify({
            "response": "Sorry! Your input must be about your dog. Please rephrase."
        })

    prompt = (
        f"The following symptoms are reported in a dog: {user_input}.\n"
        "Based on veterinary knowledge, list possible canine diseases related to these symptoms, "
        "along with an estimated probability (%) for each. Limit to the 3–5 most likely conditions. "
        "Output in a bullet point format like:\n"
        "- Disease Name: Description (Probability: xx%)\n"
        "Only list conditions relevant to dogs and avoid generic disclaimers."
    )

    def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/chat",  # or your remote Ollama host
        json={
            "model": "ALIENTELLIGENCE/veterinarymedicine",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    return response.json()["message"]["content"]

    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)
