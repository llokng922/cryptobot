from flask import Flask, render_template
from flask import request, redirect
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("chatbot.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')