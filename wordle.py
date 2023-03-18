from words import load_all_words, get_all_wordle_words
from enum import Enum

LETTER_COUNT = 5
MAX_ATTEMPT = 6


# Enum for letter verdicts
class LetterVerdict(Enum):
    GREEN = 1
    YELLOW = 2
    GRAY = 3


# Enum for attempt verdict
class AttemptVerdict(Enum):
    WON = 1
    LOST = 2
    FAILED_ATTEMPT = 3
    INVALID_TRY = 4
    INVALID_WORD = 5


# Class to simulate playing wordle
class Wordle:
    def __init__(self):
        self.attempt = 0
        self.todays_word = ""

        # sets the current day the word aprpeared
        # 0 being the first
        self.__day = 0
        self.__all_candidate_words = sorted(get_all_wordle_words())  # load_all_words(LETTER_COUNT)

        # this is for creating a sorted version of the word list
        '''
        sortedWords = open("sortedWordList", "w")
        for Word in self.__all_candidate_words:
            sortedWords.write(Word + "\n")        
        '''

        self.__word_set = set(self.__all_candidate_words)
        self.__letter_set = set()
        self.print_tiles = False
        self.reset()

    # grabbing the total word count and returning it
    def max_word_count(self):
        return len(self.__all_candidate_words)

    # overriding todays word
    def override_todays_word(self, word):
        self.todays_word = word
        self.__letter_set = set(word)

    # Resets the game
    def reset(self):
        self.attempt = 0
        self.todays_word = self.__all_candidate_words[self.__day % len(self.__all_candidate_words)]
        self.__letter_set = set(self.todays_word)

    # going to a new day for a new word
    def next_game(self):
        self.__day += 1
        self.reset()

    # Returns true if won
    def guess(self, word):
        # making sure that the word is the right length
        if len(word) != LETTER_COUNT:
            print("Give a valid 5 letter word")
            return AttemptVerdict.INVALID_TRY, None

        # checking if the word is in the word set
        if word not in self.__word_set:
            print("Invalid word. Doesn't exist in the word set.")
            return AttemptVerdict.INVALID_WORD, None

        # checking if the user has reached their maximum amount of attempts
        self.attempt += 1
        if self.attempt > MAX_ATTEMPT:
            print("You've already reached max num of attempts. Try later")
            return AttemptVerdict.LOST, None

        # creating a list of blocks showing the conditions met for each letter
        result = []
        for i in range(LETTER_COUNT):
            c = word[i]
            if c == self.todays_word[i]:
                result.append((c, LetterVerdict.GREEN))
            elif c in self.__letter_set:
                result.append((c, LetterVerdict.YELLOW))
            else:
                result.append((c, LetterVerdict.GRAY))

        # if the attempt resulted in all green blocks, then it is a win
        attempt_verdict = AttemptVerdict.WON
        for _, verdict in result:
            if verdict != LetterVerdict.GREEN:
                attempt_verdict = AttemptVerdict.FAILED_ATTEMPT
                break

        # prints out the results if the user specifies they want it
        if self.print_tiles:
            print(get_letter_verdicts_colored(result))

        # analyzing if the user lost
        if self.attempt == MAX_ATTEMPT and attempt_verdict == AttemptVerdict.FAILED_ATTEMPT:
            attempt_verdict = AttemptVerdict.LOST

        # returning the results of the attempt
        return attempt_verdict, result


def get_letter_verdicts_colored(verdicts):
    # if the verdict is false then just short return
    if not verdicts:
        return verdicts

    # variable for storing the color blocks in order
    colors = []
    
    # filling the list with the coordinated color block for each letter analysis
    for l, v in verdicts:
        if v == LetterVerdict.GREEN:
            colors.append("🟩️")
        elif v == LetterVerdict.YELLOW:
            colors.append("🟨")
        else:
            colors.append("⬜️")
    return "".join(colors)

# plays a single game
def play_single_game(wordle):
    # resetting the wordle because its the beginning of a game
    wordle.reset()
    print(wordle.todays_word)

    # taking in guesses from the user
    for i in range(MAX_ATTEMPT):
        guess = input("Guess: ")
        result, letter_verdicts = wordle.guess(guess)
        if result == AttemptVerdict.WON:
            print("Contrats! You've won!")
            return
        # print(letter_verdicts)

    print("Sorry, you've lost the game")


if __name__ == '__main__':
    wordle = Wordle()
    wordle.print_tiles = True
    play_single_game(wordle)
