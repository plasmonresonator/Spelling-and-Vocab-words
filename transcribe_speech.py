import random
import time
import speech_recognition as sr
from datetime import datetime

def listen(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be Microphone' instance")


    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print('\tSay your answer now.')
        audio = recognizer.listen(source)
        
    response = {
        'success': True,
        'error': None,
        'transcription': None
        }

    try:
        response['transcription'] = recognizer.recognize_google(audio)
        print('Translating...')
    except sr.RequestError:
        response['success'] = False
        response['error'] = 'API unavailable'
    except sr.UnknownValueError:
        response['error'] = 'Unable to recognize speech'
    return response