# This file includes code subject to the MIT License. 
# For the full text of the license, see LICENSES/LICENSE-languageleapai.txt.
# The original code can be found at https://github.com/SociallyIneptWeeb/LanguageLeapAI.
# This modified code is also subject to the MIT License.

import wave
from os import getenv
from time import sleep

import keyboard
import pyaudio
from dotenv import load_dotenv

load_dotenv()

MIC_ID = int(getenv('MICROPHONE_ID'))
RECORD_KEY = getenv('MIC_RECORD_KEY')
LOGGING = getenv('LOGGING', 'False').lower() in ('true', '1', 't')

MIC_AUDIO_PATH = r'audio/mic.wav'
CHUNK = 1024
FORMAT = pyaudio.paInt16

def record_audio():

    p = pyaudio.PyAudio()

    mic_info = p.get_device_info_by_index(MIC_ID)
    MIC_CHANNELS = mic_info['maxInputChannels']
    MIC_SAMPLING_RATE = int(mic_info['defaultSampleRate'])

    stream = p.open(format=FORMAT,
                    channels=MIC_CHANNELS,
                    rate=MIC_SAMPLING_RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_ID)
    frames = []
    if LOGGING:
        print("Recording...")

    while keyboard.is_pressed(RECORD_KEY):
        data = stream.read(CHUNK)
        frames.append(data)
        
    if LOGGING:
        print("Stopped recording.")

    # if empty audio file
    if not frames:
        print('Error: No audio file to transcribe detected.')
        return

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(MIC_AUDIO_PATH, 'wb')
    wf.setnchannels(MIC_CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(MIC_SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    try:
        while True:
            if keyboard.is_pressed(RECORD_KEY):
                record_audio()
            else:
                sleep(0.2)

    except KeyboardInterrupt:
        print('Closing voice recorder.')    