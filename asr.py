from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv('WHISPER_BASE_URL')
REQUEST_TIMEOUT = int(getenv('REQUEST_TIMEOUT'))


def transcribe(filepath):
    try:
        with open(filepath, 'rb') as infile:
            files = {'audio_file': infile}
            r = requests.post(f'{BASE_URL}/asr?task=transcribe&language=en&output=json', files=files)

    except requests.exceptions.Timeout:
        print('Request timeout')
        return None

    except requests.exceptions.ConnectionError:
        print('Unable to reach Whisper, ensure that it is running, or the WHISPER_BASE_URL variable is set correctly')
        return None

    return r.json()['text'].strip()


def translate(filepath, language):
    try:
        with open(filepath, 'rb') as infile:
            files = {'audio_file': infile}
            r = requests.post(f'{BASE_URL}/asr?task=translate&language={language}&output=json',
                              files=files,
                              timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        print('Request timeout')
        return None

    except requests.exceptions.ConnectionError:
        print('Unable to reach Whisper, ensure that it is running, or the WHISPER_BASE_URL variable is set correctly')
        return None

    translation = r.json()['text'].strip()

    # remove most hallucinations
    if translation.lower().startswith('thank you for'):
        return None

    return translation


if __name__ == '__main__':
    # test if whisper is up and running
    print('Testing Whisper on Japanese speech sample.')
    print(f'Actual translation: How is this dress? It suits you very well.\n'
          f"Whisper translation: {transcribe('samples/japanese_speech_sample.wav')}")