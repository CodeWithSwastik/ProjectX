import pytchat
from chat import get_ai_response
from tts import speak_en_ibm, play
from threading import Thread
import time

VIDEO_ID = ""
chat = pytchat.create(video_id=VIDEO_ID)

def captions(text):
    with open("output.txt", "w", encoding='utf8') as outfile:
        words = text.split()
        lines = [words[i:i+10] for i in range(0, len(words), 10)]
        for line in lines:
            for word in line:
                outfile.write(word+ " ")
                outfile.flush()
                time.sleep(len(word)/10)

            outfile.write("\n")

def respond(text):
    speak_en_ibm(text)
    threads = [Thread(target=play, args=["audio/voice.wav"]), Thread(target=captions, args=[text])]
    [t.start() for t in threads]
    [t.join() for t in threads]

while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")
        resp = get_ai_response(f"{c.author.name} said {c.message}")
        respond(resp)

