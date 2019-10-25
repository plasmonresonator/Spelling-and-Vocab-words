import os
import sys
import random
import time
from datetime import datetime
from datetime import date
import pyttsx3
from send_gmail_results import send_email
import win32com.client as wincl
from credentials import app_password, matt_email, maddie_email, krista_email
from current_vocab_words import definitions
import speech_recognition as sr
from speak import speak_fast, speak_slow, speak
from transcribe_speech import listen
import webbrowser
from hint_function import gethint

num_guesses = 3
prompt_limit = 5

recognizer = sr.Recognizer()
microphone = sr.Microphone()

praise = ['freaking awesome!', 'nice job!', 'you are so damn smart, Maddie!!!',
          'see, I told you, computers are dumb, and you are awesome!',
          "You're killing it, Maddie!"
          ]

beating = ['oops!', 'haha!  I knew I could trick you!',
           'better luck next time!',
           'are you telling me the computer is smarter than you?!']

def listen_for_answer(question, answer):
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



'''

def play_game():
    print(timestamp)

    with open(filename, 'a+') as f:
        f.write(f"Start time: {datetime.now()}\n\n")
        f.write(f"Here are the words that were tested during this session:\n\n")
        for word in words_list:
            f.write(f'\n\t{word}')

    tries = {}
    correct = []
    wrong = []
    wrong_holder = []
    accuracy = {}
    complete_miss = []
    correct_second = {}
    print("Greetings Meatbag! So you'd like to practice some spelling? First, tell me your name.")
    speak_fast("Greetings Meatbag! So you'd like to practice some spelling? First, tell me your name.")
    name = input('Please type your name:\t')
    if str.lower(name) == 'maddie':
        print('Hello Maddie McStinkerbutt! Let\'s get started!')
        speak_fast("Hello Maddie McStinkerbutt! Let's get started!")
    else:
        speak_fast(f"You just told me your name was {name}.")
        speak_fast("If you can't even spell your name right, how the heck do you think you are going to spell all these words?!?!")

    # print(f"There are {len(words_list)} words in your word list.  If you would like to add more words to the list for practice, please type 'more' and press enter, otherwise, just press enter to get started.")
    # speak(f"There are {len(words_list)} words in your word list.  If you would like to add more words to the list for practice, please type 'more' and press enter, otherwise, just press enter to get started.")
    # more = input("Would you like to add more words to practice? (type 'more' and press enter to add more words, otherwise, just press enter)\t")
    # if str.lower(more) == 'more':

    start = datetime.now()
    while words_list:
        word = str.lower(words_list.pop(random.randrange(len(words_list))))
        x = 0
        proceed = 'n'
        word_log = []
        while proceed == 'n':
            question = f'How do you spell the word?'
            speak_fast(question)
            speak_slow(word)
            guess = input("\nHow dow you spell this word? (type the letter 'r' to repeat the word)\t")

            if str.lower(guess) == 'q':
                break

            elif str.lower(guess) == 'r':
                proceed = 'n'

            elif str.lower(guess) == word:
                x += 1
                correct.append(word)
                accuracy[word] = x
                speak_fast(random.choice(praise))
                proceed = 'y'

            elif str.lower(guess) != word:
                x += 1
                speak_fast(random.choice(beating))
                word_log.append(guess)
                speak_fast(f"The word you typed sounds more like")
                speak_slow(guess)

                if x == 1:
                    speak_fast("Let's try that one again.")
                elif x == 2:
                    speak_fast("Let's give it one more shot.")

                elif x >= 3:
                    wrong.append(word)
                    wrong_holder.append(word)
                    accuracy[word] = x
                    proceed = 'y'
                    tries[word] = word_log
                    speak_fast('This is how you spell it')
                    print(f"\n\t\t{word}\n")
                    time.sleep(1.5)

    if len(wrong) > 0:
        print(f"\nGreat job!  You spelled {len(correct)} words correctly! Let's work on the {len(wrong)} words that you missed the first time around.")
        speak_fast(f"Great job!  You spelled {len(correct)} words correctly! Let's work on the {len(wrong)} words that you missed the first time around.")

        # f.write(f"\n\nWords below were not spelled correctly within 3 trys.\n\n")
        # for word in wrong:
        #   f.write(f'\t{word}\n')
    while wrong:
        word = str.lower(wrong.pop(random.randrange(len(wrong))))
        x = 0
        y = accuracy[word]
        proceed = 'n'
        while proceed == 'n':
            question = f'How do you spell the word?'
            speak_fast(question)
            speak_slow(word)
            guess = input("\nHow dow you spell this word? (type the letter 'r' to repeat the word)\t")

            if str.lower(guess) == 'q':
                break

            elif str.lower(guess) == 'r':
                proceed = 'n'

            elif str.lower(guess) == word:
                x += 1
                z = x + y
                correct_second[word] = x
                speak_fast(random.choice(praise))
                proceed = 'y'

            elif str.lower(guess) != word:
                x += 1
                speak_fast(random.choice(beating))
                tries[word].append(guess)
                speak_fast(f"The word you typed sounds more like,")
                speak_slow(guess)

                if x == 1:
                    speak_fast("Let's try that one again.")
                elif x == 2:
                    speak_fast("Let's give it one more shot.")

                elif x >= 3:
                    # wrong.append(word)
                    wrong_holder.append(word)
                    accuracy[word] = x
                    proceed = 'y'
                    tries[word] = word_log
                    speak_fast('This is how you spell it')
                    print(f"\n\t\t{word}\n")
                    time.sleep(1)
                    speak_fast("That's enough for now.  We'll try that word again next time you play this game.")

    end = datetime.now()

    total_time = end - start
    minutes = total_time.seconds/60
    print(f"Nice work, Maddie! You got through all the words in {round(minutes,2)} minutes!")
    speak_fast(f"Nice work, Stinky!! You got through all the words in {round(minutes,2)} minutes!")
    with open(filename, 'a+') as f:
        # f.write(f"\n\nWords below were revisited again after missing them initially after 3 consecutive attempts.\n\n")
        # for word, trys in correct_second.items():
        #   f.write(f'\t{word} spelled correctly in {trys} attempt(s)\n')

        if len(complete_miss) > 0:
            f.write(f"\n\nWords below were not spelled correctly at all during the session:\n\n")
            for word in complete_miss:
                f.write(f'\t{word}\n')
        else:
            pass

        f.write(f'\n\nLog of spelling errors for missed words (if any) can be found below.\n')
        for word, guesses in tries.items():
            f.write(f'\nAttempts to spell {word}:')
            for i in guesses:
                f.write(f"\n\t{i}")

        f.write(f'\n\n EXCERCISE COMPLETED IN {round(minutes, 2)} minutes')
        f.write('\n\n**********************************************\n\n')

    with open(filename, 'r') as f:
        email_report = f.read()
    speak_fast('Mom and Dad should have a copy of your awesome work in their email soon!')
    try:
        send_email(recipient=krista_email, msg=email_report)
        send_email(msg=email_report)
    except Exception as e:
        print(f"Your results didn't sent for some reason.\n\n{e}\n\n\tYou can go to the folder: {os.getcwd()} and find your results file named {filename} if you want to.")


keep_playing = 'y'
while str.lower(keep_playing) == 'y':
    play_game()
    speak_fast("If you want to play again, type the letter Y and press enter.  If you want to quit type any other letter or just press enter.")
    keep_playing = input("\n\n\tDo you want to play again? If yes, type 'y', otherwise hit enter to quite the game.")

speak_fast("Nice work stinky butt!  Thanks for playing!")
closing = ['Goodbye', 'Later Gator', 'Peace Out Trout!', 'Catch you lata home skillet!']
final = random.choice(closing)
speak_fast(final)
'''
