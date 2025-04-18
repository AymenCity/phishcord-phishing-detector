# https://www.youtube.com/watch?v=Jxj_jfh4IDk 
from flask import Flask, request, jsonify, render_template, Response
import pickle
import numpy as np
from flask_cors import CORS
import subprocess
import os
import signal
import queue
import json

app = Flask(__name__)
CORS(app)

imap_process = None
prediction_queue = queue.Queue()

with open('svc_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vector.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json.get('text')
    if text is not None:
        text_transformed = vectorizer.transform([text])

        prediction = model.predict(text_transformed)[0]

        return jsonify({'prediction': int(prediction)})
    else:
        return jsonify({'error': 'Input text not provided.'})
    
@app.route('/start', methods=['POST'])
def start_script():
    global imap_process
    if imap_process is None:
        imap_process = subprocess.Popen(["python", "imap_listener.py"])
        return "Started IMAP script", 200
    else:
        return "IMAP script already running", 409

@app.route('/stop', methods=['POST'])
def stop_script():
    global imap_process
    if imap_process is not None:
        os.kill(imap_process.pid, signal.SIGTERM)
        imap_process = None
        return "Stopped IMAP script", 200
    else:
        return "IMAP script not running", 404
    
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    if not data or 'prediction' not in data or 'subject' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Queue it for frontend to pick up
    
    prediction_queue.put(data)
    return jsonify({'status': 'Notification received'}), 200

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            data = prediction_queue.get()
            yield f"data: {json.dumps(data)}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)