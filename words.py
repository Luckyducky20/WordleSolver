from collections import Counter


# Class to laod all words from unix dictionary.
def load_all_words(letter_count=5):
    with open("/usr/share/dict/words", "r") as word_file:
        return sorted([word.strip().lower() for word in word_file.readlines() if len(word.strip()) == letter_count])


def get_letter_freq_map(words):
    counter = Counter()
    for w in words:
        for c in w:
            counter[c] += 1
    return counter


def get_letter_freq_sorted_list(words):
    return sorted(get_letter_freq_map(words).items(), key=lambda item: item[1], reverse=True)


def get_all_wordle_words():
    with open("all_wordle_words.txt", "r") as infile:
        return [line.strip() for line in infile.readlines()]


all_words = set(load_all_words())
wordle_words = get_all_wordle_words()
print(len(wordle_words))

# for word in wordle_words:
#     if word not in all_words:
#         print(word)
