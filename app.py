# https://www.youtube.com/watch?v=Jxj_jfh4IDk 
from flask import Flask, request, jsonify, render_template, Response, session
import pickle
import numpy as np
from flask_cors import CORS
import subprocess
import os
import signal
import queue
import json
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline

app = Flask(__name__)
CORS(app)
app.secret_key = 'hi'

imap_process = None
prediction_queue = queue.Queue()

# load model and vector
with open('svc_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vector.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set-model', methods=['POST'])
def set_model():
    data = request.get_json()
    selected_model = data.get('model')

    if selected_model:
        session['selected_model'] = selected_model
        # Save to disk
        with open("current_model.txt", "w") as f:
            f.write(selected_model)
        return jsonify({"message": f"Model set to {selected_model}"}), 200
    else:
        return jsonify({"error": "No model provided"}), 400
    
@app.route('/predict', methods=['POST'])
def predict():
    text = request.json.get('text')
    model_file = request.json.get('model', 'svc_model.pkl')  # default to SVC
    if text is not None:
        # Load selected model
        with open(model_file, 'rb') as f:
            selected_model = pickle.load(f)
        
        # setup pipeline and lime explainer
        pipeline = make_pipeline(vectorizer, selected_model)
        class_names = ['Regular', 'Phishing']
        explainer = LimeTextExplainer(class_names=class_names)


        # Prediction
        text_transformed = vectorizer.transform([text])
        prediction = selected_model.predict(text_transformed)[0]
        # Explanation
        exp = explainer.explain_instance(text, pipeline.predict_proba, num_features=6)
        explanation = exp.as_list()

        return jsonify({
            'prediction': int(prediction),
            'explanation': explanation
        })
    else:
        return jsonify({'error': 'Input text not provided.'})

@app.route('/start', methods=['POST'])
def start_script():
    global imap_process
    if imap_process is None:
        imap_process = subprocess.Popen(["python3", "imap_listener.py"])
        return "Started IMAP script", 200
    else:
        return "IMAP script already running", 409

@app.route('/stop', methods=['POST'])
def stop_script():
    global imap_process
    if imap_process is not None:
        try:
            os.kill(imap_process.pid, signal.SIGTERM)  # Send SIGTERM to terminate the process
            imap_process = None
            return "Stopped IMAP script", 200
        except Exception as e:
            print(f"Error stopping IMAP script: {e}")
            return f"Error stopping IMAP script: {e}", 500
    else:
        return "IMAP script not running", 404
    
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    if not data or 'prediction' not in data or 'subject' not in data or 'text' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    model_file = data.get('selected_model', 'svc_model.pkl')  # Default model if none provided

    try:
        # Load selected model
        with open(model_file, 'rb') as f:
            selected_model = pickle.load(f)

        # Build pipeline and explainer dynamically
        pipeline = make_pipeline(vectorizer, selected_model)
        class_names = ['Regular', 'Phishing']
        explainer = LimeTextExplainer(class_names=class_names)

        # Generate explanation
        exp = explainer.explain_instance(data['text'], pipeline.predict_proba, num_features=6)
        explanation = exp.as_list()

        data['explanation'] = explanation

        # Queue the enhanced data for the stream
        prediction_queue.put(data)

        return jsonify({'status': 'Notification received'}), 200

    except Exception as e:
        return jsonify({'error': f"LIME explanation error: {e}"}), 500

@app.route('/stream')
def stream():
    def generate():
        while True:
            try:
                # Wait up to 10 seconds for new prediction data
                data = prediction_queue.get(timeout=10)
                yield f"data: {json.dumps(data)}\n\n"
            except queue.Empty:
                # No new data in 10s, send a keep-alive (optional)
                yield "data: {}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)