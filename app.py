from flask import Flask, request, jsonify
import openai
import pytesseract
from PIL import Image
import io
import base64

app = Flask(__name__)

# Configura tu clave de API de OpenAI
openai.api_key = 'APIKEY'

@app.route('/generate_poem', methods=['POST'])
def generate_poem():
    data = request.json
    text = data.get('text', '')
    
    if 'image' in data:
        image_data = data['image']
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        text += pytesseract.image_to_string(image)
    
    if not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Genera un poema a partir del siguiente texto:\n\n{text}",
        max_tokens=150
    )
    poem = response.choices[0].text.strip()
    return jsonify({'poem': poem})

if __name__ == '__main__':
    app.run(debug=True)
