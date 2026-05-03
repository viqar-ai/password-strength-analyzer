from flask import Flask, render_template, request
from zxcvbn import zxcvbn
import random
import string

app = Flask(__name__)

def generate_strong_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(12))

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = None
    message = ""
    feedback = {}
    suggestions = []
    alternatives = []

    if request.method == 'POST':
        password = request.form['password']
        result = zxcvbn(password)

        strength = result['score']
        feedback = result['feedback']

        # Strength message
        if strength == 0:
            message = "Very weak – easily guessable"
        elif strength == 1:
            message = "Weak – needs improvement"
        elif strength == 2:
            message = "Moderate – could be stronger"
        elif strength == 3:
            message = "Strong – good password"
        else:
            message = "Very strong – highly secure"

        # Suggestions from zxcvbn
        suggestions = feedback.get('suggestions', [])

        # Generate better alternatives
        for _ in range(3):
            alternatives.append(generate_strong_password())

    return render_template(
        'index.html',
        strength=strength,
        message=message,
        suggestions=suggestions,
        alternatives=alternatives
    )

if __name__ == '__main__':
    
    import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

from flask import jsonify

@app.route('/check', methods=['POST'])
def check():
    password = request.json.get('password')
    result = zxcvbn(password)

    return jsonify({
        "score": result['score'],
        "feedback": result['feedback']
    })
