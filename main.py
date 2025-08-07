# main.py

from gtts import gTTS
import speech_recognition as sr
import datetime
import random
import os
import getpass
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
# playsound is imported conditionally in nova_speak function
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import click_login_button
from location import enter_location_details
from options import read_ride_options
from confirm_and_request import confirm_and_request_ride


# === Speak Function ===
def nova_speak(text):
    print(f"\n🔊 Nova: {text}")
    # Check if we're in a production environment
    if os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true':
        # In production, just print the text
        return
    else:
        # In development, use text-to-speech
        try:
            # Only import playsound in development environment
            try:
                from playsound import playsound
                tts = gTTS(text=text, lang='en')
                filename = f"nova_{random.randint(1000,9999)}.mp3"
                tts.save(filename)
                playsound(filename)
                os.remove(filename)
            except ImportError:
                # If playsound is not available, just print the text
                print(f"Text-to-speech not available: {text}")
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            # Continue execution even if TTS fails

# === Listen Function ===
def nova_listen():
    # Check if we're in a production environment
    if os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true':
        # In production, return a default response for testing
        print("🤖 Running in production mode - using default response")
        return "book a cab"
    
    try:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as mic:
                print("🎙️ Listening...")
                recognizer.adjust_for_ambient_noise(mic)
                try:
                    audio = recognizer.listen(mic, timeout=8, phrase_time_limit=10)
                    query = recognizer.recognize_google(audio, language='en-IN')
                    print(f"🗣️ You said: {query}")
                    return query.lower()
                except sr.WaitTimeoutError:
                    print("⏱️ No response detected.")
                    return ""
                except Exception as e:
                    print(f"Speech recognition error: {e}")
                    nova_speak("Sorry, I didn't understand.")
                    return ""
        except Exception as e:
            print(f"Microphone initialization error: {e}")
            return "book a cab"  # Default response when microphone initialization fails
    except Exception as e:
        print(f"Speech recognition system error: {e}")
        return "book a cab"  # Default response when speech recognition system fails

# === Greeting ===
def get_time_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# === Introduce Nova ===
def nova_intro():
    messages = [
        "Hello, I'm NovaCab. Your voice is my command.",
        "I'm Nova, designed by Sahil to assist you with cabs and conversation.",
        "Nova here! Ready to make your travels smooth and easy."
    ]
    nova_speak(random.choice(messages))

# === Sleep Mode ===
def sleep_mode():
    nova_speak("Entering sleep mode. Say 'wake up Nova' when you're ready.")
    while True:
        cmd = nova_listen()
        if "wake up nova" in cmd or ("wake" in cmd and "nova" in cmd):
            nova_speak("Nova is awake and ready.")
            break

# === Open Uber Mobile Website with Persistence ===
def open_uber_with_persistence():
    nova_speak("Opening Uber mobile website. Please wait...")

    try:
        # Configure Chrome options for headless operation in production
        options = uc.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 "
            "Mobile/15E148 Safari/604.1"
        )
        
        # Add headless mode for production environment
        if os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true':
            print("🤖 Running in headless mode for production environment")
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=420,900')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--ignore-certificate-errors')
        else:
            # For local development, use persistent profile
            username = getpass.getuser()
            custom_profile = f"C:\\Users\\{username}\\clova-mobile-profile"
            options.add_argument(f"--user-data-dir={custom_profile}")
            options.add_argument("--profile-directory=Profile1")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        try:
            # Initialize Chrome driver with more flexible version handling
            print("Initializing Chrome driver...")
            try:
                # Try with specific version first
                driver = uc.Chrome(version_main=138, options=options)
            except Exception as version_error:
                print(f"Error with specific Chrome version: {version_error}")
                # Fall back to automatic version detection
                driver = uc.Chrome(options=options)
                
            # Set window size if not already set in options
            if os.environ.get('RAILWAY_ENVIRONMENT') != 'production' and os.environ.get('RENDER') != 'true':
                driver.set_window_size(420, 900)

            # Open Uber mobile site with retry logic
            print("Opening Uber mobile site...")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    driver.get("https://m.uber.com/go/home")
                    break
                except Exception as page_error:
                    if attempt < max_retries - 1:
                        print(f"Error loading page (attempt {attempt+1}): {page_error}. Retrying...")
                    else:
                        raise

            # Execute the Uber flow
            click_login_button(driver, nova_speak)
            enter_location_details(driver, nova_speak, nova_listen)
            read_ride_options(driver)
            confirm_and_request_ride(driver)
            
        except Exception as driver_error:
            print(f"⚠️ Chrome driver error: {driver_error}")
            raise

    except Exception as e:
        print(f"⚠️ Error in open_uber_with_persistence: {e}")
        nova_speak("Failed to open Uber mobile website.")
        # In production, we want to see the full error details
        if os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true':
            import traceback
            traceback.print_exc()


# === Command Handler ===
def handle_command(cmd):
    if "introduce" in cmd or "who are you" in cmd:
        nova_intro()
    elif "sleep" in cmd:
        sleep_mode()
    elif "exit" in cmd or "quit" in cmd:
        nova_speak("Goodbye. Nova signing off.")
        return False
    elif "book a cab" in cmd or "open uber" in cmd:
        open_uber_with_persistence()
    else:
        nova_speak("I didn't catch that.")
    return True

# === Assistant Loop ===
def nova_loop():
    nova_speak("Nova is standing by. Say 'wake up Nova' to begin.")
    awake = False

    # In production, skip the wake-up command
    if os.environ.get('RAILWAY_ENVIRONMENT') == 'production' or os.environ.get('RENDER') == 'true':
        awake = True
        nova_speak(get_time_greeting())

    while True:
        command = nova_listen()
        if not awake:
            if "wake up nova" in command or ("wake" in command and "nova" in command):
                awake = True
                nova_speak(get_time_greeting())
                continue
            else:
                continue

        if not handle_command(command):
            break

# === Start Nova ===
if __name__ == "__main__":
    nova_loop()
