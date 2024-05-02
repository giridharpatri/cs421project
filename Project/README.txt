Teammate 1 NAME: Giridhar Patri netid: gbpatri2
Teammate 2 NAME: Janki Chaudhari netid: jchaud23

Project files & functions:
- functions.py:

    1. read_text_file: a function for reading in an essay

    2. count_sentences: function that counts the number of sentences, and provides a score 

    3. median_corpus_counts:function used to get the median counts for high and low, part of count_sentences analysis 

    4. score_subject_verb_agreement: function that scores the subject verb agreement (e.g. plurality), 
                                     counts the correct subject and verb agreements (or what it can recognize), & creates a ratio 

    5. check_main_verbs: helper functions that tries to find a main verb (that isn't auxiliary). Presence of a main verb is used in 
                         other functions.

    6. analyze_verb_errors: checks how many errors are there with verb syntax. Checks some auxiliary requirements too 
                            (like "to" when used with infinitives) 

    7. spell_check: function for scoring spelling, utilizes rudimentary regular expression and library spell check_main_verbs

    8. evaluate_syntactic_well_formedness: algorithm that yielded best results to determine whether or not a sentences is formed correctly. 
                                           rudimentary to be applicable to all essay formats. 
    
    9. evaluate_essay_coherence: function for determining coherence. Utilizes cosine similarity amongst consectutive sentences 
                                 to determine if an essay stays relatively on topic. 



- run_project.py:
    - contains code for running the project. Place any new essays files in the 'essays' folder in 
        essays_dataset (which is in the same directory as run_project.py and functions.py). Provide the name of the 
        essay file (no quotes, including .txt at the end) when prompted. 


Packages used:
- SpaCY
- Pandas 
- statistics 
- nltk 
- re (regular expressions)