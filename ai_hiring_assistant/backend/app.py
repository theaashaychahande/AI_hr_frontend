from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = '../uploads'
CAPTURED_FOLDER = '../captured'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CAPTURED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "AI Hiring Assistant Backend is Running!"

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.json
    image_data = data['image']
    
    with open(os.path.join(CAPTURED_FOLDER, 'photo.jpg'), 'w') as f:
        f.write(image_data)
    
    return jsonify({"message": "Photo saved successfully!"})

@app.route('/upload_reference', methods=['POST'])
def upload_reference():
    if 'reference' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['reference']
    file.save(os.path.join(UPLOAD_FOLDER, 'reference.jpg'))
    
    return jsonify({"message": "Reference image saved!"})

if __name__ == '__main__':
    app.run(debug=True)