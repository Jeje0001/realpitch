import os
import requests
import subprocess
from flask import Blueprint, request, jsonify
from uuid import uuid4
from config.s3_config import s3
from PIL import Image
import ffmpeg
from flask_cors import CORS, cross_origin

generate_video_blueprint = Blueprint("generate_video", __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# ✅ Enable CORS on blueprint
CORS(generate_video_blueprint, origins=[
    "http://localhost:5173",
    "https://realpitch009.vercel.app",
    "https://realpitch-1.onrender.com"
])

# ✅ Video Generation Route
@generate_video_blueprint.route("/generatevideo", methods=["POST"])
@cross_origin(origins="https://realpitch009.vercel.app")
def generatevideo():
    print("🔔 /generatevideo endpoint hit")

    try:
        data = request.get_json()
        print("✅ JSON parsed:", data)

        image_urls = data.get("image_urls")
        audio_url = data.get("audio_url")
        session_id = data.get("session_id")
        print("🖼 image_urls:", image_urls)
        print("🔊 audio_url:", audio_url)
        print("📦 session_id:", session_id)

        tmpfolderpath = os.path.join("/tmp", session_id)
        os.makedirs(tmpfolderpath, exist_ok=True)

        # 🔊 Download audio
        audio_path = os.path.join(tmpfolderpath, "audio.mp3")
        audio_data = requests.get(audio_url)
        with open(audio_path, "wb") as f:
            f.write(audio_data.content)
        print("✅ Audio saved:", audio_path)

        # ⏱️ Get audio duration
        probe = ffmpeg.probe(audio_path)
        audio_duration = float(probe['format']['duration'])
        print("🎯 Audio duration:", audio_duration)

        # 🖼 Download and convert images
        frame_paths = []
        for i, url in enumerate(image_urls):
            print(f"📥 Downloading image {i}: {url}")
            response = requests.get(url)
            raw_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
            with open(raw_path, "wb") as f:
                f.write(response.content)

            try:
                with Image.open(raw_path) as im:
                    frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
                    rgb_im = im.convert("RGB")
                    rgb_im.save(frame_path, "JPEG")
                    frame_paths.append(frame_path)
                    print(f"✅ Frame {i} saved:", frame_path)
            except Exception as e:
                print(f"⚠️ Skipping image {i}: {e}")

        if not frame_paths:
            return jsonify({"error": "No valid images"}), 400

        print("📸 Total frames:", len(frame_paths))

        # 🎬 Slideshow generation
        seconds_per_image = audio_duration / len(frame_paths)
        framerate = max(0.5, 1 / seconds_per_image)  # ⛑ prevent too-low fps
        slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
        frame_pattern = os.path.join(tmpfolderpath, "frame_%03d.jpg")

        cmd_slideshow = [
            "ffmpeg", "-y",
            "-framerate", f"{framerate:.4f}",
            "-i", frame_pattern,
            "-c:v", "libx264",
            "-r", "30",
            "-pix_fmt", "yuv420p",
            slideshow_path
        ]

        print("🎬 Running slideshow ffmpeg command:")
        print(" ".join(cmd_slideshow))

        try:
            result = subprocess.run(cmd_slideshow, check=True, capture_output=True, text=True)
            print("✅ Slideshow created")
            print("FFmpeg stdout:\n", result.stdout)
            print("FFmpeg stderr:\n", result.stderr)
        except subprocess.CalledProcessError as e:
            print("❌ FFmpeg slideshow FAILED")
            print("Command:", e.cmd)
            print("Return code:", e.returncode)
            print("stdout:", e.stdout)
            print("stderr:", e.stderr)
            return jsonify({
                "error": "slideshow_failed",
                "return_code": e.returncode,
                "stderr": e.stderr,
                "stdout": e.stdout
            }), 500

        return jsonify({"message": "Slideshow step completed"}), 200

    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500