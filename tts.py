from os import getenv
from voicevox import speak_jp
from gtts import gTTS
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

# Audio devices
SPEAKERS_INPUT_ID = int(getenv('SPEAKER_INPUT_ID'))


def speak_en_ibm(sentence):
    from ibm_watson import TextToSpeechV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    authenticator = IAMAuthenticator(getenv('IBM_API_KEY'))
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(getenv('IBM_URL'))
    data = text_to_speech.synthesize(
        sentence,
        voice='en-US_AllisonExpressive',
        accept='audio/wav',
    ).get_result().content

    with open('audio/voice.wav','wb') as audio_file:
        audio_file.write(data)


def speak_en_gtts(sentence):
    tts = gTTS(sentence, lang="en", tld='co.uk')
    tts.save("audio/voice.wav")


def play(audio_fp):
    data, fs = sf.read(audio_fp, dtype='float32')

    sd.play(data, fs, device=SPEAKERS_INPUT_ID)
    sd.wait()

# Text-to-Speech, feel free to add your own function or add more languages
def speak(sentence, language_code='ja'):
    # Japanese
    if language_code == 'ja':
        speak_jp(sentence)
    elif language_code == 'en':
        speak_en_ibm(sentence)
        play('audio/voice.wav')
    else:
        pass

