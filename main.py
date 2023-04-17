import os
import replicate
from flask import Flask, request, jsonify, send_from_directory, Response, send_file

app = Flask(__name__)

REPLICATE_API_TOKEN = os.environ["REPLICATE_API_TOKEN"]

@app.route("/")
def index():
    return "Midjourney Diffusion Plugin is running."

@app.route("/.well-known/ai-plugin.json", methods=["GET"])
def send_ai_plugin_json():
    with open(os.path.join(os.getcwd(), ".well-known", "ai-plugin.json"), "r") as f:
        return Response(f.read(), content_type="application/json")

@app.route("/openapi.yaml", methods=["GET"])
def send_openapi_spec():
    with open(os.path.join(os.getcwd(), "openapi.yaml"), "r") as f:
        return Response(f.read(), content_type="text/yaml")

@app.route("/logo.png")
def logo():
    return send_file(os.path.join(os.getcwd(), "logo.png"))

@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")
    output = replicate.run(
        "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b",
        input={"prompt": prompt}
    )
    image_url = output[0] if output else None
    return jsonify({"image_url": image_url})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7080)

