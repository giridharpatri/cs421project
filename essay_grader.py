import sys
import pandas as pd
import spacy
import numpy
import os
from spellchecker import SpellChecker
import re

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            # print(f"Contents of '{file_path}':")
            # print(contents)
            return contents
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.") 


def count_sentences(essay):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(essay)
    sentence_count = 0
    for sent in doc.sents: 
        print(sent)
        finite_verbs = [token for token in sent if token.tag_ in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ") and token.dep_ != "aux"]
        if finite_verbs:
            sentence_count += 1
        tokens = [token for token in sent if not token.is_punct]
        for i, token in enumerate(tokens[:-1]): 
            if token.text.istitle() and tokens[i-1].text in [".", "!", "?", ":", ";", "and", "but", "or"] and i != 0:  # Check if the token is capitalized and follows punctuation or conjunctions
                sentence_count += 1
                break   
            
    return sentence_count 

def score_subject_verb_agreement(essay):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(essay)
    agreements = 0
    total = 0

    for token in doc:
        if "subj" in token.dep_:
            verb = next((child for child in token.head.children if child.dep_ == "ROOT"), None)
            if verb:
                total += 1
                subject_agreement = "SINGULAR" if token.tag_ in {"NN", "NNP"} else "PLURAL"
                verb_agreement = "SINGULAR" if verb.tag_ in {"VBZ"} else "PLURAL"
                agreements += (subject_agreement == verb_agreement)

    agreement_ratio = (agreements / total) if total > 0 else 0

    if agreement_ratio > 0.75:
        return 4
    elif agreement_ratio > 0.50:
        return 3
    elif agreement_ratio > 0.25:
        return 2
    else:
        return 1

def spell_check(essay):
    spell = SpellChecker()
    words = essay.split()
    words = re.findall(r'\b\w+\b', essay.lower()) 
    misspelled = spell.unknown(words)
    num_mistakes = len(misspelled) 
    print(num_mistakes)
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
    csv_path = 'essays_dataset/index.csv'
    # df = pd.read_csv(csv_path) 
    directory = 'essays_dataset/essays/'

    while True:
        file_name = input("Enter the name of the text file to read from (press 'e' to exit): ").strip("'\"")
        if file_name.lower() == 'e':
            print("Exiting...") 
            break  # Exit the loop if 'e' is entered

        file_path = os.path.join(directory, file_name)
        contents = read_text_file(file_path)  # Assign the returned content to contents variable 

        if contents is not None:
            # Count sentences in the text
            num_sentences = count_sentences(contents)
            print(f"Number of Sentences: {num_sentences}")
            
            # Calculate the spelling score
            spelling_score = spell_check(contents)
            print(f"Spelling Score: {spelling_score}") 

if __name__ == "__main__":
    main()