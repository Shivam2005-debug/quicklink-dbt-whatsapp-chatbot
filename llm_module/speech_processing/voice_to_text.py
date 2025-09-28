# # speech_processing/voice_to_text.py
# import speech_recognition as sr
# import requests
# import os
# import io

# def voice_to_text(audio_url: str, twilio_auth_token: str) -> str:
#     """
#     Download audio from a URL and convert it to text.
#     """
#     try:
#         # Download the audio file from Twilio
#         response = requests.get(audio_url, auth=("AC...", twilio_auth_token)) # Replace with your Account SID
#         audio_content = response.content

#         recognizer = sr.Recognizer()
        
#         # Use a temporary file to process the audio
#         with sr.AudioFile(io.BytesIO(audio_content)) as source:
#             audio = recognizer.record(source)
            
#         # Recognize speech using Google Web Speech API
#         # It supports multiple languages automatically
#         text = recognizer.recognize_google(audio, language="en-IN") # Default to Indian English, but can be auto-detected
        
#         return text.lower()
#     except sr.UnknownValueError:
#         return "Could not understand the audio."
#     except sr.RequestError as e:
#         return f"Could not request results; {e}"
#     except Exception as e:
#         return f"Error processing audio: {e}"

# llm_module/speech_processing/voice_to_text.py
import speech_recognition as sr
import requests
import io
import os
import soundfile as sf  # NEW: Import soundfile

def voice_to_text(audio_url: str, twilio_auth_token: str) -> str:
    """
    Download audio from a URL, convert it to WAV format using soundfile, and transcribe to text.
    """
    try:
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        
        # Download the audio file from Twilio
        response = requests.get(audio_url, auth=(twilio_account_sid, twilio_auth_token))
        
        if response.status_code != 200:
            return f"Error: Could not download audio file. Status code: {response.status_code}"

        audio_content = response.content
        
        # --- NEW CONVERSION LOGIC using soundfile ---
        # 1. Read the downloaded audio data (OGG/Opus) from the in-memory file
        data, samplerate = sf.read(io.BytesIO(audio_content))

        # 2. Write the raw audio data as a WAV file into a new in-memory buffer
        wav_buffer = io.BytesIO()
        sf.write(wav_buffer, data, samplerate, format='WAV', subtype='PCM_16')
        wav_buffer.seek(0)
        # --- END OF NEW LOGIC ---

        recognizer = sr.Recognizer()
        
        # Use the NEW WAV buffer with AudioFile
        with sr.AudioFile(wav_buffer) as source:
            audio = recognizer.record(source)
            
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio, language="en-IN")
        
        return text.lower()
        
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        # This will catch errors if soundfile can't read the format
        return f"Error processing audio: {e}"