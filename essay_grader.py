import sys
import pandas 
import spacy
import numpy
import os

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
        finite_verbs = [token for token in sent if token.tag_ in ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ") and token.dep_ != "aux"]
        if finite_verbs:
            sentence_count += 1 
            # print(sent)
 
    print(sentence_count)
    return sentence_count



def main():
    directory = 'essays_dataset/essays/'
    while True:
        file_name = input("Enter the name of the text file to read from (press 'e' to exit): ").strip("'\"")
        if file_name.lower() == 'e':
            print("Exiting...") 
            break  # Exit the loop if 'e' is entered
        file_path = os.path.join(directory, file_name)
        contents = read_text_file(file_path)  # Assign the returned content to contents variable 

        count_sentences(contents)
        
        # if contents is not None:  # Check if contents is not None before proceeding
        #     # Count sentences in the text
        #     num_sentences = count_sentences(contents)
        #     print("Number of Sentences:", num_sentences)

if __name__ == "__main__":
    main()