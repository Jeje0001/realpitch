
import os
import requests
import subprocess
import tempfile
import shutil
import psutil
import ffmpeg
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from flask import Blueprint, request, jsonify
from uuid import uuid4
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

generate_video_blueprint = Blueprint("generate_video", __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CORS(generate_video_blueprint, origins=[
    "http://localhost:5173",
    "https://realpitch-1.onrender.com",
    "https://realpitch009.vercel.app"
])
def log_memory(stage):
    used = psutil.virtual_memory().used / 1024 / 1024
    print(f"🧠 Memory after {stage}: {used:.2f} MB")

def get_audio_duration(audio_path):
    try:
        probe = ffmpeg.probe(audio_path)
        duration = float(probe['format']['duration'])
        print(f"🕒 Audio duration: {duration:.2f} seconds")
        return duration
    except Exception as e:
        print("❌ Failed to get audio duration:", str(e))
        return 6.0

@generate_video_blueprint.route("/generatevideo", methods=["POST"])
@cross_origin(origins="https://realpitch009.vercel.app")

def generate_video():
    print("🔔 /generatevideo endpoint hit")

    try:
        data = request.get_json(force=True)
        print("✅ JSON parsed:", data)
    except Exception as e:
        print("❌ Failed to parse JSON:", str(e))
        return jsonify({"error": "Invalid JSON body"}), 400

    image_urls = data.get("image_urls")
    audio_url = data.get("audio_url")
    session_id = data.get("session_id")

    if not image_urls or not audio_url or not session_id:
        print("❌ Missing required fields")
        return jsonify({"error": "Missing fields"}), 400

    print("🖼 image_urls:", image_urls)
    print("🔊 audio_url:", audio_url)
    print("📦 session_id:", session_id)
    log_memory("start")

    try:
        temp_dir = tempfile.mkdtemp()
        print("📁 Temp dir created:", temp_dir)

        frame_paths = []
        skipped_images = []

        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                img = Image.open(BytesIO(response.content))
                img.verify()  # Validate
                img = Image.open(BytesIO(response.content))  # Reopen for manipulation

                if img.width < 10 or img.height < 10:
                    raise ValueError(f"Image too small: {img.width}x{img.height}")

                # Resize for consistency
                img = img.convert("RGB").resize((1280, 720))

                image_path = os.path.join(temp_dir, f"frame_{len(frame_paths):03}.jpg")
                img.save(image_path, "JPEG")
                frame_paths.append(image_path)
                print(f"✅ Frame saved: {image_path}")
                log_memory(f"after image {i}")

            except (requests.RequestException, UnidentifiedImageError, ValueError, OSError) as e:
                print(f"❌ Skipping invalid image {i}: {url} | Reason: {e}")
                skipped_images.append(url)

        if not frame_paths:
            return jsonify({"error": "All images failed or were invalid."}), 400

        try:
            audio_path = os.path.join(temp_dir, "audio.mp3")
            audio_response = requests.get(audio_url, timeout=10)
            with open(audio_path, "wb") as f:
                f.write(audio_response.content)
            print("✅ Audio saved:", audio_path)
            log_memory("after audio download")
        except Exception as e:
            print("❌ Failed to download audio:", str(e))
            return jsonify({"error": "Audio download failed"}), 500

        audio_duration = get_audio_duration(audio_path)
        if audio_duration <= 0:
            print("❌ Invalid audio duration")
            return jsonify({"error": "Invalid audio duration"}), 500

        frame_rate = len(frame_paths) / audio_duration
        print(f"🎞️ Frame rate calculated: {frame_rate:.2f} fps")

        try:
            video_path = os.path.join(temp_dir, "video.mp4")
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",
                "-framerate", str(frame_rate),
                "-i", os.path.join(temp_dir, "frame_%03d.jpg"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                video_path
            ]
            print("🎬 Running FFmpeg:", " ".join(ffmpeg_cmd))
            subprocess.run(ffmpeg_cmd, check=True)
            print("✅ Video created:", video_path)
            log_memory("after video creation")
        except Exception as e:
            print("❌ FFmpeg failed:", str(e))
            return jsonify({"error": "Video generation failed"}), 500

        try:
            final_path = os.path.join(temp_dir, f"{session_id}_final.mp4")
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                final_path
            ]
            print("🔗 Combining audio and video")
            subprocess.run(ffmpeg_cmd, check=True)
            print("✅ Final video created:", final_path)
            log_memory("after audio+video combine")
        except Exception as e:
            print("❌ Failed to combine video and audio:", str(e))
            return jsonify({"error": "Failed to combine video and audio"}), 500

        try:
            import boto3
            s3 = boto3.client("s3")
            s3_key = f"final_videos/{session_id}.mp4"
            s3.upload_file(final_path, S3_BUCKET_NAME, s3_key, ExtraArgs={"ContentType": "video/mp4"})
            s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            print("✅ Uploaded to S3:", s3_url)
            log_memory("after S3 upload")
        except Exception as e:
            print("❌ S3 upload failed:", str(e))
            return jsonify({"error": "S3 upload failed"}), 500

        response = {
            "video_url": s3_url,
            "audio_url": audio_url
        }
        if skipped_images:
            response["warning"] = f"{len(skipped_images)} image(s) were skipped due to errors."

        return jsonify(response), 200

    finally:
        try:
            shutil.rmtree(temp_dir)
            print("🧹 Temp files cleaned up:", temp_dir)
        except Exception as e:
            print("⚠️ Failed to clean temp dir:", str(e))
