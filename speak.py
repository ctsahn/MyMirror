"""
Contains an output method for the voice assistant that performs text-to-speech using GTTS.
"""
from gtts import gTTS
import os


def output(result):
    out = gTTS(text=result,lang = "en")
    out.save("rec.mp3")
    os.system("mpg321 rec.mp3")
    
