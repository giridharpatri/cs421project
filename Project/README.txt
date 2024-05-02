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
  
  Each function calculates the sub-score. The subscores are generally calculated using ratios, and the mappings were based on corpus analysis of 
  the individual tests. We sampled some high and low essays, and averaged their respective sub-scores. 


- run_project.py:
    - contains code for running the project. Place any new essays files in the 'essays' folder in 
        essays_dataset (which is in the same directory as run_project.py and functions.py). Provide the name of the 
        essay file (no quotes, including .txt at the end) when prompted.  

    - Prompts are grabbed from the index.csv file. No need to input a prompt. If you're inputting a new essay, with a new prompt        
      Then you need to add the file name, prompt, and score to the INDEX.CSV file. 


SAMPLE OUTPUT: 

'''' 
Enter the name of the text file to read from (press 'e' to exit): 38209.txt  

Number of Sentences score: 4
Spelling Deductions: 1
Subject-Verb Agreement Score: 3        
Verb Tense Error Score: 4
Sentences with Main Verbs: 21 out of 23
Syntactic Well-Formedness Score: 3     
Coherence Score: 3

Final Score: 69
Qualitative Score: High

''''

Packages used:
- SpaCY
- Pandas 
- statistics 
- nltk 
- re (regular expressions)
-scipy 
-sklearn
-pyspellchecker 
- pathlib