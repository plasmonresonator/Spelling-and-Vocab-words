import pyttsx3
import win32com.client as wincl

def speak_fast(message):
    engine = pyttsx3.init()
    # rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 215)
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()
    engine.stop()


def speak_slow(message):
    engine = pyttsx3.init()
    # rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()
    engine.stop()


def speak(word):
    speak = wincl.Dispatch('SAPI.SpVoice')
    speak.Speak(word)
