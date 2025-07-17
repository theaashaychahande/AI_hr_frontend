from flask import Flask, request, jsonify, send_from_directory
import os
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__, static_folder='../frontend')

CAPTURED_FOLDER = '../captured'
UPLOAD_FOLDER = '../uploads'

os.makedirs(CAPTURED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload_reference', methods=['POST'])
def upload_reference():
    if 'reference' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['reference']
    file.save(os.path.join(UPLOAD_FOLDER, 'reference.jpg'))
    return jsonify({"message": "Reference image saved!"})

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.json
    image_data = data['image']

    # Remove header (e.g., data:image/png;base64,)
    header, encoded = image_data.split(",", 1)
    decoded = base64.b64decode(encoded)
    img = Image.open(BytesIO(decoded))
    img = img.convert("RGB")  # Ensure RGB format
    img.save(os.path.join(CAPTURED_FOLDER, 'photo.jpg'))  # Save image

    return jsonify({
        "message": "Photo saved successfully!",
        "saved_at": os.path.abspath(os.path.join(CAPTURED_FOLDER, 'photo.jpg'))
    })

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)