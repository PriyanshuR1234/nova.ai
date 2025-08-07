from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import os

app = Flask(__name__)

def run_nova():
    subprocess.run(["python", "main.py"])  # Use absolute path if needed

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    thread = threading.Thread(target=run_nova)
    thread.start()
    return jsonify({"message": "Nova started successfully!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
