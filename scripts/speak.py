from threading import Lock, Semaphore
import threading
import gtts
import os
import random
from playsound import playsound
import requests
from config import Config
cfg = Config()
import gtts
import threading
from threading import Lock, Semaphore

# Default voice IDs
default_voices = ["ErXwobaYiN019PkySvjV", "EXAVITQu4vr4xnSDxMaL"]

# Retrieve custom voice IDs from the Config class
custom_voice_1 = cfg.elevenlabs_voice_1_id
custom_voice_2 = cfg.elevenlabs_voice_2_id

# Placeholder values that should be treated as empty
placeholders = {"your-voice-id"}

# Use custom voice IDs if provided and not placeholders, otherwise use default voice IDs
voices = [
    custom_voice_1 if custom_voice_1 and custom_voice_1 not in placeholders else default_voices[0],
    custom_voice_2 if custom_voice_2 and custom_voice_2 not in placeholders else default_voices[1]
]

tts_headers = {
    "Content-Type": "application/json",
    "xi-api-key": cfg.elevenlabs_api_key
}

mutex_lock = Lock()  # Ensure only one sound is played at a time
# The amount of sounds to queue before blocking the main thread
queue_semaphore = Semaphore(1)


def eleven_labs_speech(text, voice_index=0):
    """Speak text using elevenlabs.io's API"""
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}".format(
        voice_id=voices[voice_index])
    formatted_message = {"text": text}
    response = requests.post(
        tts_url, headers=tts_headers, json=formatted_message)

    if response.status_code == 200:
        with mutex_lock:
            with open("speech.mpeg", "wb") as f:
                f.write(response.content)
            playsound("speech.mpeg", True)
            os.remove("speech.mpeg")
        return True
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
        return False


def gtts_speech(text):
    tts = gtts.gTTS(text)
    with mutex_lock:
        tts.save("speech.mp3")
        playsound("speech.mp3", True)
        os.remove("speech.mp3")


macos_voice_names = [
    "Zoe (Premium)",
    "Ava (Premium)",
    "com.apple.speech.synthesis.voice.custom.siri.aaron",
    "Samantha",
    "com.apple.speech.synthesis.voice.custom.siri.riya",
    "com.apple.speech.synthesis.voice.custom.siri.gordon",
    "com.apple.speech.synthesis.voice.custom.siri.arthur",
    "com.apple.speech.synthesis.voice.custom.siri.aidan",
    "com.apple.speech.synthesis.voice.custom.siri.akash",
    "com.apple.speech.synthesis.voice.custom.siri.xander",
]


def macos_tts_speech(text, voice_index=0):
    if voice_index == 0:
        os.system(f'say -v "{macos_voice_names[0]}" "{text}"')
    else:
        random_voice_index = random.randint(0, len(macos_voice_names) - 1)
        os.system(f'say -v "{macos_voice_names[random_voice_index]}" "{text}"')


def say_text(text, voice_index=0):

    
    def speak():
        if not cfg.elevenlabs_api_key:
            if cfg.use_mac_os_tts == 'True':
                macos_tts_speech(text, voice_index)
            else:
                gtts_speech(text)
        else:
            success = eleven_labs_speech(text, voice_index)
            if not success:
                gtts_speech(text)
                
        queue_semaphore.release()

    queue_semaphore.acquire(True)
    thread = threading.Thread(target=speak)
    thread.start()
