import random
import time
import speech_recognition as sr
from datetime import datetime

# api_key = '2205b94e270d7f9be823ff62c1d61b2e5159b267'
# with open('Speech Transcription-2205b94e270d.json') as f:
#     cred_json = f.read()
def listen(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be Microphone' instance")


    with microphone as source:
        # print('listening for ambient noise...')
        # before = datetime.now()
        recognizer.adjust_for_ambient_noise(source)
        # after = datetime.now()
        # runtime = after - before
        # print(f'ambient noise took {runtime} to run.')
        print('\tSay your answer now.')
        audio = recognizer.listen(source)
        # print('listening 3')

    response = {
        'success': True,
        'error': None,
        'transcription': None
        }

    try:
        # gstart = datetime.now()
        # print('sending audio to google API')
        response['transcription'] = recognizer.recognize_google(audio)
        print('Translating...')
        # print('google api call complete')
        # gend = datetime.now()
        # g1 = gend-gstart
        # print(f'regular google time = {g1}')
        # cloudstart = datetime.now()
        # response2 = recognizer.recognize_google_cloud(audio, credentials_json=cred_json)
        # cloudend = datetime.now()
        # cloudtime = cloudend-cloudstart
        # print(f'google cloud time = {cloudtime}')
        # print(f"regular google results = {response['transcription']}")
        # print(f"google cloud results = {response2}")
    except sr.RequestError:
        response['success'] = False
        response['error'] = 'API unavailable'
    except sr.UnknownValueError:
        response['error'] = 'Unable to recognize speech'
    # print('returning transcription response back to the main program...')
    return response

'''
if __name__ == '__main__':
    words = ['apple', 'banana', 'grape', 'orange', 'mango', 'lemon']
    num_guesses = 3
    prompt_limit = 5

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    word = random.choice(words)

    print("I'm thinking of one of these words:\n")
    for word in words:
        print(word)
    print(f'\nYou have {num_guesses} tries to guess which one.')
    time.sleep(3)

    for i in range(num_guesses):
        for j in range(prompt_limit):
            print(f'Guess {i+1}. Speak!')
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess['transcription']:
                break
            if not guess['success']:
                break
            print("I didn't catch that. What did you say?\n")

        if guess['error']:
            print(f"ERROR: {guess['error']}")
            break
        print(f"You said: {guess['transcription']}")

        guess_is_correct = guess['transcription'].lower() == word.lower()
        user_has_more_attempts = i < num_guesses -1

        if guess_is_correct:
            print(f"Correct! You win!!! {word}")
            break
        elif user_has_more_attempts:
            print('Incorrect.  Try again.\n')
        else:
            print(f"Sorry, you lose!\nI was thinking of:\n{word}")
            break

'''