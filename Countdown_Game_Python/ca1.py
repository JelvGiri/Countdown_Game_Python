import random
from threading import Timer
def select_characters():
    '''
    Return 9 letters that are either a consonant or a vowel.
    Ask user to input 'c' for a consonant or 'v' for a vowel
    if input is 'c', while number of letters are less than 9.
    '''
    vowels = 'aeiou'
    cons = 'bcdfghjklmnpqrstvwxyz'
    chars = []
    numlet = 0

    # generate random vowels or random consonants based on user inputs
    while numlet < 9:
        letter = input("Enter the letter \'C\' for consonant or \'V\' for vowel: ")
        letter = letter.lower().strip()

        # generate random consonant if user enters letter c
        if letter == 'c':
            chars.append(random.choice(cons))
            numlet += 1

        # generate random vowel if user enters letter v
        elif letter == 'v':
            chars.append(random.choice(vowels))
            numlet += 1

        # Other inputs are invalid
        else:
            print('Invalid User Input, please enter \'C\' for consonant or \'V\' for vowel')
    return chars

def dictionary_reader():
    '''
    Returns a list of all the possible correct words for the game.
    '''
    # words.txt are all the words from the dictionary
    file1 = open('words.txt', 'r')
    lines = file1.readlines()

    # Store all the possible correct words in a list
    # All possible correct words will have 9 or less than 9 characters
    l=[]
    for i in lines:

        # Checks if word has 9 or less characters (Get rid of '\n')
        if len(i)<=10: # 10 as '\n' counts as a character
            l.append(i.replace('\n', ''))

    # Close the file
    file1.close()

    # Return all the words from the dictionary
    return l


def check_guess(answer, words, chosen_chars):
    '''
    Checks if the user's guess is a valid word and the word can be
    created from characters randomly selected by the user.
    Returns the user score if the user's guess is valid and can be
    created from the characters and returns 0 if not.

    :param answer: User's guess
    :param words: text file containing all words in the dictionary
    :param chosen_chars: characters randomly selected by the use
    '''
    # Check if user's guess is a valid word
    if answer in words:
        # Sort the letters of user's guess alphabetically
        sorted_guess = ''.join(sorted(answer))

        # Check different combinations of the chosen characters
        # Pick the ones with the same length as the answer
        combi = []
        same_len = []
        for i in range(len(chosen_chars) - 1, -1, -1):
            for j in range(len(combi)):
                combination = chosen_chars[i] + combi[j]
                combi.append(combination)
                if len(combination)==len(answer):
                    same_len.append(combination)

            combi.append(chosen_chars[i])

        # Return the user score if sorted user guess matches sorted combination of game letters
        for i in same_len:
            sort_letters = ''.join(sorted(i))
            if sort_letters == sorted_guess:
                return len(answer)

        # If User's answer is a word but not all letters were chosen from the game letters
        return 0
    else:
        # If User's answer is not a word
        return 0

def word_lookup(words, chosen_chars):
    '''
    Return the longest words that can be made from the characters
    selected by the user

    :param words: text file containing all words in the dictionary
    :param chosen_chars: characters randomly selected by the user
    '''

    # sort every word alphabetically and get rid of the capital letters
    sorted_words = []
    for i in words:
        sorted_words.append(''.join(sorted(i.lower())))

    # generate all combinations of game letters
    combi = []
    for i in range(len(chosen_chars) - 1, -1, -1):
        for j in range(len(combi)):
            combination = chosen_chars[i] + combi[j]
            combi.append(combination)

        combi.append(chosen_chars[i])

    # sort the combinations out in alphabetical order
    combi.sort()
    combi.sort(key=len)
    for i in range(len(combi)):
        combi[i] = ''.join((sorted(combi[i])))
    # Remove any duplicates from list (same randomly character was selected)
    combi = list(dict.fromkeys(combi))

    # Assign the words to their alphabetical order of their letters
    alpha_x = {}
    for i in range(len(sorted_words)):
        alpha_x[sorted_words[i]] = words[i]

    # Finds all the words that can be created from the randomly selected characters
    # If sorted combination of game letters match sorted possible answer word, find
    # its corresponding word and store the word.
    answers = []
    for i in sorted_words[::-1]:
        for j in combi[::-1]:
            if i == j:
                answers.append(alpha_x[i])

    # Finds the longest words
    longest_len = 0
    longest_strings = []
    for i in answers:
        if len(i) > longest_len:
            longest_len = len(i)
            longest_strings = [i]
        elif len(i) == longest_len:
            longest_strings.append(i)

    return longest_strings


if __name__ == "__main__":
    # Start the game, user chooses vowels and consonants
    print('Welcome to the Countdown game')
    chosen_chars = select_characters()
    print(chosen_chars)

    # User has 30 seconds to come up with the longest word based on the randomly chosen characters
    t = Timer(30, print, ['Times up!'])
    t.start()
    prompt = "You have 30 seconds to come up with the longest word with these characters.\n"
    answer = input(prompt)
    t.cancel()

    words = dictionary_reader()

    if answer == "":
        print('No input provided')
    else:
        # Checks if user's answer is a valid word and can be created from randomly selected characters
        user_score = check_guess(answer, words, chosen_chars)
        if user_score!=0:
            print('Your answer is valid and your score is %d' % user_score)
        else:
            print("Your answer is not valid so you Score 0 points.")

        # Find the longest word possible from the randomly selected characters
        longest_words = word_lookup(words, chosen_chars)
        max_length = str(len(longest_words[0]))
        print('Best possible answers are: ' + ', '.join(longest_words) + '.')
        print('Each answer has a length of ' + max_length + '.')

        # Game Outro to user
        print('Thank you for playing the game.')








