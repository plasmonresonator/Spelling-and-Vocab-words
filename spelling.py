import win32com.client as wincl
import os
import random, time
from datetime import datetime

def speak(word):
	speak = wincl.Dispatch('SAPI.SpVoice')
	speak.Speak(word)

words = ['mountainous', 'jealous', 'famous', 'adventurous', 'ravenous', 'nervous', 'enormous', 'fabulous',
		'tremendous', 'mysterious', 'humorous', 'generous', 'delicious', 'igneous', 'rigorous',
]


praise = ['freaking awesome!', 'nice job!', 'you are so damn smart!!!', 'you are smart as shit!!!']
beating = ['haha!  I knew I could trick you!', 'better luck next time!',]

correct = []
wrong = []
for word in words:
	x=0
	proceed = 'n'
	while proceed == 'n':
		question = f'How do you spell the word? {word}'
		speak(question)
		guess = input("How dow you spell this word? (type the letter 'r' to repeat the word)\t")
		if str.lower(guess) == 'r':
			proceed = 'n'

		elif str.lower(guess) == word:
			correct.append(word)
			speak(random.choice(praise))
			proceed = 'y'

		elif str.lower(guess) != word:
			x+=1
			speak(random.choice(beating))

		if x>=3:
			wrong.append(word)
			proceed = 'y'
			speak('This is how you spell it')
			print(f"\n{word}\n")

with open('maddie_spelling_results.txt', 'a+') as f:
	f.write(f"Current time: {datetime.now()}\n\n")
	f.write(f"Words below were spelled correctly in less than 3 trys.\n\n")
	for word in correct:
		f.write(f'{word}\n')

	f.write(f"\n\nWords below were not spelled correctly within 3 trys.\n\n")
	for word in wrong:
		f.write(f'{word}\n')

	f.write('\n\n**********************************************\n\n')