import sys
import time
from datetime import datetime
from datetime import date
import speech_recognition as sr
from send_gmail_results import send_email
from credentials import app_password, matt_email, maddie_email, krista_email
from current_vocab_words import definitions
import webbrowser
from hint_function import gethint
from speak import speak, speak_fast, speak_slow
from transcribe_speech import listen

num_guesses = 3
prompt_limit = 5

recognizer = sr.Recognizer()
microphone = sr.Microphone()

'''
praise = ['freaking awesome!', 'nice job!', 'you are so damn smart, Maddie!!!',
          'see, I told you, computers are dumb, and you are awesome!',
          "You're killing it, Maddie!"
          ]

beating = ['oops!', 'haha!  I knew I could trick you!',
           'better luck next time!',
           'are you telling me the computer is smarter than you?!']
'''


def listen_for_answer(question, answer):
    '''
    Main fuction for speaking definitions and asking for proper spelling.
    '''

    for i in range(num_guesses):
        for j in range(prompt_limit):
            print(f'Guess {i+1}.')
            guess = listen(recognizer, microphone)
            if guess['transcription']:
                break
            if not guess['success']:
                break
            print("I didn't catch that. What did you say?\n")
            speak_fast("I didn't catch that. What did you say?\n")

        if guess['error']:
            print(f"ERROR: {guess['error']}")
            break
        speak_fast(f"I heard you say: {guess['transcription']}")

        guess_is_correct = answer.lower() in guess['transcription'].lower()
        user_has_more_attempts = i < num_guesses - 1

        if guess_is_correct:
            print(f"Correct!")
            speak_fast(f"Correct! {answer} is the correct word for {question}")
            f.write(f"\nCorrect word guessed on try {i+1}")
            break
        elif user_has_more_attempts:
            f.write(f"\nGuess {i+1}:\t{guess['transcription']}")
            print('Incorrect.  Try again.\n')
            speak_fast("Oops, I don't think that's right, guess again.")
        else:
            f.write(f"\nGuess {i+1}:\t{guess['transcription']}")
            f.write(f"\nComputer verbally gave the correct answer after 3 missed attempts.\n")
            print(f"Incorrect, here let me help you.")
            speak_fast(f"Sorry, {answer} is the word for {question}")
            break


def spell(answer):
    f.write(f"\n\nSPELLING for the word {answer.upper()}\n")
    answer = answer.lower()
    speak_fast(f"OK, can you spell the word {answer} for me?")
    for i in range(num_guesses):
        spell_guess = input('\n\tType your answer here:\t')
        guess_is_correct = spell_guess.lower() == answer
        user_has_more_attempts = i < num_guesses - 1

        if guess_is_correct:
            f.write(f"\n{spell_guess} spelled correctly in {i+1} attempt(s)\n\n\n")
            print(f"Nice job, you nailed it!!!")
            if i+1 == 1:
                speak_fast(f"Nice job, you spelled {answer} correctly in on your first try!")
            else:
                speak_fast(f"Nice job, you spelled {answer} correctly in only {i+1} tries!")
            break
        elif user_has_more_attempts:
            f.write(f"\nAttempt {i+1}:\t{spell_guess}")
            hintword, voice = gethint(answer, spell_guess)
            print(f"Not quite, here's what you got right so far\n\t\t{hintword}")
            speak_fast(f"Not quite, here's what you got right so far")
            time.sleep(0.5)
            speak_slow(voice)
            speak_fast(f"Let's try again. Spell the word {answer}.")
        else:
            f.write(f"\nAttempt {i+1}:\t{spell_guess}")
            f.write(f"\nComputer gave correct spelling after3 missed attempts.\n")
            print(f"Let me help you.  Here's how you spell it:\n\t{answer}\n")
            speak_fast(f"Good try, but let me help you. {answer} is spelled, {list(answer)}")


today = date.today()
timestamp_raw = datetime.now()
timestamp = timestamp_raw.strftime('%Y-%m-%d, %H%M')
filename = f"Vocab results- {timestamp}.txt"

with open(filename, 'a+') as f:
    start = datetime.now()
    f.write(f"Start time: {timestamp}\n\n")
    f.write(f"Here are the words/meanings that were tested during this session:\n")
    for meaning, word in definitions.items():
        f.write(f'\n\t{word}')
    print(f"There are {len(definitions)} words to work on this week.")
    speak_fast(f"Ok Moo, there are {len(definitions)} words to work on this week. Let's do it to it pruit!")
    for meaning, word in definitions.items():
        f.write('\n\n------------------\n')
        f.write(f"Test word: {word.upper()} --- Definition given: {meaning}\n")
        print(f"What is the word for: {meaning}")
        speak_slow(f"What is the word for, {meaning}")
        listen_for_answer(meaning, word)
        spell(word)

    end = datetime.now()
    total_time = end - start
    minutes = total_time.seconds/60
    f.write(f"\n\n****************************************************************\n\n")
    f.write(f"\t\t{len(definitions)} words tested on/completed in {round(minutes, 2)} minutes.")
    f.write(f"\n\n****************************************************************\n\n")

print("Hey, you're all finished!!")
speak_fast("Hey, you're all finished now!")

with open(filename, 'r') as f:
    email_report = f.read()
    speak_fast('Mom and Dad should have a copy of your awesome work in their email soon!')
    try:
        # send_email(recipient=krista_email, msg=email_report)
        send_email(msg=email_report)
    except Exception as e:
        print(f"Your results didn't sent for some reason.\n\n{e}\n\n\tYou can go to the folder: {os.getcwd()} and find your results file named {filename} if you want to.")

print('Great work Maddie!  Thanks for playing!!! :-)')
speak_fast('Great job stinky! Thanks for playing my game, now go give Daddy a big hug!!!!')
speak_fast('Here, enjoy this short treat for all of your hard work!')
webbrowser.open('https://www.youtube.com/watch?v=-SomEwQ6L_s')
time.sleep(2)
sys.exit()