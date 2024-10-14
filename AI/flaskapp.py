from LLMS import LLM
from flask import Flask, request, jsonify

llm=LLM(model_name='llama3.1')
app = Flask(__name__)

# Keyword extraction endpoint
@app.route('/keywords', methods=['POST'])
def extract_keywords():
    try:
        # Get text from request body
        data = request.get_json()
        text = data['text']
        
        # Extract keywords using Gensim
        extracted_keywords = llm.get_keywords(text)
        
        return jsonify({
            'status': 'success',
            'keywords': extracted_keywords
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    

# Summary generation endpoint
@app.route('/summary', methods=['POST'])
def generate_summary():
    try:
        # Get text from request body
        data = request.get_json()
        text = data['text']
        
        # Summarize the text using Gensim
        summary = llm.get_summary(text)
        
        if not summary:
            summary = "Text is too short to summarize."
        
        return jsonify({
            'status': 'success',
            'summary': summary
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Keyword extraction endpoint
@app.route('/chatbot', methods=['POST'])
def extract_keywords():
    try:
        # Get question from request body
        data = request.get_json()
        question = data['text']
        
        # 
        answer = llm.chat(question)
        
        return jsonify({
            'status': 'success',
            'answer': answer
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})













if __name__ == '__main__':
   
    app.run(debug=True)

   
    text="HISTORY: Abdominal pain. COMPARISON: CT abdomen pelvis May 3, 2023 TECHNIQUE: CT examination of the abdomen and pelvis was performed following the administration of intravenous contrast. CT dose lowering techniques were used, to include: automated exposure control, adjustment for patient size, and/or use of iterative reconstruction. CONTRAST: 150 mL of Omnipaque 350 intravenous contrast was administered. FINDINGS: ABDOMEN/PELVIS: Lower Chest: Heart size is normal. Minimal dependent atelectasis bilaterally at the lung bases. Small hiatal hernia. Liver: Noncirrhotic liver morphology. There is no focal hepatic lesion. The portal veins and hepatic veins are patent."

    keywords=llm.get_keywords(text)
    summary=llm.get_summary(text)
    
    print(summary)