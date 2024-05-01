from functions import (
    read_text_file, count_sentences, median_corpus_counts,
    score_subject_verb_agreement, check_main_verbs, analyze_verb_errors, spell_check,
    evaluate_syntactic_well_formedness, evaluate_essay_coherence
)
import spacy
import os
import nltk
import numpy as np
from scipy import sparse

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def main():
    directory = 'Project/essays_dataset/essays/'

    # Load Spacy NLP model
    nlp = spacy.load("en_core_web_sm")  
    while True:
        file_name = input("Enter the name of the text file to read from (press 'e' to exit): ").strip("'\"")
        if file_name.lower() == 'e':
            print("Exiting...")
            break

        file_path = os.path.join(directory, file_name)
        contents = read_text_file(file_path)
        if contents:
            num_sentences = count_sentences(contents, nlp)
            spelling_score = spell_check(contents)
            agreement_score = score_subject_verb_agreement(contents, nlp)
            main_verbs_count, total_sentences = check_main_verbs(contents, nlp)
            pattern_error_score = analyze_verb_errors(contents, nlp)
            syntactic_score = evaluate_syntactic_well_formedness(contents, nlp)
            coherence_score = evaluate_essay_coherence(contents, nlp)

            final_score = (2 * num_sentences - spelling_score + agreement_score +
                           2 * syntactic_score + 3 * coherence_score)

            threshold = 20.44 
            qualitative_score = "High" if final_score >= threshold else "Low"

            print(f"Number of Sentences score: {num_sentences}")
            print(f"Spelling Deductions: {spelling_score}")
            print(f"Subject-Verb Agreement Score: {agreement_score}")
            print(f"Verb Tense Error Score: {pattern_error_score}")
            print(f"Sentences with Main Verbs: {main_verbs_count} out of {total_sentences}")
            print(f"Syntactic Well-Formedness Score: {syntactic_score}")
            print(f"Coherence Score: {coherence_score}\n")
            print(f"Final Score: {final_score}")
            print(f"Qualitative Score: {qualitative_score}")

if __name__ == "__main__": 
    main()
