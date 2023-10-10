from flask import Flask, request, send_from_directory
import os
from firebase_admin import credentials, initialize_app, storage

app = Flask(__name__)

cred = credentials.Certificate('credentials.json')
initialize_app(cred)

bucket = storage.bucket()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        return 'File uploaded successfully'
    else:
        return 'Invalid file type'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    blob = bucket.blob(filename)
    if blob.exists():
        blob.download_to_filename('/tmp/' + filename)
        return send_from_directory('/tmp', filename, as_attachment=True)
    else:
        return 'File not found'

@app.route('/list', methods=['GET'])
def list_files():
    blobs = bucket.list_blobs()
    files = []
    for blob in blobs:
        files.append(blob.name)
    return str(files)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']

if __name__ == '__main__':
    app.run(debug=True)