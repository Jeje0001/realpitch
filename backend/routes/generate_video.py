import os
import requests
import subprocess
from flask import Blueprint, request, jsonify
from uuid import uuid4
from config.s3_config import s3
from werkzeug.utils import secure_filename

generate_video_blueprint = Blueprint("generate_video", __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@generate_video_blueprint.route("/generatevideo", methods=["POST"])
def generatevideo():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    image_urls = data.get("image_urls")  # Now expects a list
    audio_url = data.get("audio_url")
    session_id = data.get("session_id")

    if not image_urls or not audio_url or not session_id:
        return jsonify({"error": "Missing required fields"}), 400

    # 🌀 Prepare temp directory
    tmpfolderpath = os.path.join("/tmp", session_id)
    os.makedirs(tmpfolderpath, exist_ok=True)

    # 🎵 Download audio
    audio = requests.get(audio_url, stream=True)
    audio_path = os.path.join(tmpfolderpath, "audio.mp3")
    with open(audio_path, "wb") as f:
        for chunk in audio.iter_content(chunk_size=8192):
            f.write(chunk)

    # 🖼️ Download all images
    for idx, url in enumerate(image_urls):
        img = requests.get(url, stream=True)
        img_path = os.path.join(tmpfolderpath, f"frame_{idx:03}.jpg")
        with open(img_path, "wb") as f:
            for chunk in img.iter_content(chunk_size=8192):
                f.write(chunk)

    # 🎬 Create slideshow video from images (1 image per second)
    slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
    cmd_slideshow = [
        "ffmpeg",
        "-framerate", "1",
        "-i", os.path.join(tmpfolderpath, "frame_%03d.jpg"),
        "-c:v", "libx264",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        "-y", slideshow_path
    ]

    try:
        subprocess.run(cmd_slideshow, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Image stitching failed: {str(e)}"}), 500

    # 🔊 Merge audio + slideshow
    output_path = os.path.join(tmpfolderpath, "output.mp4")
    cmd_merge = [
        "ffmpeg",
        "-i", slideshow_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y", output_path
    ]

    try:
        subprocess.run(cmd_merge, check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Final merge failed: {str(e)}"}), 500

    # ☁️ Upload to S3
    s3_key = f"videos/{session_id}.mp4"
    try:
        with open(output_path, "rb") as f:
            s3.upload_fileobj(f, S3_BUCKET_NAME, s3_key)
        video_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    except Exception as e:
        return jsonify({"error": f"S3 Upload failed: {str(e)}"}), 500

    # 🧹 Cleanup
    for file in os.listdir(tmpfolderpath):
        os.remove(os.path.join(tmpfolderpath, file))


    return jsonify({
        "message": "Video generated successfully",
        "video_url": video_url,
        "session_id": session_id
    }), 200
