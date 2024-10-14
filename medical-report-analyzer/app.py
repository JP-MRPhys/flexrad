import openai
from flask import Flask, request, jsonify, send_from_directory
import os
from pymongo import MongoClient
from bson import ObjectId
from MedicalReportAnalyzer import PreProcessing, MedicalReportAnalyzer
from datetime import datetime
from Mongodb import Mongodb

app = Flask(__name__, static_folder='build')

# Initialize MongoDB and MedicalReportAnalyzer
mongo_db = Mongodb()
analyzer = MedicalReportAnalyzer('your-openai-api-key-here')
PreProcessing=PreProcessing()  


"Comment to test"


@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        table, text = PreProcessing.read_pdf_text_and_tables_from_file(file)
        content=text
        content = file.read().decode('utf-8')
        keywords = analyzer.extract_keywords(content)
        analysis = analyzer.analyze_report(content)
        report_id = mongo_db.store_report(content, keywords, analysis)
        return jsonify({
            'text': content,
            'keywords': keywords,
            'analysis': analysis,
            'report_id': report_id
        })

@app.route('/api/report/<report_id>', methods=['GET'])
def get_report(report_id):
    report = mongo_db.get_report(report_id)
    if report:
        return jsonify(report)
    else:
        return jsonify({'error': 'Report not found'}), 404

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

# Ensure the MongoDB connection is closed when the application exits
@app.teardown_appcontext
def teardown_db(exception):
    mongo_db.close_connection()