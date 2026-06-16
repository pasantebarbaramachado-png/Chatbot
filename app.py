import os
from flask import Flask, request
from google import genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
ai_client = genai.Client()

@app.route("/", methods=["POST"])
def webhook():
    mensaje_usuario = request.values.get('Body', '')
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensaje_usuario
        )
        respuesta_bot = response.text
    except Exception as e:
        respuesta_bot = "Lo siento, tuve un problema al procesar tu mensaje."

    twilio_response = MessagingResponse()
    twilio_response.message(respuesta_bot)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
