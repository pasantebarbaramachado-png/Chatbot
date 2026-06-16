import os
from flask import Flask, request
from google import genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Inicializa Gemini. Buscará automáticamente la variable GEMINI_API_KEY en Render
ai_client = genai.Client()

@app.route("/webhook", methods=["POST"])
def webhook():
    # Lee el mensaje que enviaste desde WhatsApp
    mensaje_usuario = request.values.get('Body', '')
    
    try:
        # Gemini genera la respuesta inteligente
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensaje_usuario
        )
        respuesta_bot = response.text
    except Exception as e:
        # Si hay un error con la API Key, el bot te avisará en WhatsApp
        respuesta_bot = f"Error de conexión con Gemini: {str(e)}"

    # Envia el texto de regreso a Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(respuesta_bot)
    
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
