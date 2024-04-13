import os
import re
import spacy
from spellchecker import SpellChecker

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def count_sentences(essay):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(essay)
    sentence_count = 0
    for sent in doc.sents: 
        finite_verbs = [token for token in sent if token.tag_ in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ") and token.dep_ != "aux"]
        if finite_verbs:
            sentence_count += 1
    return sentence_count

def score_subject_verb_agreement(essay, nlp):
    if not essay.strip():  # Check for empty essays
        return 0  # Or another appropriate handling
    doc = nlp(essay)
    agreements = 0
    total = 0
    for token in doc:
        if "subj" in token.dep_:  # Check for subjects
            # Find the main verb in the sentence which may not necessarily be the root
            verbs = [child for child in token.head.children if child.pos_ == "VERB"]
            main_verb = verbs[0] if verbs else None
            if main_verb:
                total += 1
                # Expanding tags for singular and plural detection
                subject_agreement = "SINGULAR" if token.tag_ in {"NN", "NNP"} else "PLURAL"
                verb_agreement = "SINGULAR" if main_verb.tag_ in {"VBZ", "VBP"} else "PLURAL"
                agreements += (subject_agreement == verb_agreement)

    agreement_ratio = (agreements / total) if total > 0 else 0

    # Return a score based on the ratio
    if agreement_ratio > 0.75:
        return 4
    elif agreement_ratio > 0.50:
        return 3
    elif agreement_ratio > 0.25:
        return 2
    else:
        return 1
    
def check_main_verbs(essay, nlp):
    doc = nlp(essay)
    total_sentences = 0
    sentences_with_main_verbs = 0

    for sent in doc.sents:
        total_sentences += 1
        # Check for a main verb in the sentence, which isn't an auxiliary verb
        if any(token.pos_ == 'VERB' and token.dep_ not in {'aux', 'auxpass'} for token in sent):
            sentences_with_main_verbs += 1

    return sentences_with_main_verbs, total_sentences
def analyze_verb_errors(essay, nlp):
    doc = nlp(essay)
    error_count = 0
    total_verbs = 0

    # Define common error patterns in POS tags
    error_patterns = [
        ['PRON', 'VERB', 'NOUN'],  # Hypothetical incorrect sequence
        ['VERB', 'VERB', 'VERB'],  # Potentially incorrect consecutive verbs
    ]

    for sent in doc.sents:
        pos_tags = [token.pos_ for token in sent if not token.is_punct]
        total_verbs += sum(1 for tag in pos_tags if tag == 'VERB')

        # Check for defined error patterns within the sentence
        for i in range(len(pos_tags) - max(len(pattern) for pattern in error_patterns) + 1):
            for pattern in error_patterns:
                if pos_tags[i:i+len(pattern)] == pattern:
                    error_count += 1

    if total_verbs > 0:
        error_ratio = error_count / total_verbs
    else:
        error_ratio = 0

    # Calculate the score based on the number of errors detected
    score = max(5 - int(5 * error_ratio), 1)
    return score

def spell_check(essay):
    spell = SpellChecker()
    words = re.findall(r'\b\w+\b', essay.lower())  # Extract words using regex
    misspelled = spell.unknown(words)
    num_mistakes = len(misspelled)
    if num_mistakes > 20:
        return 4
    elif num_mistakes > 15:
        return 3
    elif num_mistakes > 10:
        return 2
    elif num_mistakes > 5:
        return 1
    else:
        return 0

def main():
    directory = 'essays_dataset/essays/'
    nlp = spacy.load("en_core_web_sm")  # Load the SpaCy NLP model once
    while True:
        file_name = input("Enter the name of the text file to read from (press 'e' to exit): ").strip("'\"")
        if file_name.lower() == 'e':
            print("Exiting...")
            break

        file_path = os.path.join(directory, file_name)
        contents = read_text_file(file_path)
        if contents:
            num_sentences = count_sentences(contents)
            spelling_score = spell_check(contents)
            agreement_score = score_subject_verb_agreement(contents, nlp)
            main_verbs_count, total_sentences = check_main_verbs(contents, nlp)
            pattern_error_score = analyze_verb_errors(contents, nlp)

            print(f"Number of Sentences: {num_sentences}")
            print(f"Spelling Score: {spelling_score}")
            print(f"Subject-Verb Agreement Score: {agreement_score}")
            print(f"Sentences with Main Verbs: {main_verbs_count} out of {total_sentences}")
            print(f"Pattern of Error Score: {pattern_error_score}")

if __name__ == "__main__":
    main()
