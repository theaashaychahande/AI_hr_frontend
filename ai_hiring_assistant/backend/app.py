# app.py
from flask import Flask, request, jsonify, send_from_directory
import os
import base64
from io import BytesIO  
from PIL import Image
import imagehash

app = Flask(__name__, static_folder='../frontend')

UPLOAD_FOLDER = '../uploads'
CAPTURED_FOLDER = '../captured'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CAPTURED_FOLDER, exist_ok=True)

def compare_images(img1_path, img2_path):
    try:
        hash1 = imagehash.phash(Image.open(img1_path))
        hash2 = imagehash.phash(Image.open(img2_path))
        return hash1 - hash2  # Hamming distance
    except Exception as e:
        print("Error in compare_images:", str(e))
        return 999


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/upload_reference', methods=['POST'])
def upload_reference():
    if 'reference' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['reference']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file.save(os.path.join(UPLOAD_FOLDER, 'reference.jpg'))
        return jsonify({"message": "Reference image uploaded successfully!"})
    except Exception as e:
        return jsonify({"error": "Could not save reference image", "details": str(e)}), 500


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.json
    image_data = data['image']

    try:
        header, encoded = image_data.split(",", 1)
    except ValueError:
        return jsonify({"result": "Invalid image data"})

    try:
        decoded = base64.b64decode(encoded)  # ✅ base64 imported
        img = Image.open(BytesIO(decoded))  # ✅ BytesIO imported
        img = img.convert("RGB")
        img.save(os.path.join(CAPTURED_FOLDER, 'photo.jpg'))
    except Exception as e:
        return jsonify({"result": f"Error decoding image: {str(e)}"})

    ref_path = os.path.join(UPLOAD_FOLDER, 'reference.jpg')
    if not os.path.exists(ref_path):
        return jsonify({"result": "Reference image not found"})

    try:
        distance = compare_images(ref_path, os.path.join(CAPTURED_FOLDER, 'photo.jpg'))
        if distance <= 10:
            result = "✅ Face Matched"
        else:
            result = "❌ Not Matched"
    except Exception as e:
        return jsonify({"result": "Error comparing images", "error": str(e)})

    return jsonify({"result": result})


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)