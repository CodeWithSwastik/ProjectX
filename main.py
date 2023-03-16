import requests
from os import getenv
from time import sleep

import keyboard
from dotenv import load_dotenv

from asr import transcribe
from tts import speak
from voice_recorder import record_audio
from chat import get_ai_response

load_dotenv()

RECORD_KEY = getenv('MIC_RECORD_KEY')
MIC_AUDIO_PATH = r'audio/mic.wav'
LOGGING = getenv('LOGGING', 'False').lower() in ('true', '1', 't')


def process_audio():
    # transcribe audio
    try:
        text = transcribe(MIC_AUDIO_PATH)
    except requests.exceptions.JSONDecodeError:
        print('Too many requests to process at once')
        return

    if text:
        if LOGGING:
            print(f'Heard: {text}')
    else:
        print('No speech detected.')
        return
    
    response = get_ai_response(text)
    if LOGGING:
        print(f'AI Response: {response}')
        print("Attempting to speak this.")

    speak(response)    
    if LOGGING:
        print("Finished Speaking")

def main():
    try:
        while True:
            if keyboard.is_pressed(RECORD_KEY):
                record_audio()
                process_audio()
            else:
                sleep(0.2)

    except KeyboardInterrupt:
        print('Closing voice recorder.')    



if __name__ == '__main__':
    main()
