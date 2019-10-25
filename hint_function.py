def gethint(answer, guess):
    def makeword(word):
        new = ''
        new = new.join(word)
        return new

    answer = list(answer)
    guess = list(guess)
    correct_len = len(answer)
    diff = abs(len(answer) - len(guess))
    if len(answer) > len(guess):
        for i in range(diff):
            guess.append('_')

    elif len(answer) < len(guess):
        for i in range(diff):
            answer.append('_')

    hint = []
    for first, second in zip(answer, guess):
        if first == second:
            hint.append(second)
        else:
            hint.append('-')

    hint = hint[:correct_len]
    hintword = makeword(hint)
    voice = []
    for i in hint:
        if i == '-':
            voice.append('blank')
        else:
            voice.append(i)
    return (hintword, voice)