# whatsapp_bot/bot.py
from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys
import uuid
from langdetect import detect

# Add parent directory to path to import llm_module
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_module.llm_integration.gemini_api import get_gemini_response
from llm_module.speech_processing.text_to_speech import text_to_speech
from llm_module.speech_processing.voice_to_text import voice_to_text

load_dotenv()

app = Flask(__name__)

# Twilio REST Client Initialization
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory session management
user_sessions = {}
TEMP_AUDIO_DIR = "temp_audio"

# Create a directory for temporary audio files if it doesn't exist
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Handle incoming WhatsApp messages."""
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From")
    
    is_voice_message = False
    if 'MediaUrl0' in request.values and 'audio' in request.values.get('MediaContentType0', ''):
        audio_url = request.values['MediaUrl0']
        incoming_msg = voice_to_text(audio_url, TWILIO_AUTH_TOKEN)
        is_voice_message = True

    resp = MessagingResponse()
    
    if from_number not in user_sessions:
        user_sessions[from_number] = {"mode": None}
        resp.message("Welcome to QuickLink DBT!How would you like to receive responses?\n1. Text\n2. Voice")
        return str(resp)

    session = user_sessions[from_number]

    if not session.get("mode"):
        if "1" in incoming_msg or "text" in incoming_msg.lower():
            session["mode"] = "text"
            resp.message("Text mode selected. How can I help you today?")
        elif "2" in incoming_msg or "voice" in incoming_msg.lower():
            session["mode"] = "voice"
            resp.message("Voice mode selected. Please send your query as a text or voice note.")
        else:
            resp.message("Invalid selection. Please choose:\n1. Text\n2. Voice")
        return str(resp)

    # Main logic - if it's a real query, process it.
    if incoming_msg:
        try:
            lang = detect(incoming_msg)
            if lang not in ['en', 'hi', 'mr']:
                lang = 'en'
            
            bot_response_text = get_gemini_response(incoming_msg, lang=lang)

            if session["mode"] == "text":
                resp.message(bot_response_text)
            else: # Voice mode
                audio_bytes = text_to_speech(bot_response_text, lang=lang)
                if audio_bytes:
                    filename = f"{uuid.uuid4()}.mp3"
                    file_path = os.path.join(TEMP_AUDIO_DIR, filename)
                    
                    with open(file_path, "wb") as f:
                        f.write(audio_bytes)
                    
                    # The public URL for the audio file, served by our Flask app via Ngrok
                    media_url = f"{request.host_url}audio/{filename}"
                    
                    # Use the REST API to send the voice message
                    client.messages.create(
                        from_=TWILIO_WHATSAPP_NUMBER,
                        to=from_number,
                        media_url=[media_url]
                    )
                else:
                    # Fallback to text if TTS fails
                    resp.message("Sorry, I couldn't generate a voice response. Here is the answer in text:\n\n" + bot_response_text)

            # whatsapp_bot/bot.py
# # ... (imports and setup are the same) ...

# # --- THIS IS THE ONLY CHANGE NEEDED IN THIS FILE ---
# # Inside the whatsapp_reply function, find this section and modify it:

#             else: # Voice mode
#                 audio_bytes = text_to_speech(bot_response_text, lang=lang)
#                 if audio_bytes:
#                     filename = f"{uuid.uuid4()}.mp3"
#                     file_path = os.path.join(TEMP_AUDIO_DIR, filename)
                    
#                     with open(file_path, "wb") as f:
#                         f.write(audio_bytes)
                    
#                     media_url = f"{request.host_url}audio/{filename}"
                    
#                     # MODIFICATION: Check for credentials before sending
#                     if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
#                         print(f"--- SIMULATING VOICE REPLY: Sending audio file {media_url} ---")
#                         client.messages.create(
#                             from_=TWILIO_WHATSAPP_NUMBER,
#                             to=from_number,
#                             media_url=[media_url]
#                         )
#                     else:
#                         print("--- Twilio credentials not found. Skipping actual voice message send. ---")
#                         print(f"--- Voice response saved to: {file_path} ---")
#                         # You can manually open this file to hear the audio.

#                 else:
#                     resp.message("Sorry, I couldn't generate a voice response. Here is the answer in text:\n\n" + bot_response_text)
# # ... (the rest of the file is the same) ...
                
        except Exception as e:
            print(f"Error during processing: {e}")
            resp.message(f"An error occurred. Please try again.")

    # Return the TwiML response. It will be empty for voice mode, which is correct.
    return str(resp)

# New route to serve the temporary audio files
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(TEMP_AUDIO_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)