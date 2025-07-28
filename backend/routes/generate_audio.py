import os
import requests
from flask import Blueprint, request, jsonify
from uuid import uuid4
from config.s3_config import s3
from werkzeug.utils import secure_filename
from flask_cors import CORS

generate_audio_blueprint = Blueprint('generate_audio', __name__)
CORS(generate_audio_blueprint, origins=["http://localhost:5173","https://realpitch-1.onrender.com"])

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@generate_audio_blueprint.route("/generateaudio", methods=["POST"])
def generateaudio():
    script = request.json.get("script")
    session_id = request.json.get("session_id")

    if not script:
        return jsonify({"error": "No script provided"}), 400
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    s3_key = f"voice/{secure_filename(session_id)}.mp3"
    temp_path = f"/tmp/{session_id}.mp3"

    eleven_url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": script,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(eleven_url, headers=headers, json=payload, stream=True)
        content_type = response.headers.get("Content-Type", "")
        print(f"🎧 Audio Content-Type: {content_type}")

        if "audio/mpeg" not in content_type:
            print("🔴 ElevenLabs Error Response:", response.text)
            return jsonify({
                "error": "Voice generation failed",
                "status_code": response.status_code,
                "details": response.text
            }), 500

        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    except Exception as e:
        print("🔥 Unexpected Exception during ElevenLabs call:", str(e))
        return jsonify({"error": f"Voice generation failed: {str(e)}"}), 500

    try:
        with open(temp_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET_NAME, s3_key)

        audio_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return jsonify({"audio_url": audio_url, "session_id": session_id}), 200

    except Exception as e:
        print("🪣 S3 Upload Error:", str(e))
        return jsonify({"error": f"S3 upload failed: {str(e)}"}), 500
