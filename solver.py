from words import load_all_words, get_all_wordle_words
from wordle import AttemptVerdict, LetterVerdict, LETTER_COUNT, MAX_ATTEMPT, get_letter_verdicts_colored, Wordle
from collections import Counter

DEB = False


# Perfect solver for Wordle.
class WordleSolver:
    def __init__(self):
        self.__all_possible_words = set(get_all_wordle_words())  # set(load_all_words(LETTER_COUNT))
        self.__invalid_letters = set()
        self.__untried_letters = set()
        self.__candidate_words = []
        self.__green_blocks = set()
        self.__yellow_blocks = set()
        self.attempt = 0
        self.game_number = -1
        self.tries = []
        self.reset()

    # resetting the variables
    def reset(self):
        self.__invalid_letters.clear()
        self.__candidate_words = sorted(list(self.__all_possible_words))
        self.__yellow_blocks.clear()
        self.__green_blocks.clear()
        self.attempt = 0
        self.__untried_letters = set(chr(ord('a') + i) for i in range(26))
        self.game_number += 1
        self.tries.clear()

    # checks for letters that are not in the word
    # returns true if any letters that are not in the word are found
    def __contains_forbidden_letters(self, word):
        for c in word:
            if c in self.__invalid_letters:
                return True
        return False

    # returns the probabilities for each character in the word
    def __get_untried_letter_probability(self, words):
        counter = Counter()
        for w in words:
            for c in w:
                if c in self.__untried_letters:
                    counter[c] += 1
        return counter

    # creates a letter frequency list and returns it
    def __get_letter_freq_map(self, words):
        counter = Counter()
        for w in words:
            for c in w:
                counter[c] += 1
        return counter

    # checking if the green letters are in the same slots that were green for them before
    def __matches_green_constraints(self, word):
        for letter, index in self.__green_blocks:
            if word[index] != letter:
                return False
        return True

    # checking if the yellow letters are in the same slot as before or not in the word
    def __matches_yellow_constraints(self, word):
        for letter, index in self.__yellow_blocks:
            if word[index] == letter or letter not in word:
                return False
        return True

    # iterating through the word possibilities and updating what words could possibly result
    #  in a win and ignoring the ones that don't match the green and yellow letters
    def __filter_out_invalid_words(self):
        new_candidates = []
        for word in self.__candidate_words:
            if self.__contains_forbidden_letters(word) or not self.__matches_green_constraints(word) or not self.__matches_yellow_constraints(word):
                continue
            new_candidates.append(word)

        # updating the new word possinbilities
        self.__candidate_words = new_candidates

    # making an educated guess for what the word could be after fine tuning our word candidates
    def __make_educated_guess(self):
        untried_letters = self.__get_untried_letter_probability(self.__candidate_words)
        freq_map = self.__get_letter_freq_map(self.__candidate_words)
        if len(untried_letters) > 1 and self.attempt <= MAX_ATTEMPT - 1:
            word_with_score = []
            word_list = self.__all_possible_words  # if (self.attempt <= MAX_ATTEMPT - 2 and len(untried_letters) >= LETTER_COUNT) else self.candidate_words
            for word in word_list:
                letters = set(word)
                untried_score = sum(untried_letters[c] if c in untried_letters else 0 for c in letters)
                freq_score = sum(freq_map[c] for c in letters)
                word_with_score.append((word, untried_score, freq_score))
            ranked_words = sorted(word_with_score,key=lambda item: (-item[1], -item[2], item[0]))
            guess = ranked_words[0][0]
        else:
            guess = sorted(self.__candidate_words,key=lambda word: (-len(set(word)), -sum(freq_map[c] for c in word), word))[0]
        return guess

    # picking the word for next guess
    def __pick_a_word(self):
        self.__filter_out_invalid_words()
        if DEB:
            print(f"Remaining Candidates: {len(self.__candidate_words)}")

        if len(self.__candidate_words) == 0:
            print("Game's word doesn't exist in our dictionary.")
            exit(1)
        elif len(self.__candidate_words) == 1:
            return self.__candidate_words[0]

        # finds the best probability for a word to be winning and returns it
        return self.__make_educated_guess()

    # word guesser, gets the best word to choose from pick a word and guesses it
    def solve(self, wordle):
        if DEB:
            print("=" * 20)
            print(f"Game: {self.game_number}")
            print("=" * 20)

        # runs 6 attempts and guesses the best word it can find from an algorithm,
        # then guesses until either winning or losing
        while True:
            self.attempt += 1
            guess = self.__pick_a_word()
            if DEB:
                print(f"Guessing: {guess} ", end="")
            result, letter_verdicts = wordle.guess(guess)

            self.tries.append(guess)

            if DEB:
                print(get_letter_verdicts_colored(letter_verdicts), end=" ")

            if result == AttemptVerdict.WON:
                return True
            elif result == AttemptVerdict.LOST:
                return False
            elif result == AttemptVerdict.FAILED_ATTEMPT:
                for chr in guess:
                    self.__untried_letters.discard(chr)
                for i in range(len(letter_verdicts)):
                    letter, verdict = letter_verdicts[i]
                    if verdict == LetterVerdict.GRAY:
                        self.__invalid_letters.add(letter)
                    elif verdict == LetterVerdict.GREEN:
                        self.__green_blocks.add((letter, i))
                        if (letter, i) in self.__yellow_blocks:
                            self.__yellow_blocks.remove((letter, i))
                    elif verdict == LetterVerdict.YELLOW:
                        self.__yellow_blocks.add((letter, i))
                    else:
                        exit(1)
            elif result == AttemptVerdict.INVALID_WORD:
                self.attempt -= 1
                self.__candidate_words.remove(guess)
                self.__all_possible_words.remove(guess)

# plays a set amount of games the user specifies, if they don't specify, then the default is 1
def play_games(count=1):
    wordle = Wordle()
    solver = WordleSolver()
    for i in range(count):
        solver.reset()
        # wordle.override_todays_word("mover")
        solver.solve(wordle)
        print("Actual word:", wordle.todays_word)
        print()
        wordle.next_game()

# running specified number of wordle games
if __name__ == '__main__':
    DEB = True
    play_games(5)
