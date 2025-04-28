# https://www.youtube.com/watch?v=Jxj_jfh4IDk 
from flask import Flask, request, jsonify, render_template, Response, session
import pickle
from flask_cors import CORS
import subprocess
import os
import signal
import queue
import json
from lime.lime_text import LimeTextExplainer
from sklearn.pipeline import make_pipeline

# flask setup
app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24) # https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask

# global variables / constants
imap_process = None #tracks imap listener process
prediction_queue = queue.Queue() #queue for server-sent events 
CLASS_NAMES = ['Regular', 'Phishing'] #labels to be used for the lime explanation

# load vectoriser
with open('vector.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# load model (helper function)
def load_model(model_file='svc_model.pkl'):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    pipeline = make_pipeline(vectorizer, model) #creates pipeline
    print("Loaded model:", model_file) 
    return model, pipeline

# routes
@app.route('/')
def home():
    return render_template('index.html')

# sets the selected model
@app.route('/set-model', methods=['POST'])
def set_model():
    data = request.get_json()
    selected_model = data.get('model')

    if selected_model:
        session['selected_model'] = selected_model
        # Save to disk
        with open("current_model.txt", "w") as f:
            f.write(selected_model)
        return jsonify({"message": "Model set to " + selected_model}), 200
    else:
        return jsonify({"error": "No model provided"}), 400

# predicts whether the manual text is phishing or regular    
@app.route('/predict', methods=['POST'])
def predict():
    text = request.json.get('text')
    model_file = request.json.get('model', 'svc_model.pkl')  #default to SVC
    if text is not None:
        selected_model, pipeline = load_model(model_file) #load model and pipeline
        
        # setup lime explainer
        explainer = LimeTextExplainer(class_names=CLASS_NAMES)

        # generates prediction
        text_transformed = vectorizer.transform([text])
        prediction = selected_model.predict(text_transformed)[0]

        # generates explanation
        exp = explainer.explain_instance(text, pipeline.predict_proba, num_features=6)
        explanation = exp.as_list()

        return jsonify({
            'prediction': int(prediction),
            'explanation': explanation
        })
    else:
        return jsonify({'error': 'Input text not provided.'})

# checks status of imap listener script (imap_listener.py)
@app.route('/status', methods=['GET'])
def check_status():
    global imap_process
    is_running = imap_process is not None
    return jsonify({'running': is_running}), 200

# starts imap listener script (imap_listener.py)
@app.route('/start', methods=['POST'])
def start_script():
    global imap_process
    if imap_process is None:
        imap_process = subprocess.Popen(["python3", "imap_listener.py"])
        return jsonify({"status": "Started IMAP script"}), 200
    else:
        return jsonify({"error": "IMAP script already running"}), 409

# stops imap listener script (imap_listener.py)
@app.route('/stop', methods=['POST'])
def stop_script():
    global imap_process
    if imap_process is not None:
        try:
            os.kill(imap_process.pid, signal.SIGTERM)  # Send SIGTERM to terminate the process
            imap_process = None
            return jsonify({"status": "Stopped IMAP script"}), 200
        except Exception as e:
            print("Error stopping IMAP script:", e)
            return jsonify({"error": "Error stopping IMAP script"}), 500
    else:
        return jsonify({"error": "IMAP script not running"}), 404
    
# receives new email prediction and puts it in a queue for streaming 
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    if not data or 'prediction' not in data or 'subject' not in data or 'text' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    model_file = data.get('selected_model', 'svc_model.pkl')  # Default model if none provided

    try:
        selected_model, pipeline = load_model(model_file)

        # Build pipeline and explainer dynamically
        explainer = LimeTextExplainer(class_names=CLASS_NAMES)

        # Generate explanation
        exp = explainer.explain_instance(data['text'], pipeline.predict_proba, num_features=6)
        explanation = exp.as_list()

        data['explanation'] = explanation

        # Queue the enhanced data for the stream
        prediction_queue.put(data)
        return jsonify({'status': 'Notification received'}), 200

    except Exception as e:
        return jsonify({'error': "LIME explanation error: " + str(e)}), 500 # exception object need to be converted to string

# streams predictions to server-sent events
@app.route('/stream')
def stream():
    def generate():
        while True:
            try:
                # Wait up to 5 seconds for new prediction data
                data = prediction_queue.get(timeout=5)
                yield "data: " + json.dumps(data) + "\n\n"
            except queue.Empty:
                # No new data in 5s, send a keep-alive (optional)
                yield "data: {}\n\n"

    return Response(generate(), mimetype='text/event-stream')

# main
if __name__ == '__main__':
    app.run(debug=True)