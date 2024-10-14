import openai
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='build')

# Set your OpenAI API key
openai.api_key = 'your-api-key-here'

def extract_keywords_openai(text):
    prompt = f"""
    You are an expert medical professional tasked with extracting important keywords from medical reports.
    Given the following medical report, identify and list the most significant keywords.
    Focus on medical terms, diagnoses, treatments, symptoms, and medications.
    Provide the keywords as a Python list of strings.

    Medical Report:
    {text}

    Keywords:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts keywords from medical reports."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        keywords_str = response.choices[0].message['content'].strip()
        # Convert the string representation of a list to an actual list
        keywords = eval(keywords_str)
        return keywords
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return []

@app.route('/api/analyze', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        content = file.read().decode('utf-8')
        keywords = extract_keywords_openai(content)
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