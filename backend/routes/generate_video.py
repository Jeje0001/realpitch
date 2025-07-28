import os
import requests
import subprocess
from flask import Blueprint, request, jsonify
from uuid import uuid4
from config.s3_config import s3
from PIL import Image
from io import BytesIO
import ffmpeg 
from flask_cors import CORS,cross_origin


generate_video_blueprint = Blueprint("generate_video", __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
CORS(generate_video_blueprint,origins=["http://localhost:5173","https://realpitch-1.onrender.com","https://realpitch009.vercel.app"])
@generate_video_blueprint.route("/generatevideo", methods=["POST"])
@cross_origin(origins="https://realpitch009.vercel.app")
def generatevideo():
    print("🟢 /generatevideo hit")
    return jsonify({"message": "Route is working with CORS!"}), 200

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# def generatevideo():
#     print("🔔 generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼️ image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)
#         if not image_urls or not audio_url or not session_id:
#             return jsonify({"error": "Missing required fields"}), 400

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         audio_data = requests.get(audio_url)
#         print("🎧 Audio Content-Type:", audio_data.headers.get("Content-Type"))
#         if audio_data.status_code != 200:
#             return jsonify({"error": "Failed to download audio"}), 400

#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)

#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])

#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             response = requests.get(url)
#             print(f"🔍 Image {i} content-type:", response.headers.get("Content-Type"))

#             temp_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
#             with open(temp_path, "wb") as f:
#                 f.write(response.content)

#             try:
#                 with Image.open(temp_path) as im:
#                     frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
#                     rgb_im = im.convert("RGB")
#                     rgb_im.save(frame_path, "JPEG")
#                     frame_paths.append(frame_path)
#             except Exception as e:
#                 print(f"Skipping invalid image {temp_path}: {e}")

#         if not frame_paths:
#             return jsonify({"error": "No valid images to generate slideshow"}), 400

#         seconds_per_image = audio_duration / len(frame_paths)
#         framerate = 1 / seconds_per_image

#         slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
#         cmd_slideshow = [
#             "ffmpeg", "-framerate", f"{framerate:.4f}", "-i",
#             os.path.join(tmpfolderpath, "frame_%03d.jpg"),
#             "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
#             "-y", slideshow_path
#         ]
#         subprocess.run(cmd_slideshow, check=True, capture_output=True, text=True)

#         output_video_path = os.path.join(tmpfolderpath, "final_output.mp4")
#         cmd_merge = [
#             "ffmpeg", "-i", slideshow_path, "-i", audio_path,
#             "-c:v", "copy", "-c:a", "aac", "-shortest", "-y", output_video_path
#         ]
#         subprocess.run(cmd_merge, check=True, capture_output=True, text=True)

#         s3_key = f"{session_id}/final_output.mp4"
#         s3.upload_file(output_video_path, S3_BUCKET_NAME, s3_key)
#         s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

#         return jsonify({"video_url": s3_url}), 200

#     except subprocess.CalledProcessError as e:
#         print("❌ FFmpeg Error:")
#         print("Command:", e.cmd)
#         print("Return code:", e.returncode)
#         print("Output:", e.output)
#         print("Stderr:", e.stderr)
#         return jsonify({
#             "error": "Video generation failed",
#             "stderr": e.stderr if isinstance(e.stderr, str) else str(e)
#         }), 500
#     except Exception as e:
#         print("❌ Failed to parse JSON:", str(e))

#         return jsonify({"error": str(e)}), 500
