import os
from flask import Flask,jsonify
from routes.upload_routes import upload_blueprint
from routes.generate_script import generate_script_blueprint
from routes.generate_audio import generate_audio_blueprint
from routes.generate_video import generate_video_blueprint
from flask_cors import CORS
from dotenv import  *

app=Flask(__name__)
CORS(app)
@app.route("/")

def home():
    print("jeje")
    print(os.getenv("REGION_NAME"))

    return jsonify({
        "message":"RealPitch Backend is working"
    })
app.register_blueprint(upload_blueprint)
app.register_blueprint(generate_script_blueprint)
app.register_blueprint(generate_audio_blueprint)
app.register_blueprint(generate_video_blueprint)
if __name__ == "__main__":
    app.run(debug=True)