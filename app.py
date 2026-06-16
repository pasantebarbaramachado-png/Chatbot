import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
ai_client = genai.Client()

@app.route("/chat", methods=["POST"])
def chat():
    # Recibe los datos directamente del mensaje enviado
    data = request.json or {}
    mensaje_usuario = data.get('message', '')
    
    if not mensaje_usuario:
        return jsonify({"reply": "No se recibió ningún mensaje."}), 400

    try:
        # Gemini procesa la respuesta
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensaje_usuario
        )
        respuesta_bot = response.text
    except Exception as e:
        respuesta_bot = "Lo siento, tuve un problema al procesar tu mensaje."

    return jsonify({"reply": respuesta_bot})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

