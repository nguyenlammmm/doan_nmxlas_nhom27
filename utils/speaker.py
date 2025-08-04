from gtts import gTTS
import os
import uuid
from pygame import mixer
import threading
mixer.init()
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print("Speak error:", e)

def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()
