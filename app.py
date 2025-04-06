from flask import Flask, render_template, request, jsonify
import ollama
import re

app = Flask(__name__)

def extract_subject(user_input):
    lower_input = user_input.lower()
    match = re.match(r"(my|the|a)?\s*(dog|dogs)\b", lower_input)
    return "dog" if match else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    subject = extract_subject(user_input)

    if not subject:
        return jsonify({"response": "Sorry! Your input must be about your dog. Please rephrase."})

    prompt = f"Provide veterinary advice for the following scenario involving a dog: {user_input}. " \
             "Focus only on dogs and provide relevant medical insights."

    response = ollama.chat(
        model='ALIENTELLIGENCE/veterinarymedicine',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({"response": response['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)
