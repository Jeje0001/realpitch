# import os
# import requests
# import subprocess
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from config.s3_config import s3
# from PIL import Image
# from io import BytesIO
# import ffmpeg
# from flask_cors import CORS, cross_origin

# # 🔧 Blueprint setup
# generate_video_blueprint = Blueprint("generate_video", __name__)
# # S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# # ✅ Enable CORS for this blueprint
# CORS(generate_video_blueprint, origins=[
#     "http://localhost:5173",
#     "https://realpitch-1.onrender.com",
#     "https://realpitch009.vercel.app"
# ])

# ✅ Route with cross-origin decorator
# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         # ✅ Step 1: Parse and log request
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         if not image_urls or not audio_url or not session_id:
#             return jsonify({"error": "Missing required fields"}), 400

#         # ✅ Step 2: Prepare temp folder
#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         # ✅ Step 3: Download audio file
#         audio_data = requests.get(audio_url)
#         print("🎧 Audio Content-Type:", audio_data.headers.get("Content-Type"))
#         if audio_data.status_code != 200:
#             return jsonify({"error": "Failed to download audio"}), 400

#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)

#         # ✅ Step 4: Analyze audio length
#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])

#         # ✅ Step 5: Download and convert images
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
#                 print(f"⚠️ Skipping invalid image {temp_path}: {e}")

#         if not frame_paths:
#             return jsonify({"error": "No valid images to generate slideshow"}), 400

#         # ✅ Step 6: Generate video slideshow
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

#         # ✅ Step 7: Merge slideshow with audio
#         output_video_path = os.path.join(tmpfolderpath, "final_output.mp4")
#         cmd_merge = [
#             "ffmpeg", "-i", slideshow_path, "-i", audio_path,
#             "-c:v", "copy", "-c:a", "aac", "-shortest", "-y", output_video_path
#         ]
#         subprocess.run(cmd_merge, check=True, capture_output=True, text=True)

#         # ✅ Step 8: Upload to S3
#         s3_key = f"{session_id}/final_output.mp4"
#         s3.upload_file(output_video_path, S3_BUCKET_NAME, s3_key)
#         s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

#         print("✅ Final video uploaded to:", s3_url)
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
#         print("❌ Unexpected error:", str(e))
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         # 🔍 Add a test GET request to audio_url only
#         audio_data = requests.get(audio_url)
#         print("🎧 Audio download test status:", audio_data.status_code)

#         return jsonify({"message": "Audio downloaded OK"}), 200

#     except Exception as e:
#         print("❌ Test failed:", str(e))
#         return jsonify({"error": str(e)}), 500
# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         audio_data = requests.get(audio_url)
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)
#         print("✅ Audio saved at:", audio_path)

#         # ✅ Now test ffmpeg probe
#         probe = ffmpeg.probe(audio_path)
#         print("🎯 Audio duration:", probe['format']['duration'])

#         return jsonify({"message": "Audio probe succeeded!"}), 200

#     except Exception as e:
#         print("❌ Probe test failed:", str(e))
#         return jsonify({"error": str(e)}), 500
# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         # Save audio
#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         audio_data = requests.get(audio_url)
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)

#         # FFmpeg probe
#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])
#         print("🎯 Audio duration:", audio_duration)

#         # ✅ Now test downloading & saving image frames
#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             print(f"📥 Downloading image {i}: {url}")
#             response = requests.get(url)
#             temp_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
#             with open(temp_path, "wb") as f:
#                 f.write(response.content)

#             try:
#                 with Image.open(temp_path) as im:
#                     frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
#                     rgb_im = im.convert("RGB")
#                     rgb_im.save(frame_path, "JPEG")
#                     frame_paths.append(frame_path)
#                     print(f"✅ Frame {i} saved:", frame_path)
#             except Exception as e:
#                 print(f"⚠️ Skipping invalid image {i}: {e}")

#         print("📸 Total frames created:", len(frame_paths))

#         return jsonify({"message": "Image processing succeeded!"}), 200

#     except Exception as e:
#         print("❌ Image test failed:", str(e))
#         return jsonify({"error": str(e)}), 500


# import os
# import requests
# import subprocess
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from config.s3_config import s3
# from PIL import Image
# import ffmpeg
# from flask_cors import CORS, cross_origin

# generate_video_blueprint = Blueprint("generate_video", __name__)
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# CORS(generate_video_blueprint, origins=[
#     "http://localhost:5173",
#     "https://realpitch-1.onrender.com",
#     "https://realpitch009.vercel.app"
# ])

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         # 🔊 Download audio
#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         audio_data = requests.get(audio_url)
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)
#         print("✅ Audio saved:", audio_path)

#         # ⏱️ Probe audio duration
#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])
#         print("🎯 Audio duration:", audio_duration)

#         # 🖼 Download and convert images
#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             print(f"📥 Downloading image {i}: {url}")
#             response = requests.get(url)
#             raw_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
#             with open(raw_path, "wb") as f:
#                 f.write(response.content)

#             try:
#                 with Image.open(raw_path) as im:
#                     frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
#                     rgb_im = im.convert("RGB")
#                     rgb_im.save(frame_path, "JPEG")
#                     frame_paths.append(frame_path)
#                     print(f"✅ Frame {i} saved:", frame_path)
#             except Exception as e:
#                 print(f"⚠️ Skipping image {i}: {e}")

#         print("📸 Total frames ready:", len(frame_paths))

#         if not frame_paths:
#             return jsonify({"error": "No valid images found"}), 400

#         # 🎬 Generate slideshow with ffmpeg
#         seconds_per_image = audio_duration / len(frame_paths)
#         framerate = 1 / seconds_per_image

#         slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
#         cmd_slideshow = [
#             "ffmpeg", "-framerate", f"{framerate:.4f}", "-i",
#             os.path.join(tmpfolderpath, "frame_%03d.jpg"),
#             "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
#             "-y", slideshow_path
#         ]

#         print("🎬 Running ffmpeg slideshow command:")
#         print(" ".join(cmd_slideshow))

#         subprocess.run(cmd_slideshow, check=True, capture_output=True, text=True)
#         print("✅ Slideshow video created:", slideshow_path)

#         return jsonify({"message": "Slideshow generation succeeded!"}), 200

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
#         print("❌ Unexpected error:", str(e))
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500

# import os
# import requests
# import subprocess
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from config.s3_config import s3
# from PIL import Image
# import ffmpeg
# from flask_cors import CORS, cross_origin

# generate_video_blueprint = Blueprint("generate_video", __name__)
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# CORS(generate_video_blueprint, origins=[
#     "http://localhost:5173",
#     "https://realpitch-1.onrender.com",
#     "https://realpitch009.vercel.app"
# ])

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         # 🔊 Download audio
#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         audio_data = requests.get(audio_url)
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)
#         print("✅ Audio saved:", audio_path)

#         # ⏱️ Get duration
#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])
#         print("🎯 Audio duration:", audio_duration)

#         # 🖼 Download images and convert
#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             print(f"📥 Downloading image {i}: {url}")
#             response = requests.get(url)
#             raw_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
#             with open(raw_path, "wb") as f:
#                 f.write(response.content)

#             try:
#                 with Image.open(raw_path) as im:
#                     frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
#                     rgb_im = im.convert("RGB")
#                     rgb_im.save(frame_path, "JPEG")
#                     frame_paths.append(frame_path)
#                     print(f"✅ Frame {i} saved:", frame_path)
#             except Exception as e:
#                 print(f"⚠️ Skipping image {i}: {e}")

#         print("📸 Total frames created:", len(frame_paths))

#         if not frame_paths:
#             return jsonify({"error": "No valid images found"}), 400

#         # 🎬 Attempt to generate slideshow with ffmpeg
#         seconds_per_image = audio_duration / len(frame_paths)
#         framerate = 1 / seconds_per_image

#         slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
#         cmd_slideshow = [
#             "ffmpeg", "-framerate", f"{framerate:.4f}", "-i",
#             os.path.join(tmpfolderpath, "frame_%03d.jpg"),
#             "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
#             "-y", slideshow_path
#         ]

#         print("🎬 About to run slideshow ffmpeg command:")
#         print(" ".join(cmd_slideshow))

#         try:
#             result = subprocess.run(cmd_slideshow, check=True, capture_output=True, text=True)
#             print("✅ Slideshow created successfully")
#             print("stdout:", result.stdout)
#             print("stderr:", result.stderr)
#         except subprocess.CalledProcessError as e:
#             print("❌ FFmpeg FAILED")
#             print("Command:", e.cmd)
#             print("Return code:", e.returncode)
#             print("stdout:", e.stdout)
#             print("stderr:", e.stderr)
#             return jsonify({
#                 "error": "Slideshow ffmpeg failed",
#                 "return_code": e.returncode,
#                 "stderr": e.stderr,
#                 "stdout": e.stdout
#             }), 500

#         return jsonify({"message": "Slideshow step completed"}), 200

#     except Exception as e:
#         print("❌ Unexpected error:", str(e))
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500

# @generate_video_blueprint.route("/testffmpeg", methods=["GET"])
# @cross_origin(origins="https://realpitch009.vercel.app")  # or "*" for now
# def test_ffmpeg():
#     try:
#         result = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
#         print("✅ FFmpeg found!")
#         print("stdout:", result.stdout)
#         return jsonify({"ffmpeg_version": result.stdout}), 200
#     except FileNotFoundError:
#         print("❌ FFmpeg is NOT installed on this server.")
#         return jsonify({"error": "ffmpeg not found"}), 500
#     except subprocess.CalledProcessError as e:
#         print("❌ ffmpeg exists but crashed:", e.stderr)
#         return jsonify({"error": e.stderr}), 500


# import os
# import requests
# import subprocess
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from config.s3_config import s3
# from PIL import Image
# import ffmpeg
# from flask_cors import CORS, cross_origin

# generate_video_blueprint = Blueprint("generate_video", __name__)
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# # ✅ Enable CORS on blueprint
# CORS(generate_video_blueprint, origins=[
#     "http://localhost:5173",
#     "https://realpitch009.vercel.app",
#     "https://realpitch-1.onrender.com"
# ])

# # ✅ Video Generation Route
# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# @cross_origin(origins="https://realpitch009.vercel.app")
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#         print("✅ JSON parsed:", data)

#         image_urls = data.get("image_urls")
#         audio_url = data.get("audio_url")
#         session_id = data.get("session_id")
#         print("🖼 image_urls:", image_urls)
#         print("🔊 audio_url:", audio_url)
#         print("📦 session_id:", session_id)

#         tmpfolderpath = os.path.join("/tmp", session_id)
#         os.makedirs(tmpfolderpath, exist_ok=True)

#         # 🔊 Download audio
#         audio_path = os.path.join(tmpfolderpath, "audio.mp3")
#         audio_data = requests.get(audio_url)
#         with open(audio_path, "wb") as f:
#             f.write(audio_data.content)
#         print("✅ Audio saved:", audio_path)

#         # ⏱️ Get audio duration
#         probe = ffmpeg.probe(audio_path)
#         audio_duration = float(probe['format']['duration'])
#         print("🎯 Audio duration:", audio_duration)

#         # 🖼 Download and convert images
#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             print(f"📥 Downloading image {i}: {url}")
#             response = requests.get(url)
#             raw_path = os.path.join(tmpfolderpath, f"raw_{i:03d}")
#             with open(raw_path, "wb") as f:
#                 f.write(response.content)

#             try:
#                 with Image.open(raw_path) as im:
#                     frame_path = os.path.join(tmpfolderpath, f"frame_{i:03d}.jpg")
#                     rgb_im = im.convert("RGB")
#                     rgb_im.save(frame_path, "JPEG")
#                     frame_paths.append(frame_path)
#                     print(f"✅ Frame {i} saved:", frame_path)
#             except Exception as e:
#                 print(f"⚠️ Skipping image {i}: {e}")

#         if not frame_paths:
#             return jsonify({"error": "No valid images"}), 400

#         print("📸 Total frames:", len(frame_paths))

#         # 🎬 Slideshow generation
#         seconds_per_image = audio_duration / len(frame_paths)
#         framerate = max(0.5, 1 / seconds_per_image)  # ⛑ prevent too-low fps
#         slideshow_path = os.path.join(tmpfolderpath, "slideshow.mp4")
#         frame_pattern = os.path.join(tmpfolderpath, "frame_%03d.jpg")

#         cmd_slideshow = [
#             "ffmpeg", "-y",
#             "-framerate", f"{framerate:.4f}",
#             "-i", frame_pattern,
#             "-c:v", "libx264",
#             "-r", "30",
#             "-pix_fmt", "yuv420p",
#             slideshow_path
#         ]

#         print("🎬 Running slideshow ffmpeg command:")
#         print(" ".join(cmd_slideshow))

#         try:
#             result = subprocess.run(cmd_slideshow, check=True, capture_output=True, text=True)
#             print("✅ Slideshow created")
#             print("FFmpeg stdout:\n", result.stdout)
#             print("FFmpeg stderr:\n", result.stderr)
#         except subprocess.CalledProcessError as e:
#             print("❌ FFmpeg slideshow FAILED")
#             print("Command:", e.cmd)
#             print("Return code:", e.returncode)
#             print("stdout:", e.stdout)
#             print("stderr:", e.stderr)
#             return jsonify({
#                 "error": "slideshow_failed",
#                 "return_code": e.returncode,
#                 "stderr": e.stderr,
#                 "stdout": e.stdout
#             }), 500

#         return jsonify({"message": "Slideshow step completed"}), 200

#     except Exception as e:
#         print("❌ Unexpected error:", str(e))
#         return jsonify({
#             "error": "Internal server error",
#             "details": str(e)
#         }), 500


# import os
# import requests
# import subprocess
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from config.s3_config import s3
# from werkzeug.utils import secure_filename

# generate_video_blueprint = Blueprint("generate_video", __name__)
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# def generatevideo():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json()
#     except Exception as e:
#         return jsonify({"error": "Invalid JSON body", "details": str(e)}), 400

#     image_urls = data.get("image_urls")
#     audio_url = data.get("audio_url")
#     session_id = data.get("session_id")

#     if not image_urls or not audio_url or not session_id:
#         return jsonify({"error": "Missing required fields"}), 400

#     print("✅ JSON parsed:", data)
#     print("🖼 image_urls:", image_urls)
#     print("🔊 audio_url:", audio_url)
#     print("📦 session_id:", session_id)

#     temp_dir = f"/tmp/{session_id}"
#     os.makedirs(temp_dir, exist_ok=True)

#     # Step 1: Download Images
#     for idx, url in enumerate(image_urls):
#         response = requests.get(url)
#         if response.status_code != 200:
#             return jsonify({"error": f"Failed to download image {url}"}), 400
#         img_path = os.path.join(temp_dir, f"frame_{idx:03d}.jpg")
#         with open(img_path, "wb") as f:
#             f.write(response.content)
#         print(f"✅ Frame {idx} saved:", img_path)

#     frame_count = len(image_urls)
#     print(f"📸 Total frames created: {frame_count}")

#     # Step 2: Create slideshow video using ffmpeg
#     slideshow_path = os.path.join(temp_dir, "slideshow.mp4")
#     cmd_slideshow = [
#         "ffmpeg",
#         "-y",
#         "-r", "1",
#         "-i", f"{temp_dir}/frame_%03d.jpg",
#         "-c:v", "libx264",
#         "-vf", "fps=25",
#         "-pix_fmt", "yuv420p",
#         slideshow_path
#     ]

#     print("🎬 Running FFmpeg command for slideshow:")
#     print(" ".join(cmd_slideshow))

#     result = subprocess.run(cmd_slideshow, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#     print("📥 FFmpeg return code:", result.returncode)
#     print("📥 FFmpeg stdout:\n", result.stdout)
#     print("📥 FFmpeg stderr:\n", result.stderr)

#     if result.returncode != 0:
#         return jsonify({
#             "error": "slideshow_failed",
#             "return_code": result.returncode,
#             "stderr": result.stderr,
#             "stdout": result.stdout
#         }), 500

#     print("🎞 Slideshow video created:", slideshow_path)

#     # Optional: Upload to S3 or merge with audio in next step...
#     return jsonify({"message": "Slideshow video generated successfully!"})

# import os
# import requests
# import subprocess
# import tempfile
# import shutil
# import psutil
# from flask import Blueprint, request, jsonify
# from uuid import uuid4
# from werkzeug.utils import secure_filename

# generate_video_blueprint = Blueprint("generate_video", __name__)
# S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# def log_memory(stage):
#     used = psutil.virtual_memory().used / 1024 / 1024
#     print(f"🧠 Memory after {stage}: {used:.2f} MB")

# @generate_video_blueprint.route("/generatevideo", methods=["POST"])
# def generate_video():
#     print("🔔 /generatevideo endpoint hit")

#     try:
#         data = request.get_json(force=True)
#         print("✅ JSON parsed:", data)
#     except Exception as e:
#         print("❌ Failed to parse JSON:", str(e))
#         return jsonify({"error": "Invalid JSON body"}), 400

#     image_urls = data.get("image_urls")
#     audio_url = data.get("audio_url")
#     session_id = data.get("session_id")

#     if not image_urls or not audio_url or not session_id:
#         print("❌ Missing required fields")
#         return jsonify({"error": "Missing fields"}), 400

#     print("🖼 image_urls:", image_urls)
#     print("🔊 audio_url:", audio_url)
#     print("📦 session_id:", session_id)
#     log_memory("start")

#     try:
#         temp_dir = tempfile.mkdtemp()
#         print("📁 Temp dir created:", temp_dir)

#         frame_paths = []
#         for i, url in enumerate(image_urls):
#             try:
#                 response = requests.get(url, timeout=10)
#                 image_path = os.path.join(temp_dir, f"frame_{i:03}.jpg")
#                 with open(image_path, "wb") as f:
#                     f.write(response.content)
#                 frame_paths.append(image_path)
#                 print(f"✅ Frame {i} saved: {image_path}")
#                 log_memory(f"after image {i}")
#             except Exception as e:
#                 print(f"❌ Failed to download image {i}:", str(e))

#         # Download audio
#         try:
#             audio_path = os.path.join(temp_dir, "audio.mp3")
#             audio_response = requests.get(audio_url, timeout=10)
#             with open(audio_path, "wb") as f:
#                 f.write(audio_response.content)
#             print("✅ Audio saved:", audio_path)
#             log_memory("after audio download")
#         except Exception as e:
#             print("❌ Failed to download audio:", str(e))
#             return jsonify({"error": "Audio download failed"}), 500

#         # Generate video from images
#         try:
#             video_path = os.path.join(temp_dir, "video.mp4")
#             frame_rate = len(frame_paths) / 6  # example: 6 seconds total
#             ffmpeg_cmd = [
#                 "ffmpeg",
#                 "-y",
#                 "-framerate", str(frame_rate),
#                 "-i", os.path.join(temp_dir, "frame_%03d.jpg"),
#                 "-c:v", "libx264",
#                 "-pix_fmt", "yuv420p",
#                 video_path
#             ]
#             print("🎬 Running FFmpeg:", " ".join(ffmpeg_cmd))
#             subprocess.run(ffmpeg_cmd, check=True)
#             print("✅ Video created:", video_path)
#             log_memory("after video creation")
#         except Exception as e:
#             print("❌ FFmpeg failed:", str(e))
#             return jsonify({"error": "Video generation failed"}), 500

#         # Combine video + audio
#         try:
#             final_path = os.path.join(temp_dir, f"{session_id}_final.mp4")
#             ffmpeg_cmd = [
#                 "ffmpeg",
#                 "-y",
#                 "-i", video_path,
#                 "-i", audio_path,
#                 "-c:v", "copy",
#                 "-c:a", "aac",
#                 "-shortest",
#                 final_path
#             ]
#             print("🔗 Combining audio and video")
#             subprocess.run(ffmpeg_cmd, check=True)
#             print("✅ Final video created:", final_path)
#             log_memory("after audio+video combine")
#         except Exception as e:
#             print("❌ Failed to combine video and audio:", str(e))
#             return jsonify({"error": "Failed to combine video and audio"}), 500

#         # Upload to S3
#         try:
#             import boto3
#             s3 = boto3.client("s3")
#             s3_key = f"final_videos/{session_id}.mp4"
#             s3.upload_file(final_path, S3_BUCKET_NAME, s3_key, ExtraArgs={"ContentType": "video/mp4"})
#             s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
#             print("✅ Uploaded to S3:", s3_url)
#             log_memory("after S3 upload")
#         except Exception as e:
#             print("❌ S3 upload failed:", str(e))
#             return jsonify({"error": "S3 upload failed"}), 500

#         return jsonify({"video_url": s3_url}), 200

#     finally:
#         try:
#             shutil.rmtree(temp_dir)
#             print("🧹 Temp files cleaned up:", temp_dir)
#         except Exception as e:
#             print("⚠️ Failed to clean temp dir:", str(e))

import os
import requests
import subprocess
import tempfile
import shutil
import psutil
from flask import Blueprint, request, jsonify
from uuid import uuid4
from werkzeug.utils import secure_filename

generate_video_blueprint = Blueprint("generate_video", __name__)
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def log_memory(stage):
    process = psutil.Process(os.getpid())
    used = process.memory_info().rss / 1024 / 1024  # RSS = resident set size
    print(f"🧠 Memory after {stage}: {used:.2f} MB")

@generate_video_blueprint.route("/generatevideo", methods=["POST"])
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
        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url, timeout=10)
                image_path = os.path.join(temp_dir, f"frame_{i:03}.jpg")
                with open(image_path, "wb") as f:
                    f.write(response.content)
                frame_paths.append(image_path)
                print(f"✅ Frame {i} saved: {image_path}")
                log_memory(f"after image {i}")
            except Exception as e:
                print(f"❌ Failed to download image {i}:", str(e))

        # Download audio
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

        # Generate video from images
        try:
            video_path = os.path.join(temp_dir, "video.mp4")
            frame_rate = len(frame_paths) / 6  # 6 second video
            ffmpeg_cmd = [
                "ffmpeg",
                "-y",
                "-framerate", str(frame_rate),
                "-i", os.path.join(temp_dir, "frame_%03d.jpg"),
                "-vf", "scale=720:1280",  # reduce memory
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                video_path
            ]
            print("🎬 Running FFmpeg:", " ".join(ffmpeg_cmd))
            log_memory("before video ffmpeg")
            subprocess.run(ffmpeg_cmd, check=True, timeout=60)
            print("✅ Video created:", video_path)
            log_memory("after video ffmpeg")
        except subprocess.TimeoutExpired:
            print("⏱️ FFmpeg video generation timed out")
            return jsonify({"error": "FFmpeg timeout"}), 500
        except Exception as e:
            print("❌ FFmpeg video generation failed:", str(e))
            return jsonify({"error": "Video generation failed"}), 500

        # Combine video and audio
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
            log_memory("before audio combine")
            subprocess.run(ffmpeg_cmd, check=True, timeout=60)
            print("✅ Final video created:", final_path)
            log_memory("after audio combine")
        except subprocess.TimeoutExpired:
            print("⏱️ FFmpeg combine timed out")
            return jsonify({"error": "FFmpeg combine timeout"}), 500
        except Exception as e:
            print("❌ Failed to combine video and audio:", str(e))
            return jsonify({"error": "Failed to combine video and audio"}), 500

        # Upload to S3
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

        return jsonify({"video_url": s3_url}), 200

    finally:
        try:
            shutil.rmtree(temp_dir)
            print("🧹 Temp files cleaned up:", temp_dir)
        except Exception as e:
            print("⚠️ Failed to clean temp dir:", str(e))
