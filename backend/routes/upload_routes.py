import os
from flask import Blueprint, request
from config.s3_config import s3
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask_cors import CORS

upload_blueprint = Blueprint('upload', __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "mov", "webm", "gif"}
CORS(upload_blueprint, origins=["http://localhost:5173"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_blueprint.route("/upload", methods=['POST'])
def upload_images():
    files = request.files.getlist("files")
    
    if not files:
        return {'error': "No files found in the request"}, 400

    session_id = str(uuid4())
    uploaded_urls = []

    for idx, uploaded_file in enumerate(files):
        if uploaded_file.filename == '':
            continue

        if not allowed_file(uploaded_file.filename):
            continue

        extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"image_{idx + 1}.{extension}")
        s3_key = f"uploads/{session_id}/{filename}"

        try:
            s3.upload_fileobj(uploaded_file, S3_BUCKET_NAME, s3_key)
            url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            uploaded_urls.append(url)
        except Exception as e:
            return {"error": f"Upload failed for {filename}: {str(e)}"}, 500

    if not uploaded_urls:
        return {"error": "No valid files were uploaded"}, 400

    return {
        'session_id': session_id,
        'uploaded_files': uploaded_urls
    }, 200
