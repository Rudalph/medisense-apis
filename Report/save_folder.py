from flask import request, jsonify
import os
from Report.load_documents import load_documents




UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Data')

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




def save_folder():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # Save the file to the desired folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        load_documents()
        os.remove(file_path)
        return jsonify({'message': f'File {file.filename} uploaded successfully!'}), 200