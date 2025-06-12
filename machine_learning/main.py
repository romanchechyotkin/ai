import argparse
import nltk

def parse_args():
    parser = argparse.ArgumentParser(
        description="receive text to be edited"
    )

    parser.add_argument(
        'text',
        metavar='input text',
        type=str,
    )

    args = parser.parse_args()

    return args.text


def clean_input(text):
    return str(text.encode().decode('ascii', errors='ignore'))


def preprocess_input(text):
    sentences = nltk.sent_tokenize(text)
    print(sentences)
    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    return tokens

def count_word_usage(sentences: list[list[str]], words: list[str]):
    count = 0

    for sentence in sentences:
        for word in words:
            if word in sentence:
                count += 1

    return count

def generate_suggestions(sentence_list):
    told_said_usage = sum(
        (count_word_usage(tokens, ["told", "said"]) for tokens in sentence_list)
    )

    but_and_usage = sum(
        (count_word_usage(tokens, ["but", "and"]) for tokens in sentence_list)
    )

    wh_adverbs_usage = sum(
        (count_word_usage(
            tokens,
            [
                "when",
                "where",
                "why",
                "whence",
                "whereby",
                "wherein",
                "whereupon",
            ],
        )
        for tokens in sentence_list)
    )

    result_str = ""
    adverb_usage = "Adverb usage: %s told/said, %s but/and, %s wh adverbs" % (
        told_said_usage,
        but_and_usage,
        wh_adverbs_usage,
    )

    result_str += adverb_usage

    average_word_length = compute_total_average_word_length(sentence_list)
    unique_words_fraction = compute_total_unique_words_fraction(sentence_list)
    word_stats = "Average word length %.2f, fraction of unique words %.2f" % (
        average_word_length,
        unique_words_fraction,
    )

    result_str += "<br/>"
    result_str += word_stats

    number_of_syllables = count_total_syllables(sentence_list)
    number_of_words = count_total_words(sentence_list)
    number_of_sentences = len(sentence_list)
    syllable_counts = "%d syllables, %d words, %d sentences" % (
        number_of_syllables,
        number_of_words,
        number_of_sentences,
    )

    result_str += "<br/>"
    result_str += syllable_counts
    flesch_score = compute_flesch_reading_ease(
        number_of_syllables, number_of_words, number_of_sentences
    )
    flesch = "%d syllables, %.2f flesch score: %s" % (
        number_of_syllables,
        flesch_score,
        get_reading_level_from_flesch(flesch_score),
    )

    result_str += "<br/>"
    result_str += flesch

    return result_str

def compute_total_average_word_length(sentence_list):
    total_length = 0
    total_words = 0
    
    for sentence in sentence_list:
        for word in sentence:
            total_length += len(word)
            total_words += 1
    
    return total_length / total_words if total_words > 0 else 0

def compute_total_unique_words_fraction(sentence_list):
    all_words = []
    for sentence in sentence_list:
        all_words.extend(sentence)
    
    unique_words = set(all_words)
    return len(unique_words) / len(all_words) if all_words else 0

def count_syllables(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    previous_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_is_vowel:
            count += 1
        previous_is_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1

    if count == 0:
        return 1
    
    return count

def count_total_syllables(sentence_list):
    total_syllables = 0
    for sentence in sentence_list:
        for word in sentence:
            total_syllables += count_syllables(word)
    return total_syllables

def count_total_words(sentence_list):
    all_words = sum(len(sentence) for sentence in sentence_list)

    all_symbols = 0
    for sentence in sentence_list:
        for word in sentence:
            if word in "?<>/|!@#$%^*()_{}[]":
                all_symbols += 1
    
    return all_words - all_symbols

def compute_flesch_reading_ease(syllables, words, sentences):
    if sentences == 0 or words == 0:
        return 0
    
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

def get_reading_level_from_flesch(score):
    if score >= 90:
        return "Very easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College)"
    else:
        return "Very difficult (College graduate)"

input_text = parse_args()
input = clean_input(input_text)
tokenized_sentences = preprocess_input(input)
print(tokenized_sentences)
suggestions = generate_suggestions(tokenized_sentences)
print(suggestions)