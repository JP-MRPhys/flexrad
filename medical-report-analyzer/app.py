# app.py
from flask import Flask, request, jsonify, send_from_directory
import os
import re

app = Flask(__name__, static_folder='build')

# Keyword extraction function (replace with more sophisticated NLP in production)
def extract_keywords(text):
    common_keywords = ['diagnosis', 'treatment', 'symptoms', 'medication', 'patient']
    return [keyword for keyword in common_keywords if keyword in text.lower()]

@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        content = file.read().decode('utf-8')
        keywords = extract_keywords(content)
        return jsonify({
            'text': content,
            'keywords': keywords
        })

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)