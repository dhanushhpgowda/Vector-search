from flask import Flask, render_template, request, jsonify, session
import os
from engine import ingest_file, query_collection

app = Flask(__name__)
app.secret_key = "super_secret_key"
UPLOAD_FOLDER = 'docs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        coll_name = ingest_file(file_path)
        session['current_coll'] = coll_name
        
        # Track history in session
        if 'history' not in session:
            session['history'] = []
        
        # Add to history if not already there
        if not any(item['filename'] == file.filename for item in session['history']):
            session['history'].append({"filename": file.filename, "coll": coll_name})
            session.modified = True

        return jsonify({"message": f"Successfully ingested {file.filename}", "coll": coll_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify({"history": session.get('history', [])})

@app.route('/select_doc', methods=['POST'])
def select_doc():
    coll_name = request.json.get('coll')
    session['current_coll'] = coll_name
    return jsonify({"status": "success"})

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    coll_name = session.get('current_coll')

    if not coll_name:
        return jsonify({"error": "Please upload or select a document first"}), 400

    try:
        results = query_collection(coll_name, query)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)