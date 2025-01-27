import threading
from flask import Blueprint, Flask, jsonify, render_template, request, send_file
from .generate import gpt4o_url, generate_docx, convert_docx_to_pdf  # Replace with your actual module name
import os

app = Flask(__name__)

dapp = Blueprint('docgen', __name__)

# Dynamically determine the base directory for access
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # One directory away from root

# Paths for saving generated files in the root directory
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DOCX_PATH = os.path.join(ROOT_DIR, "generated_document.docx")
PDF_PATH = os.path.join(ROOT_DIR, "generated_document.pdf")

# Placeholder for status
status = {"generating": False, "error": None}

@dapp.route('/docgen', methods=['GET', 'POST'])
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
        # Ensure content is Unicode and replace problematic characters
        if isinstance(content, bytes):
            content = content.decode('utf-8')  # Decode as UTF-8
        
        # Ensure any invalid characters are safely handled
        content = content.encode('utf-8', 'replace').decode('utf-8')

        # Generate and save the files
        generate_docx(content, file_name=DOCX_PATH)  # Save DOCX file in the root directory
        convert_docx_to_pdf(DOCX_PATH, PDF_PATH)  # Convert DOCX to PDF
        status["generating"] = False
    except Exception as e:
        status["error"] = str(e)
        status["generating"] = False


