from gtts import gTTS
import os
import random
import string

# Check if we're in a production environment
is_production = os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true'

def speak(text):
    print(f"🔊 Nova: {text}")
    
    # In production, just print the text
    if is_production:
        return
        
    # In development, use text-to-speech
    try:
        # Only import playsound in development environment
        try:
            from playsound import playsound
            filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + ".mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except ImportError:
            print(f"Text-to-speech not available: playsound module not found")
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        # Continue execution even if TTS fails
