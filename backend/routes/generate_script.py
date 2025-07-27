import os
from flask import Blueprint, request, jsonify
import openai

generate_script_blueprint = Blueprint('generate_script', __name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@generate_script_blueprint.route("/generatescript", methods=['POST'])
def generatescript():
    description = request.json.get("description")

    if not description:
        return jsonify({'error': "No description provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a real estate video scriptwriter."},
                {"role": "user", "content": f"Write a short video script for this property: {description}"}
            ]
        )
        script = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": f"Script generation failed: {str(e)}"}), 500

    return jsonify({"script": script}), 200
