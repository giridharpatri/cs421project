from functions import read_text_file, count_sentences, median_corpus_counts, score_subject_verb_agreement, check_main_verbs, analyze_verb_errors, spell_check
import spacy
import os
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def main():
    directory = 'Project/essays_dataset/essays/'

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

            # median_corpus_counts(nlp) # fxn call for finding median counts to inform sentence_count scoring

            print(f"Number of Sentences score: {num_sentences}")
            print(f"Spelling Deductions: {spelling_score}")
            print(f"Subject-Verb Agreement Score: {agreement_score}")
            print(f"Verb tense Score: {pattern_error_score}\n")
            print(f"Sentences with Main Verbs: {main_verbs_count} out of {total_sentences}")


if __name__ == "__main__": 
    main()
