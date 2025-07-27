import os
import requests
from flask import Blueprint,request,jsonify
from uuid import uuid4
from config.s3_config import s3
from werkzeug.utils import secure_filename


generate_audio_blueprint=Blueprint('generate_audio',__name__)
ELEVENLABS_API_KEY=os.getenv("ELEVENLABS_API_KEY")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")

@generate_audio_blueprint.route("/generateaudio",methods=['POST'])

def generateaudio():
    script=request.json.get("script")

    if not script:
        return jsonify({"error":"No script Provided"}),400
    
    session_id = request.json.get("session_id")
    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400
    s3_key=f"voice/{secure_filename(session_id)}.mp3"
    eleven_url= "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
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
        response = requests.post(eleven_url, headers=headers, json=payload,stream=True)
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Voice generation failed: {str(e)}"}), 500

    # Step 5: Upload to S3
    try:
        s3.upload_fileobj(response.raw, S3_BUCKET_NAME, s3_key)
        audio_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    except Exception as e:
        return jsonify({"error": f"S3 upload failed: {str(e)}"}), 500

    return jsonify({"audio_url": audio_url, "session_id": session_id}), 200