# speech_processing/text_to_speech.py
from gtts import gTTS
import io

def text_to_speech(text: str, lang: str = "en"):
    """
    Convert text to speech and return the audio content as bytes.
    lang: 'en', 'hi', 'mr'
    """
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to memory buffer
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        
        return mp3_buffer.getvalue()
    except Exception as e:
        print(f"TTS Error: {e}")
        return None