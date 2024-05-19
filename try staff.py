import sqlite3
import collections

def read_corpus(filename):
    # conn = sqlite3.connect(r'server side\\URL_database.db') 
    # print ("connected to DB \n")
    # cursor = conn.cursor()
    # cursor.execute(f"SELECT URL from Site where isMal == '{url}'")
    with open(filename, 'r') as f:
        return f.read().lower()
def get_word_counts(text):
    """Returns a dictionary where keys are unique words and values are their counts."""
    word_counts = collections.Counter(text.split())
    return word_counts

def edit_distance_1(word):
    """Generates all strings with 1 edit distance from the input word."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    results = []

    # Add a character anywhere
    for i in range(len(word) + 1):
        for char in alphabet:
            new_word = word[:i] + char + word[i:]
            results.append(new_word)

    # Remove a character
    if len(word) > 1:
        for i in range(len(word)):
            new_word = word[:i] + word[i + 1:]
            results.append(new_word)

    # Transpose adjacent characters
    if len(word) > 1:
        for i in range(len(word) - 1):
            new_word = word[:i] + word[i + 1] + word[i] + word[i + 2:]
            results.append(new_word)

    # Substitute a character
    for i in range(len(word)):
        for char in alphabet:
            new_word = word[:i] + char + word[i + 1:]
            results.append(new_word)

    return results

def correct(word, word_counts):
    """Attempts to correct the spelling of a word."""
    if word in word_counts:
        return word

    max_count = 0
    correct_word = word
    edit_1_words = edit_distance_1(word)
    edit_2_words = []

    # Generate edit distance 2 words
    for edit_1_word in edit_1_words:
        edit_2_words.extend(edit_distance_1(edit_1_word))

    # Find the most frequent word within edit distance 1
    for edit_1_word in edit_1_words:
        if edit_1_word in word_counts and word_counts[edit_1_word] > max_count:
            max_count = word_counts[edit_1_word]
            correct_word = edit_1_word

    # Find the most frequent word within edit distance 2 (if length > 6)
    if len(word) > 6:
        max_count_2 = 0
        correct_word_2 = correct_word
        for edit_2_word in edit_2_words:
            if edit_2_word in word_counts and word_counts[edit_2_word] > max_count_2:
                max_count_2 = word_counts[edit_2_word]
                correct_word_2 = edit_2_word

        if max_count_2 > 4 * max_count:  # More lenient for longer words
            return correct_word_2

    return correct_word

def main():
    """Reads the corpus, corrects user-provided words, and prints the results."""
    corpus_filename = r'C:\Users\omerf\OneDrive\שולחן העבודה\screenshot\b\hunger_game.txt'
    corpus_text = read_corpus(corpus_filename)
    word_counts = get_word_counts(corpus_text)

    input_words = input("Enter words to be spellchecked (separated by spaces): ").split()
    output = []

    for word in input_words:
        correction = correct(word.lower(), word_counts)
        if correction == word:
            output.append(f"- {word} is spelled correctly.")
        else:
            output.append(f"- {word} should be spelled as {correction}.")

    print("\n".join(output))
    print("\nFinished!")

if __name__ == "__main__":
    main()
