# whatsapp_bot/bot.py
from flask import Flask, request
# send_from_directory is no longer needed
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys
# uuid is no longer needed
import requests # Make sure 'requests' is imported if it wasn't already
from langdetect import detect

# Add parent directory to path to import llm_module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
# We no longer need to manage a temporary audio directory
# TEMP_AUDIO_DIR = "temp_audio"
# if not os.path.exists(TEMP_AUDIO_DIR):
#     os.makedirs(TEMP_AUDIO_DIR)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Handle incoming WhatsApp messages, including mode switching and robust audio replies."""
    incoming_msg = request.values.get("Body", "")
    from_number = request.values.get("From")
    
    # Handle voice input
    if 'MediaUrl0' in request.values and 'audio' in request.values.get('MediaContentType0', ''):
        audio_url = request.values['MediaUrl0']
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
             resp = MessagingResponse()
             resp.message("Server is not configured to handle voice notes. Please use text.")
             return str(resp)
        incoming_msg = voice_to_text(audio_url, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    resp = MessagingResponse()
    
    # Handle New User Session
    if from_number not in user_sessions:
        user_sessions[from_number] = {"mode": "text"}
        resp.message("Welcome to QuickLink DBT! I'm currently in *Text Mode*.\n\nHow can I help you?\n\n_(You can type voice mode to switch to audio replies at any time.)_")
        return str(resp)

    session = user_sessions[from_number]
    msg_lower = incoming_msg.lower().strip()

    # Handle Mode Switching
    if msg_lower in ["switch to voice", "voice mode", "audio mode"]:
        session["mode"] = "voice"
        resp.message("✅ Switched to *Voice Mode*. I will now reply with audio.")
        return str(resp)

    if msg_lower in ["switch to text", "text mode"]:
        session["mode"] = "text"
        resp.message("✅ Switched to *Text Mode*. I will now reply with text.")
        return str(resp)

    # Main Q&A Logic
    if not incoming_msg:
        resp.message("I didn't receive a message. Please ask a question.")
        return str(resp)

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
                # --- NEW: UPLOAD AUDIO TO A TEMPORARY HOST ---
                files = {'file': ('response.mp3', audio_bytes, 'audio/mpeg')}
                try:
                    # Using tmpfiles.org as a free, temporary host
                    upload_response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
                    upload_response.raise_for_status()
                    data = upload_response.json()
                    
                    # The URL format for this host is specific
                    media_url = data['data']['url'].replace('https://tmpfiles.org/', 'https://tmpfiles.org/dl/')

                    client.messages.create(
                        from_=TWILIO_WHATSAPP_NUMBER,
                        to=from_number,
                        media_url=[media_url]
                    )
                except requests.exceptions.RequestException as upload_error:
                    print(f"Error uploading audio file: {upload_error}")
                    resp.message("Sorry, I couldn't prepare the voice response. Here is the answer in text:\n\n" + bot_response_text)
                # --- END OF NEW LOGIC ---
            else:
                resp.message("Sorry, I couldn't generate a voice response. Here is the answer in text:\n\n" + bot_response_text)
            
    except Exception as e:
        print(f"Error during processing: {e}")
        resp.message("I'm sorry, an error occurred. Please try again.")

    return str(resp)

# The '/audio/<filename>' route is no longer needed and has been removed.

if __name__ == "__main__":
    app.run(port=5000, debug=True)