import threading
from flask import Blueprint, Flask, jsonify, render_template, request, send_file
from generate import gpt4o_url, generate_docx, convert_docx_to_pdf  # Replace with your actual module name
import os

dapp = Blueprint('docgen', __name__)

# app = Flask(__name__)
# Paths for generated files
DOCX_PATH = "generated_document.docx"
PDF_PATH = "generated_document.pdf"

# Placeholder for status
status = {"generating": False, "error": None}

@dapp.route('/', methods=['GET', 'POST'])
def index():
    global status
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if not prompt:
            return jsonify({"error": "Prompt cannot be empty"}), 400

        # Start generating files in a separate thread
        status["generating"] = True
        status["error"] = None
        threading.Thread(target=process_generation, args=(prompt,)).start()
        return jsonify({"message": "Generation started"}), 200

    return render_template('index.html')

@dapp.route('/status', methods=['GET'])
def check_status():
    """Endpoint to check generation status."""
    global status
    return jsonify(status)

@dapp.route('/download/<file_type>', methods=['GET'])
def download(file_type):
    """Handles file downloads."""
    if file_type == 'docx':
        if os.path.exists(DOCX_PATH):
            return send_file(DOCX_PATH, as_attachment=True)
    elif file_type == 'pdf':
        if os.path.exists(PDF_PATH):
            return send_file(PDF_PATH, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@dapp.route('/view/docx', methods=['GET'])
def view_docx():
    """Serve the DOCX file for viewing in the browser."""
    if os.path.exists(DOCX_PATH):
        return send_file(DOCX_PATH, as_attachment=False, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    return jsonify({"error": "File not found"}), 404

def process_generation(prompt):
    """Generates the documents based on the prompt."""
    global status
    try:
        content = gpt4o_url(prompt)  # Fetch content from GPT API or your service
        # Ensure content is a Unicode string
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        
        generate_docx(content, file_name=DOCX_PATH)  # Save DOCX file
        convert_docx_to_pdf(DOCX_PATH, PDF_PATH)  # Convert DOCX to PDF
        status["generating"] = False
    except Exception as e:
        status["error"] = str(e)
        status["generating"] = False

# if __name__ == "__main__":
#     app.run(debug=True)
