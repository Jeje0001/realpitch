import os
from flask import Blueprint, request, jsonify
from openai import OpenAI
from flask_cors import CORS

generate_script_blueprint = Blueprint('generate_script', __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CORS(generate_script_blueprint, origins=["http://localhost:5173","https://realpitch-1.onrender.com"])

@generate_script_blueprint.route("/generatescript", methods=['POST'])
def generatescript():
    description = request.json.get("description")

    if not description:
        return jsonify({'error': "No description provided"}), 400

    try:
        prompt = f"""
You are a professional real estate video scriptwriter.

Write a short, polished voiceover script for a real estate listing video.

Only output clean narration text — no scene instructions, no brackets, no labels like 'Narrator:'.

Property description: {description}
        """.strip()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        script = response.choices[0].message.content.strip()

    except Exception as e:
        return jsonify({"error": f"Script generation failed: {str(e)}"}), 500

    return jsonify({"script": script}), 200
